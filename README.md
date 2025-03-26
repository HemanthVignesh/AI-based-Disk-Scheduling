# AI-based-Disk-Scheduling
Implementing AI based approaches for Disk Scheduling in Operating Systems


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI-Based Disk Scheduling Simulator</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
            background-color: #1a1a1a;
            color: #e0e0e0;
        }
        .container {
            display: grid;
            grid-template-columns: 1fr 3fr;
            gap: 20px;
            max-width: 1400px;
            margin: 20px auto;
            padding: 20px;
        }
        .sidebar {
            background-color: #252525;
            padding: 20px;
            border-radius: 8px;
            height: fit-content;
        }
        .main-content {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        .card {
            background-color: #252525;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        h1, h2 {
            margin: 0 0 10px;
            color: #4CAF50;
        }
        .input-group {
            margin: 10px 0;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #bbb;
        }
        input, select {
            width: 100%;
            padding: 8px;
            background-color: #333;
            border: 1px solid #444;
            color: #e0e0e0;
            border-radius: 4px;
        }
        button {
            padding: 8px 16px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin: 5px 0;
        }
        button:hover {
            background-color: #45a049;
        }
        #canvas {
            background-color: #333;
            border-radius: 4px;
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
        }
        .metric-card {
            text-align: center;
            padding: 10px;
            background-color: #333;
            border-radius: 4px;
        }
        .status-indicator {
            width: 10px;
            height: 10px;
            background-color: #4CAF50;
            border-radius: 50%;
            display: inline-block;
            margin-left: 10px;
        }
        .tooltip {
            position: relative;
        }
        .tooltip:hover::after {
            content: attr(data-tooltip);
            position: absolute;
            background-color: #444;
            padding: 5px;
            border-radius: 4px;
            color: #e0e0e0;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            white-space: nowrap;
        }
        #progress {
            width: 100%;
            height: 10px;
            background-color: #444;
            border-radius: 4px;
            margin-top: 10px;
        }
        #progress-bar {
            height: 100%;
            background-color: #4CAF50;
            width: 0;
            border-radius: 4px;
            transition: width 0.3s;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Sidebar -->
        <div class="sidebar">
            <h2>Controls</h2>
            <div class="input-group">
                <label>Algorithm</label>
                <select id="algorithm">
                    <option value="fcfs">FCFS</option>
                    <option value="sstf">SSTF</option>
                    <option value="scan">SCAN</option>
                    <option value="cscan">C-SCAN</option>
                    <option value="look">LOOK</option>
                    <option value="ai">AI-Based</option>
                </select>
            </div>
            <div class="input-group">
                <label>Head Position</label>
                <input type="number" id="headPosition" value="50" min="0">
            </div>
            <div class="input-group">
                <label>Requests</label>
                <input type="text" id="requests" placeholder="e.g., 98,183,37">
            </div>
            <div class="input-group">
                <label>Workload Pattern</label>
                <select id="workload">
                    <option value="random">Random</option>
                    <option value="sequential">Sequential</option>
                </select>
            </div>
            <button onclick="startSimulation()">Start</button>
            <button onclick="pauseSimulation()">Pause</button>
            <button onclick="resumeSimulation()">Resume</button>
            <button onclick="resetSimulation()">Reset</button>
            <div id="progress"><div id="progress-bar"></div></div>
            <button onclick="saveConfig()">Save Config</button>
            <button onclick="loadConfig()">Load Config</button>
            <button onclick="showHelp()">Help</button>
            <button onclick="showFeedback()">Feedback</button>
        </div>

        <!-- Main Content -->
        <div class="main-content">
            <!-- Dashboard -->
            <div class="card">
                <h1>Disk Scheduling Dashboard</h1>
                <p>Current Algorithm: <span id="currentAlgo">None</span><span class="status-indicator"></span></p>
                <div class="metrics-grid">
                    <div class="metric-card tooltip" data-tooltip="Total distance traveled by disk head">
                        <h3>Seek Time</h3>
                        <p id="seekTime">0</p>
                    </div>
                    <div class="metric-card tooltip" data-tooltip="Time to complete each request">
                        <h3>Response Time</h3>
                        <p id="responseTime">0</p>
                    </div>
                    <div class="metric-card tooltip" data-tooltip="Requests processed per unit time">
                        <h3>Throughput</h3>
                        <p id="throughput">0</p>
                    </div>
                </div>
            </div>

            <!-- Visualization -->
            <div class="card">
                <h2>Disk Head Movement</h2>
                <canvas id="canvas" width="800" height="400"></canvas>
            </div>

            <!-- Performance Metrics -->
            <div class="card">
                <h2>Performance Metrics</h2>
                <canvas id="metricsChart" width="800" height="200"></canvas>
            </div>

            <!-- Comparison & History -->
            <div class="card">
                <h2>Comparison & History</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Algorithm</th>
                            <th>Seek Time</th>
                            <th>Response Time</th>
                            <th>Throughput</th>
                        </tr>
                    </thead>
                    <tbody id="historyTable"></tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        let simulationRunning = false;
        let paused = false;
        let sequence = [];
        let currentStep = 0;
        const history = [];

        function startSimulation() {
            if (simulationRunning) return;
            simulationRunning = true;
            const head = parseInt(document.getElementById('headPosition').value);
            const requests = document.getElementById('requests').value.split(',').map(Number);
            const algorithm = document.getElementById('algorithm').value;
            document.getElementById('currentAlgo').textContent = algorithm.toUpperCase();
            sequence = simulateAlgorithm(algorithm, head, requests);
            currentStep = 0;
            animateSimulation(head, sequence);
        }

        function pauseSimulation() {
            paused = true;
        }

        function resumeSimulation() {
            paused = false;
            animateSimulation(parseInt(document.getElementById('headPosition').value), sequence);
        }

        function resetSimulation() {
            simulationRunning = false;
            paused = false;
            document.getElementById('progress-bar').style.width = '0%';
            document.getElementById('seekTime').textContent = '0';
            document.getElementById('responseTime').textContent = '0';
            document.getElementById('throughput').textContent = '0';
            const ctx = document.getElementById('canvas').getContext('2d');
            ctx.clearRect(0, 0, 800, 400);
        }

        function simulateAlgorithm(algorithm, head, requests) {
            let seq = [...requests];
            if (algorithm === 'sstf') {
                return sstf(head, seq);
            } else if (algorithm === 'ai') {
                return seq.sort((a, b) => a - b); // Simulated AI
            }
            return seq; // FCFS or others simplified
        }

        function sstf(head, requests) {
            let sequence = [];
            let remaining = [...requests];
            let current = head;
            while (remaining.length > 0) {
                let closest = remaining.reduce((prev, curr) => 
                    Math.abs(curr - current) < Math.abs(prev - current) ? curr : prev);
                sequence.push(closest);
                current = closest;
                remaining = remaining.filter(x => x !== closest);
            }
            return sequence;
        }

        function animateSimulation(head, sequence) {
            if (!simulationRunning || paused || currentStep >= sequence.length) {
                if (currentStep >= sequence.length) {
                    updateHistory(sequence);
                }
                return;
            }
            const canvas = document.getElementById('canvas');
            const ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            const maxValue = Math.max(head, ...sequence, 200);
            const scaleY = canvas.height / maxValue;
            const stepX = canvas.width / (sequence.length + 1);

            ctx.beginPath();
            ctx.moveTo(0, canvas.height - head * scaleY);
            let points = [head, ...sequence.slice(0, currentStep + 1)];

            for (let i = 0; i < points.length; i++) {
                let x = i * stepX;
                let y = canvas.height - points[i] * scaleY;
                ctx.lineTo(x, y);
                ctx.arc(x, y, 5, 0, Math.PI * 2);
                ctx.fillStyle = '#4CAF50';
                ctx.fill();
            }

            ctx.strokeStyle = '#4CAF50';
            ctx.lineWidth = 2;
            ctx.stroke();

            const seekTime = calculateSeekTime(head, points.slice(1));
            document.getElementById('seekTime').textContent = seekTime;
            document.getElementById('responseTime').textContent = (seekTime / points.length).toFixed(2);
            document.getElementById('throughput').textContent = points.length;
            document.getElementById('progress-bar').style.width = `${(currentStep + 1) / sequence.length * 100}%`;

            currentStep++;
            requestAnimationFrame(() => animateSimulation(head, sequence));
        }

        function calculateSeekTime(head, sequence) {
            let total = Math.abs(head - sequence[0]);
            for (let i = 1; i < sequence.length; i++) {
                total += Math.abs(sequence[i] - sequence[i - 1]);
            }
            return total;
        }

        function updateHistory(sequence) {
            const algo = document.getElementById('algorithm').value;
            const seek = document.getElementById('seekTime').textContent;
            const response = document.getElementById('responseTime').textContent;
            const throughput = document.getElementById('throughput').textContent;
            history.push({ algo, seek, response, throughput });
            const table = document.getElementById('historyTable');
            table.innerHTML = history.map(h => `
                <tr>
                    <td>${h.algo.toUpperCase()}</td>
                    <td>${h.seek}</td>
                    <td>${h.response}</td>
                    <td>${h.throughput}</td>
                </tr>`).join('');
        }

        function saveConfig() {
            const config = {
                head: document.getElementById('headPosition').value,
                requests: document.getElementById('requests').value,
                algorithm: document.getElementById('algorithm').value,
                workload: document.getElementById('workload').value
            };
            localStorage.setItem('diskConfig', JSON.stringify(config));
            alert('Configuration saved!');
        }

        function loadConfig() {
            const config = JSON.parse(localStorage.getItem('diskConfig'));
            if (config) {
                document.getElementById('headPosition').value = config.head;
                document.getElementById('requests').value = config.requests;
                document.getElementById('algorithm').value = config.algorithm;
                document.getElementById('workload').value = config.workload;
                alert('Configuration loaded!');
            }
        }

        function showHelp() {
            alert('Use the controls to set parameters and run simulations. Hover over metrics for tooltips!');
        }

        function showFeedback() {
            const feedback = prompt('Please provide your feedback:');
            if (feedback) alert('Thank you for your feedback!');
        }
    </script>
</body>
</html>
