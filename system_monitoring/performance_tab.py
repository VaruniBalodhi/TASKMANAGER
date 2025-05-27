import tkinter as tk
from tkinter import ttk
import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PerformanceTab:
    def __init__(self, parent):
        self.parent = parent
        self.cpu_data = []
        self.memory_data = []
        self.disk_data = []

        self.setup_performance_ui()

    def setup_performance_ui(self):
        self.cpu_label = tk.Label(self.parent, text="CPU Usage: 0%", font=("Arial", 14))
        self.cpu_label.pack(pady=5)

        self.memory_label = tk.Label(self.parent, text="Memory Usage: 0%", font=("Arial", 14))
        self.memory_label.pack(pady=5)

        self.disk_label = tk.Label(self.parent, text="Disk Usage: 0%", font=("Arial", 14))
        self.disk_label.pack(pady=5)

        self.fig, self.ax = plt.subplots(3, 1, figsize=(6, 4))
        self.cpu_line, = self.ax[0].plot([], [], label="CPU", color='blue')
        self.memory_line, = self.ax[1].plot([], [], label="Memory", color='green')
        self.disk_line, = self.ax[2].plot([], [], label="Disk", color='red')

        for axis in self.ax:
            axis.set_xlim(0, 50)
            axis.set_ylim(0, 100)
            axis.grid(True)
            axis.legend(loc='upper right')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.parent)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.update_performance()

    def update_performance(self):
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent

        self.cpu_label.config(text=f"CPU Usage: {cpu}%")
        self.memory_label.config(text=f"Memory Usage: {memory}%")
        self.disk_label.config(text=f"Disk Usage: {disk}%")

        self.cpu_data.append(cpu)
        self.memory_data.append(memory)
        self.disk_data.append(disk)

        if len(self.cpu_data) > 50:
            self.cpu_data.pop(0)
            self.memory_data.pop(0)
            self.disk_data.pop(0)

        self.cpu_line.set_data(range(len(self.cpu_data)), self.cpu_data)
        self.memory_line.set_data(range(len(self.memory_data)), self.memory_data)
        self.disk_line.set_data(range(len(self.disk_data)), self.disk_data)

        for axis in self.ax:
            axis.set_xlim(0, max(50, len(self.cpu_data)))

        self.canvas.draw()
        self.parent.after(1000, self.update_performance)


class AppHistoryTab:
    def __init__(self, parent):
        self.parent = parent
        self.history_tree = ttk.Treeview(parent, columns=("App", "CPU", "Memory"), show="headings")
        for col in ("App", "CPU", "Memory"):
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=200)
        self.history_tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.track_history()

    def track_history(self):
        for row in self.history_tree.get_children():
            self.history_tree.delete(row)

        for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_percent']):
            try:
                name = proc.info['name'] or "Unknown"
                cpu = f"{proc.info['cpu_percent']:.1f}%"
                mem = f"{proc.info['memory_percent']:.1f}%"
                self.history_tree.insert('', 'end', values=(name, cpu, mem))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        self.parent.after(5000, self.track_history)
