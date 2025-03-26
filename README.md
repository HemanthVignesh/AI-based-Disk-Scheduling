# AI-based-Disk-Scheduling
Implementing AI based approaches for Disk Scheduling in Operating Systems

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Disk Scheduling Simulator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f0f0f0;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .section {
            margin: 20px 0;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        .input-group {
            margin: 10px 0;
        }
        label {
            display: inline-block;
            width: 150px;
            font-weight: bold;
        }
        input, select {
            padding: 5px;
            width: 200px;
        }
        button {
            padding: 8px 16px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
        #canvas {
            border: 1px solid #ccc;
            margin-top: 20px;
        }
        .results {
            margin-top: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }
        th, td {
            padding: 8px;
            border: 1px solid #ddd;
            text-align: center;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Disk Scheduling Simulator</h1>

        <!-- Input Section -->
        <div class="section">
            <h2>Configuration</h2>
            <div class="input-group">
                <label>Initial Head Position:</label>
                <input type="number" id="headPosition" value="50" min="0">
            </div>
            <div class="input-group">
                <label>Disk Requests (comma-separated):</label>
                <input type="text" id="requests" placeholder="e.g., 98,183,37,122,14,124,65,67">
            </div>
            <div class="input-group">
                <label>Algorithm:</label>
                <select id="algorithm">
                    <option value="fcfs">FCFS</option>
                    <option value="sstf">SSTF</option>
                    <option value="scan">SCAN</option>
                    <option value="cscan">C-SCAN</option>
                    <option value="look">LOOK</option>
                    <option value="ai">AI-Based (Simulated)</option>
                </select>
            </div>
            <button onclick="runSimulation()">Run Simulation</button>
        </div>

        <!-- Results Section -->
        <div class="section results" id="results">
            <h2>Results</h2>
            <table>
                <thead>
                    <tr>
                        <th>Metric</th>
                        <th>Value</th>
                    </tr>
                </thead>
                <tbody id="resultsTable">
                </tbody>
            </table>
        </div>

        <!-- Visualization Section -->
        <div class="section">
            <h2>Disk Head Movement Visualization</h2>
            <canvas id="canvas" width="1000" height="300"></canvas>
        </div>
    </div>

    <script>
        function runSimulation() {
            const headPosition = parseInt(document.getElementById('headPosition').value);
            const requestsInput = document.getElementById('requests').value;
            const algorithm = document.getElementById('algorithm').value;
            const requests = requestsInput.split(',').map(Number);

            // Simulate disk scheduling (simplified logic)
            let sequence = simulateAlgorithm(algorithm, headPosition, requests);
            let totalSeekTime = calculateSeekTime(headPosition, sequence);

            // Display results
            displayResults(totalSeekTime, sequence);

            // Draw visualization
            drawVisualization(headPosition, sequence);
        }

        function simulateAlgorithm(algorithm, head, requests) {
            let sequence = [...requests];
            switch(algorithm) {
                case 'fcfs':
                    return sequence;
                case 'sstf':
                    return sstf(head, sequence);
                case 'ai':
                    // Simulated AI optimization (simplified as sorted for demo)
                    return sequence.sort((a, b) => a - b);
                default:
                    return sequence; // Simplified for demo
            }
        }

        function sstf(head, requests) {
            let sequence = [];
            let remaining = [...requests];
            let current = head;

            while (remaining.length > 0) {
                let closest = remaining.reduce((prev, curr) =>
                    Math.abs(curr - current) < Math.abs(prev - current) ? curr : prev
                );
                sequence.push(closest);
                current = closest;
                remaining = remaining.filter(x => x !== closest);
            }
            return sequence;
        }

        function calculateSeekTime(head, sequence) {
            let total = Math.abs(head - sequence[0]);
            for (let i = 1; i < sequence.length; i++) {
                total += Math.abs(sequence[i] - sequence[i-1]);
            }
            return total;
        }

        function displayResults(totalSeekTime, sequence) {
            const table = document.getElementById('resultsTable');
            table.innerHTML = `
                <tr><td>Total Seek Time</td><td>${totalSeekTime}</td></tr>
                <tr><td>Average Seek Time</td><td>${(totalSeekTime / sequence.length).toFixed(2)}</td></tr>
                <tr><td>Sequence</td><td>${sequence.join(' -> ')}</td></tr>
            `;
        }

        function drawVisualization(head, sequence) {
            const canvas = document.getElementById('canvas');
            const ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            const maxValue = Math.max(head, ...sequence, 200);
            const scaleX = canvas.width / (sequence.length + 1);
            const scaleY = canvas.height / maxValue;

            ctx.beginPath();
            ctx.moveTo(0, canvas.height - head * scaleY);
            let points = [head, ...sequence];

            for (let i = 0; i < points.length; i++) {
                let x = i * scaleX;
                let y = canvas.height - points[i] * scaleY;
                ctx.lineTo(x, y);
                ctx.arc(x, y, 3, 0, Math.PI * 2);
                ctx.fillText(points[i], x + 5, y - 5);
            }

            ctx.strokeStyle = '#4CAF50';
            ctx.lineWidth = 2;
            ctx.stroke();
            ctx.fillStyle = 'black';
            ctx.fill();
        }
    </script>
</body>
</html>
