 AI-Based Disk Scheduling Simulator
An interactive web-based simulator that visualizes and compares traditional and AI-enhanced disk scheduling algorithms. Built with HTML, CSS, and JavaScript, this tool aids in understanding disk head movement, seek time optimization, and throughput analysis in operating systems.


 Features
Algorithm Support: Simulate various disk scheduling algorithms, including:

FCFS (First-Come, First-Served)
SSTF (Shortest Seek Time First)
SCAN
C-SCAN
LOOK
AI-Based (simulated via sorted requests)
Interactive Controls: Set initial head position, input custom disk requests, and select workload patterns (Random or Sequential).
Real-Time Visualization: Observe disk head movements on a dynamic canvas with step-by-step animation.
Performance Metrics: Monitor key metrics such as Seek Time, Response Time, and Throughput.
Progress Tracking: Visual progress bar indicating simulation status.
History Log: Compare performance across different algorithms with a detailed history table.
Configuration Management: Save and load simulation configurations using local storage.
User Assistance: Integrated tooltips and help prompts for enhanced user experience.

 Objectives
Implement and compare traditional disk scheduling algorithms.
Simulate AI-based approaches to optimize disk scheduling.
Analyze performance improvements in terms of seek time, response time, and throughput.
Provide a user-friendly simulator for visualization and testing.​

 Technologies Used
Frontend: HTML5, CSS3, JavaScript 
Visualization: Canvas API for rendering animations
Storage: LocalStorage API for saving configurations​


 Performance Metrics
Seek Time: Total distance the disk head moves to service all requests.
Response Time: Average time taken to respond to each request.
Throughput: Number of requests processed per unit time.​

 AI-Based Scheduling (Simulated)
The AI-based algorithm in this simulator is currently simulated by sorting the disk requests to minimize seek time. Future enhancements may include integrating actual AI models, such as Reinforcement Learning or Genetic Algorithms, for dynamic and intelligent scheduling.​


 Future Enhancements
Integrate real AI algorithms for disk scheduling optimization.
Enhance visualization with more detailed animations and charts.
Implement backend support for handling larger datasets and complex simulations.
Add user authentication for saving and retrieving personalized configurations.
