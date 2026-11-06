const express = require("express");
const cors = require("cors");
const path = require("path");
require("dotenv").config();

const app = express();
const PORT = process.env.PORT || 3000;

const thyroidRoutes = require("./routes/thyroid");

// Middleware
app.use(cors());
app.use(express.json());

// Serve Frontend
app.use(express.static(path.join(__dirname, "../frontend")));

// Thyroid API
app.use("/api/thyroid", thyroidRoutes);

// Test route
app.get("/api", (req, res) => {
    res.send("Thyroid App Backend is running!");
});

// Start server
app.listen(PORT, () => {
    console.log("Server running on port " + PORT);
});