const express = require("express");
const path = require("path");
const app = express();
const PORT = 3001; // 👈 Change to 3001 to match your fetch() calls

app.use(express.json()); // To handle JSON requests

// Serve static frontend files
app.use(express.static(path.join(__dirname, "public")));

// Signup route (demo — replace with your DB logic)
app.post("/signup", (req, res) => {
  const { fullname, email, password } = req.body;
  console.log("📝 Signup:", fullname, email);
  res.json({ message: "Account created successfully!" });
});

// Signin route
app.post("/signin", (req, res) => {
  const { email, password } = req.body;
  console.log("🔑 Signin:", email);
  res.json({ message: "Signed in successfully!" });
});

// Default route
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

app.listen(PORT, () => {
  console.log(`✅ Server running at http://localhost:${PORT}`);
});
