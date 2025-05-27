import tkinter as tk
from tkinter import simpledialog, messagebox


class AlertManager:
    def __init__(self, root, cpu_threshold=80, mem_threshold=500):  # thresholds: CPU (%) and memory (MB)
        self.root = root
        self.cpu_threshold = cpu_threshold
        self.mem_threshold = mem_threshold

        self.shown_alerts = set()  # to avoid repeat alerts
        self._build_threshold_ui()

    def _build_threshold_ui(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=5)

        tk.Label(frame, text="CPU Threshold (%)").pack(side=tk.LEFT)
        self.cpu_entry = tk.Entry(frame, width=5)
        self.cpu_entry.insert(0, str(self.cpu_threshold))
        self.cpu_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(frame, text="Memory Threshold (MB)").pack(side=tk.LEFT)
        self.mem_entry = tk.Entry(frame, width=5)
        self.mem_entry.insert(0, str(self.mem_threshold))
        self.mem_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(frame, text="Set Thresholds", command=self.update_thresholds).pack(side=tk.LEFT, padx=10)

    def update_thresholds(self):
        try:
            self.cpu_threshold = float(self.cpu_entry.get())
            self.mem_threshold = float(self.mem_entry.get())
            messagebox.showinfo("Thresholds Updated", f"CPU: {self.cpu_threshold}%\nMemory: {self.mem_threshold} MB")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for thresholds.")

    def check_and_alert(self, pid, name, cpu, mem):
        alert_key_cpu = f"{pid}_cpu"
        alert_key_mem = f"{pid}_mem"

        if cpu > self.cpu_threshold and alert_key_cpu not in self.shown_alerts:
            self.shown_alerts.add(alert_key_cpu)
            messagebox.showwarning("High CPU Usage", f"⚠️ Process '{name}' (PID {pid}) is using {cpu:.1f}% CPU.")

        if mem > self.mem_threshold and alert_key_mem not in self.shown_alerts:
            self.shown_alerts.add(alert_key_mem)
            messagebox.showwarning("High Memory Usage", f"⚠️ Process '{name}' (PID {pid}) is using {mem:.1f} MB memory.")
