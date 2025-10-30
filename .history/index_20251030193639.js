const express = require("express");
const cors = require("cors");
const path = require("path");
const mongoose = require("mongoose");

const app = express();
const PORT = 3001;

// ✅ Middleware
app.use(cors());
app.use(express.json());

// ✅ Serve static frontend files
app.use(express.static(path.join(__dirname, "public")));

// ✅ Connect to MongoDB
mongoose
  .connect("mongodb://localhost:27017/healthrisk_ai")
  .then(() => console.log("✅ Connected to MongoDB!"))
  .catch((err) => console.error("❌ MongoDB connection failed:", err));

// ✅ Define Schema & Model
const UserSchema = new mongoose.Schema({
  fullname: String,
  email: { type: String, unique: true },
  password: String,
});
const User = mongoose.model("User", UserSchema);

// ✅ Routes
app.post("/signup", async (req, res) => {
  const { fullname, email, password } = req.body;
  try {
    const existing = await User.findOne({ email });
    if (existing) {
      return res.status(400).json({ message: "Email already exists!" });
    }
    await User.create({ fullname, email, password });
    res.json({ message: "Account created successfully!" });
  } catch (err) {
    res.status(500).json({ message: "Server error!" });
  }
});

app.post("/signin", async (req, res) => {
  const { email, password } = req.body;
  try {
    const user = await User.findOne({ email, password });
    if (!user) {
      return res.status(401).json({ message: "Invalid credentials!" });
    }
    res.json({ message: "Signed in successfully!" });
  } catch (err) {
    res.status(500).json({ message: "Server error!" });
  }
});

// ✅ Default route (Home page)
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

// ✅ Start Server
app.listen(PORT, () => {
  console.log(`🚀 Server ready on http://localhost:${PORT}`);
});
