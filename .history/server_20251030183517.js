const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const { MongoClient, ObjectId } = require("mongodb");

// Change this to your MongoDB connection string if running remotely
const MONGO_URI = "mongodb://localhost:27017";
// Database and collection
const DB_NAME = "ML";
const COLLECTION = "user";

const app = express();
app.use(cors());
app.use(bodyParser.json());

let db, users;

// Connect to DB before handling REST requests!
MongoClient.connect(MONGO_URI, { useUnifiedTopology: true })
  .then(client => {
    db = client.db(DB_NAME);
    users = db.collection(COLLECTION);
    console.log("Connected to MongoDB!");
  })
  .catch(err => {
    console.error("MongoDB connection error: ", err);
    process.exit(1);
  });

// Signup — create a new user
app.post("/signup", async (req, res) => {
  const { fullname, email, password } = req.body;
  if (!fullname || !email || !password)
    return res.status(400).json({ error: "All fields required." });
  // Check for duplicate email
  const found = await users.findOne({ email: email.toLowerCase() });
  if (found) return res.status(409).json({ error: "User already exists." });

  const result = await users.insertOne({
    fullname,
    email: email.toLowerCase(),
    password // For production: hash this!
  });
  res.json({ success: true, fullname });
});

// Signin — check credentials
app.post("/signin", async (req, res) => {
  const { email, password } = req.body;
  if (!email || !password)
    return res.status(400).json({ error: "All fields required." });

  const user = await users.findOne({
    email: email.toLowerCase(),
    password
  });
  if (!user) return res.status(401).json({ error: "Invalid credentials." });

  res.json({ success: true, id: user._id, fullname: user.fullname });
});

// Get user by ID (for showing name when logged in)
app.get("/user/:id", async (req, res) => {
  try {
    const user = await users.findOne({ _id: new ObjectId(req.params.id) });
    if (!user) return res.status(404).json({ error: "Not found" });
    res.json({ fullname: user.fullname, email: user.email });
  } catch {
    res.status(400).json({ error: "Invalid id" });
  }
});

app.listen(3001, () => console.log("Server ready on http://localhost:3001"));
