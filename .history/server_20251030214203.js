const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const { MongoClient, ObjectId } = require("mongodb");


const MONGO_URI = "mongodb://localhost:27017";
const DB_NAME = "healthrisk_ai"; 
const USERS_COLLECTION = "user";
const SIGNINS_COLLECTION = "signins";

const app = express();
app.use(cors());
app.use(bodyParser.json());

let db, users, signins;

// Connect to MongoDB
MongoClient.connect(MONGO_URI)
  .then(async client => {
    db = client.db(DB_NAME);
    users = db.collection(USERS_COLLECTION);
    signins = db.collection(SIGNINS_COLLECTION);

    
    await users.createIndex({ email: 1 }, { unique: true, name: "uniq_email" });
    await signins.createIndex({ userId: 1, ts: -1 }, { name: "user_ts" });

    console.log("✅ Connected to MongoDB and ensured indexes!");
  })
  .catch(err => {
    console.error("❌ MongoDB connection error:", err);
    process.exit(1);
  });


const path = require("path");
app.use(express.static(path.join(__dirname, "public")));


app.get("/health", (req, res) => {
  res.json({ ok: true, db: Boolean(db) });
});


app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});


app.post("/signup", async (req, res) => {
  try {
    const { fullname, email, password } = req.body;
    if (!fullname || !email || !password) {
      return res.status(400).json({ message: "All fields are required." });
    }
    const normalEmail = String(email).toLowerCase().trim();
    await users.insertOne({ fullname, email: normalEmail, password }); // Reminder: Hash in production!
    console.log("👤 User created:", normalEmail);
    res.json({ message: "Account created successfully!" });
  } catch (err) {
    if (err && err.code === 11000) {
      return res.status(409).json({ message: "User already exists." });
    }
    console.error("Signup Error:", err);
    res.status(500).json({ message: "Server error during signup." });
  }
});

// Signin — check credentials and store a signin record
app.post("/signin", async (req, res) => {
  try {
    const { email, password } = req.body;
    if (!email || !password) {
      return res.status(400).json({ message: "All fields are required." });
    }
    const normalEmail = String(email).toLowerCase().trim();
    const user = await users.findOne({ email: normalEmail, password });
    if (!user) {
      return res.status(401).json({ message: "Invalid credentials!" });
    }

    // Store successful sign-in
    const ts = new Date();
    await signins.insertOne({ userId: user._id, email: normalEmail, ts });
    console.log("🔐 Sign-in stored:", { email: normalEmail, ts });

    res.json({ message: "Signed in successfully!", id: user._id, fullname: user.fullname });
  } catch (err) {
    console.error("Signin Error:", err);
    res.status(500).json({ message: "Server error during signin." });
  }
});

// Get user by ID
app.get("/user/:id", async (req, res) => {
  try {
    const user = await users.findOne({ _id: new ObjectId(req.params.id) });
    if (!user) return res.status(404).json({ message: "User not found." });
    res.json({ fullname: user.fullname, email: user.email });
  } catch (err) {
    console.error("User Fetch Error:", err);
    res.status(400).json({ message: "Invalid user ID." });
  }
});

// Debug endpoints
app.get("/debug/users", async (req, res) => {
  try {
    const list = await users.find({}, { projection: { password: 0 } }).limit(50).toArray();
    res.json(list);
  } catch (err) {
    console.error("Debug Users Error:", err);
    res.status(500).json({ message: "Failed to fetch users." });
  }
});

app.get("/debug/signins", async (req, res) => {
  try {
    const list = await signins.find({}).sort({ ts: -1 }).limit(50).toArray();
    res.json(list);
  } catch (err) {
    console.error("Debug Signins Error:", err);
    res.status(500).json({ message: "Failed to fetch signins." });
  }
});

// Start server
const PORT = 3001;
app.listen(PORT, () => console.log(`🚀 Server ready on http://localhost:${PORT}`));

/* 
EXAMPLE TEST USER (for form or API):
fullname: Jane Doe
email: jane@example.com
password: test12345
*/
