const express = require('express');
const router = express.Router();
const { spawn } = require('child_process');
const path = require('path');

router.post('/predict', (req, res) => {
    const inputData = req.body;
    const scriptPath = path.join(__dirname, '..', '..', 'predict_hypertension.py');
    const pythonProcess = spawn('python', [scriptPath, JSON.stringify(inputData)]);
    let resultData = '';
    let errorData = '';
    pythonProcess.stdout.on('data', (data) => { resultData += data.toString(); });
    pythonProcess.stderr.on('data', (data) => { errorData += data.toString(); });
    pythonProcess.on('close', (code) => {
        if (code !== 0) {
            return res.status(500).json({ error: errorData || 'Execution failed' });
        }
        try {
            res.json(JSON.parse(resultData.trim()));
        } catch (err) {
            res.status(500).json({ error: 'Failed to parse output', raw: resultData });
        }
    });
});

module.exports = router;
