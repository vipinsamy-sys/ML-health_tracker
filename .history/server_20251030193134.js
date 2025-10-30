const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const { MongoClient, ObjectId } = require("mongodb");

// MongoDB Connection
const MONGO_URI = "mongodb://localhost:27017";
const DB_NAME = "ML";
const COLLECTION = "user";

const app = express();
app.use(cors());
app.use(bodyParser.json());

let db, users;

// ✅ Connect to MongoDB (no deprecated options)
MongoClient.connect(MONGO_URI)
  .then(client => {
    db = client.db(DB_NAME);
    users = db.collection(COLLECTION);
    console.log("✅ Connected to MongoDB!");
  })
  .catch(err => {
    console.error("❌ MongoDB connection error:", err);
    process.exit(1);
  });

// ✅ Root route
app.get("/", (req, res) => {
  res.send("✅ Backend is running successfully!");
});

// ✅ Signup — create a new user
app.post("/signup", async (req, res) => {
  try {
    const { fullname, email, password } = req.body;

    if (!fullname || !email || !password)
      return res.status(400).json({ error: "All fields are required." });

    const found = await users.findOne({ email: email.toLowerCase() });
    if (found)
      return res.status(409).json({ error: "User already exists." });

    const result = await users.insertOne({
      fullname,
      email: email.toLowerCase(),
      password // ⚠️ For production: always hash passwords!
    });

    res.json({ success: true, fullname });
  } catch (err) {
    console.error("Signup Error:", err);
    res.status(500).json({ error: "Server error during signup." });
  }
});

// ✅ Signin — check credentials
app.post("/signin", async (req, res) => {
  try {
    const { email, password } = req.body;

    if (!email || !password)
      return res.status(400).json({ error: "All fields are required." });

    const user = await users.findOne({
      email: email.toLowerCase(),
      password
    });

    if (!user)
      return res.status(401).json({ error: "Invalid credentials." });

    res.json({ success: true, id: user._id, fullname: user.fullname });
  } catch (err) {
    console.error("Signin Error:", err);
    res.status(500).json({ error: "Server error during signin." });
  }
});

// ✅ Get user by ID
app.get("/user/:id", async (req, res) => {
  try {
    const user = await users.findOne({ _id: new ObjectId(req.params.id) });
    if (!user) return res.status(404).json({ error: "User not found." });
    res.json({ fullname: user.fullname, email: user.email });
  } catch (err) {
    console.error("User Fetch Error:", err);
    res.status(400).json({ error: "Invalid user ID." });
  }
});

// ✅ Start server
app.listen(3001, () => console.log("🚀 Server ready on http://localhost:3001"));
