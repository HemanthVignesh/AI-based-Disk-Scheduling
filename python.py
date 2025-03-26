import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import time

class DiskSchedulingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI-Based Disk Scheduling Simulator")
        self.root.configure(bg="#1a1a1a")
        self.history = []

        # Main frame
        self.main_frame = tk.Frame(root, bg="#1a1a1a")
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Sidebar (Controls)
        self.sidebar = tk.Frame(self.main_frame, bg="#252525", relief="raised", borderwidth=2)
        self.sidebar.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

        tk.Label(self.sidebar, text="Controls", bg="#252525", fg="#4CAF50", font=("Arial", 14, "bold")).pack(pady=5)

        # Algorithm selection
        tk.Label(self.sidebar, text="Algorithm", bg="#252525", fg="#bbb").pack()
        self.algo_var = tk.StringVar(value="FCFS")
        algo_menu = ttk.Combobox(self.sidebar, textvariable=self.algo_var, values=["FCFS", "SSTF", "SCAN", "C-SCAN", "LOOK", "AI-Based"])
        algo_menu.pack(pady=5)

        # Head position
        tk.Label(self.sidebar, text="Head Position", bg="#252525", fg="#bbb").pack()
        self.head_entry = tk.Entry(self.sidebar, bg="#333", fg="#e0e0e0", insertbackground="#e0e0e0")
        self.head_entry.insert(0, "50")
        self.head_entry.pack(pady=5)

        # Requests
        tk.Label(self.sidebar, text="Requests (comma-separated)", bg="#252525", fg="#bbb").pack()
        self.requests_entry = tk.Entry(self.sidebar, bg="#333", fg="#e0e0e0", insertbackground="#e0e0e0")
        self.requests_entry.insert(0, "98,183,37,122,14")
        self.requests_entry.pack(pady=5)

        # Simulation controls
        tk.Button(self.sidebar, text="Start", bg="#4CAF50", fg="white", command=self.start_simulation).pack(pady=5)
        tk.Button(self.sidebar, text="Pause", bg="#4CAF50", fg="white", command=self.pause_simulation).pack(pady=5)
        tk.Button(self.sidebar, text="Resume", bg="#4CAF50", fg="white", command=self.resume_simulation).pack(pady=5)
        tk.Button(self.sidebar, text="Reset", bg="#4CAF50", fg="white", command=self.reset_simulation).pack(pady=5)

        # Main content
        self.content = tk.Frame(self.main_frame, bg="#252525")
        self.content.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Dashboard
        self.dashboard = tk.LabelFrame(self.content, text="Dashboard", bg="#252525", fg="#4CAF50", font=("Arial", 12))
        self.dashboard.pack(fill="x", pady=5)
        self.current_algo_label = tk.Label(self.dashboard, text="Current Algorithm: None", bg="#252525", fg="#e0e0e0")
        self.current_algo_label.pack()
        self.metrics_frame = tk.Frame(self.dashboard, bg="#252525")
        self.metrics_frame.pack(pady=5)
        self.seek_label = tk.Label(self.metrics_frame, text="Seek Time: 0", bg="#333", fg="#e0e0e0", width=20)
        self.seek_label.grid(row=0, column=0, padx=5)
        self.response_label = tk.Label(self.metrics_frame, text="Response Time: 0", bg="#333", fg="#e0e0e0", width=20)
        self.response_label.grid(row=0, column=1, padx=5)
        self.throughput_label = tk.Label(self.metrics_frame, text="Throughput: 0", bg="#333", fg="#e0e0e0", width=20)
        self.throughput_label.grid(row=0, column=2, padx=5)

        # Visualization
        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.ax.set_facecolor("#333")
        self.fig.patch.set_facecolor("#252525")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.content)
        self.canvas.get_tk_widget().pack(pady=5)

        # History
        self.history_frame = tk.LabelFrame(self.content, text="Comparison & History", bg="#252525", fg="#4CAF50", font=("Arial", 12))
        self.history_frame.pack(fill="x", pady=5)
        self.history_text = tk.Text(self.history_frame, height=5, bg="#333", fg="#e0e0e0", insertbackground="#e0e0e0")
        self.history_text.pack(fill="x")

        # Simulation state
        self.running = False
        self.paused = False
        self.sequence = []
        self.current_step = 0

    def start_simulation(self):
        if self.running:
            return
        self.running = True
        try:
            head = int(self.head_entry.get())
            requests = [int(x) for x in self.requests_entry.get().split(",") if x.strip()]
            if not requests:
                raise ValueError("No valid requests provided")
        except ValueError as e:
            messagebox.showerror("Error", str(e) if str(e) else "Invalid input!")
            self.running = False
            return

        algo = self.algo_var.get()
        self.current_algo_label.config(text=f"Current Algorithm: {algo}")
        self.sequence = self.simulate_algorithm(algo, head, requests)
        self.current_step = 0
        self.animate_simulation(head)

    def pause_simulation(self):
        self.paused = True

    def resume_simulation(self):
        if not self.running or not self.paused:
            return
        self.paused = False
        self.animate_simulation(int(self.head_entry.get()))

    def reset_simulation(self):
        self.running = False
        self.paused = False
        self.current_step = 0
        self.sequence = []
        self.seek_label.config(text="Seek Time: 0")
        self.response_label.config(text="Response Time: 0")
        self.throughput_label.config(text="Throughput: 0")
        self.current_algo_label.config(text="Current Algorithm: None")
        self.ax.clear()
        self.ax.set_facecolor("#333")
        self.canvas.draw()

    def simulate_algorithm(self, algo, head, requests):
        seq = requests.copy()
        if algo == "FCFS":
            return seq
        elif algo == "SSTF":
            return self.sstf(head, seq)
        elif algo == "AI-Based":
            return sorted(seq)  # Simulated AI
        return seq  # Simplified for SCAN, C-SCAN, LOOK

    def sstf(self, head, requests):
        sequence = []
        remaining = requests.copy()
        current = head
        while remaining:
            closest = min(remaining, key=lambda x: abs(x - current))
            sequence.append(closest)
            current = closest
            remaining.remove(closest)
        return sequence

    def calculate_metrics(self, head, sequence):
        if not sequence:
            return 0, 0, 0
        seek_time = abs(head - sequence[0])
        for i in range(1, len(sequence)):
            seek_time += abs(sequence[i] - sequence[i-1])
        response_time = seek_time / len(sequence) if sequence else 0
        throughput = len(sequence)
        return seek_time, response_time, throughput

    def animate_simulation(self, head):
        if not self.running or self.paused or self.current_step >= len(self.sequence):
            if self.current_step >= len(self.sequence) and self.sequence:
                self.update_history()
                self.running = False
            return

        self.ax.clear()
        self.ax.set_facecolor("#333")
        max_value = max(head, *self.sequence, 200)
        points = [head] + self.sequence[:self.current_step + 1]

        # Plot with scale
        self.ax.plot(range(len(points)), points, color="#4CAF50", marker="o", linewidth=2)
        self.ax.set_xlim(0, len(self.sequence) + 1)
        self.ax.set_ylim(0, max_value + 10)
        self.ax.set_xlabel("Step", color="#e0e0e0")
        self.ax.set_ylabel("Head Position", color="#e0e0e0")
        self.ax.tick_params(colors="#e0e0e0")
        self.ax.grid(True, color="#444", linestyle="--", alpha=0.5)
        self.canvas.draw()

        seek, response, throughput = self.calculate_metrics(head, self.sequence[:self.current_step + 1])
        self.seek_label.config(text=f"Seek Time: {seek}")
        self.response_label.config(text=f"Response Time: {response:.2f}")
        self.throughput_label.config(text=f"Throughput: {throughput}")

        self.current_step += 1
        self.root.after(500, lambda: self.animate_simulation(head))

    def update_history(self):
        algo = self.algo_var.get()
        seek = self.seek_label.cget("text").split(": ")[1]
        response = self.response_label.cget("text").split(": ")[1]
        throughput = self.throughput_label.cget("text").split(": ")[1]
        self.history.append((algo, seek, response, throughput))
        self.history_text.delete(1.0, tk.END)
        self.history_text.insert(tk.END, "Algorithm\tSeek Time\tResponse Time\tThroughput\n")
        for h in self.history:
            self.history_text.insert(tk.END, f"{h[0]}\t\t{h[1]}\t\t{h[2]}\t\t{h[3]}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = DiskSchedulingApp(root)
    root.mainloop()
