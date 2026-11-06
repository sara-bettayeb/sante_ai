const express = require("express");
const router = express.Router();

// Import AI Assistant
const askThyroidAssistant = require("../../ai/thyroid-assistant");

// Thyroid Information Route
router.get("/info", (req, res) => {
    res.json({
        name: "Thyroid Gland",
        description: "The thyroid is a butterfly-shaped gland located in the neck.",
        hormones: ["T3", "T4"],
        function: "Regulates metabolism, energy, and body temperature."
    });
});

// AI Assistant Chat Route
router.post("/chat", async (req, res) => {
    try {
        const message = req.body.message;

        if (!message || !message.trim()) {
            return res.status(400).json({
                error: "Please enter a message."
            });
        }

        const reply = await askThyroidAssistant(message);

        res.json({ reply });

    } catch (error) {
        console.error("AI Assistant Error:", error);

        res.status(500).json({
            error: "Could not connect to the AI assistant."
        });
    }
});

module.exports = router;