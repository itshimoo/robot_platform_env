const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const { spawn } = require('child_process');
const path = require('path');

const app = express();

// Configuration
const PORT = process.env.PORT || 3000;
const HOST = process.env.HOST || 'localhost';

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

// Utility function to run Python commands
function runPythonCommand(command, args = []) {
    return new Promise((resolve, reject) => {
        const pythonPath = path.join(__dirname, '..', 'src');
        const scriptPath = path.join(__dirname, '..', 'bin', 'rpe');
        
        const childProcess = spawn('python3', [scriptPath, command, ...args], {
            cwd: path.join(__dirname, '..'),
            env: {
                ...process.env,
                PYTHONPATH: pythonPath
            }
        });
        
        let stdout = '';
        let stderr = '';
        
        childProcess.stdout.on('data', (data) => {
            stdout += data.toString();
        });
        
        childProcess.stderr.on('data', (data) => {
            stderr += data.toString();
        });
        
        childProcess.on('close', (code) => {
            if (code === 0) {
                resolve(stdout);
            } else {
                reject(new Error(stderr || `Process exited with code ${code}`));
            }
        });
        
        childProcess.on('error', (error) => {
            reject(error);
        });
    });
}

// API Routes
app.get('/api/status', async (req, res) => {
    try {
        const output = await runPythonCommand('status');
        res.json({ success: true, data: output });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

app.post('/api/build', async (req, res) => {
    try {
        const output = await runPythonCommand('build');
        res.json({ success: true, data: output });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

app.post('/api/run', async (req, res) => {
    try {
        const output = await runPythonCommand('run');
        res.json({ success: true, data: output });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

app.post('/api/stop', async (req, res) => {
    try {
        const output = await runPythonCommand('stop');
        res.json({ success: true, data: output });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

app.post('/api/clean', async (req, res) => {
    try {
        const output = await runPythonCommand('clean');
        res.json({ success: true, data: output });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

app.post('/api/exec', async (req, res) => {
    try {
        const { command } = req.body;
        if (!command) {
            return res.status(400).json({ success: false, error: 'Command is required' });
        }
        
        const output = await runPythonCommand('exec', [command]);
        res.json({ success: true, data: output });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

app.get('/api/logs', async (req, res) => {
    try {
        const lines = req.query.lines || 50;
        const output = await runPythonCommand('logs', ['-n', lines.toString()]);
        res.json({ success: true, data: output });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

app.get('/api/config', async (req, res) => {
    try {
        const output = await runPythonCommand('config');
        res.json({ success: true, data: output });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

app.post('/api/gpu', async (req, res) => {
    try {
        const output = await runPythonCommand('gpu');
        res.json({ success: true, data: output });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

app.post('/api/shell', async (req, res) => {
    try {
        const output = await runPythonCommand('shell');
        res.json({ success: true, data: output });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

app.post('/api/update', async (req, res) => {
    try {
        const output = await runPythonCommand('update');
        res.json({ success: true, data: output });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

// Start server
app.listen(PORT, HOST, () => {
    console.log(`🚀 RobotLab Web GUI running on http://${HOST}:${PORT}`);
    console.log(`📊 API available at http://${HOST}:${PORT}/api`);
}); 