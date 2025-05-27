import tkinter as tk
from tkinter import ttk, messagebox
import psutil
import threading
import time
from ai_engine.process_recommender import ProcessRecommender
from ai_engine.priority_manager import PriorityManager
from ai_engine.voice_control import VoiceCommandProcessor

class EnhancedProcessTab:
    def __init__(self, parent):
        self.parent = parent
        self.processes = []
        self.recommender = ProcessRecommender()
        self.priority_manager = PriorityManager()
        self.priority_toggle = tk.BooleanVar(value=True)
        self.voice_processor = VoiceCommandProcessor(self)

        self.setup_process_management_ui()

        toggle_btn = tk.Checkbutton(
            self.parent,
            text="Enable Auto Priority Adjustment",
            variable=self.priority_toggle,
            command=self.toggle_priority_adjustment
        )
        toggle_btn.pack(pady=5)

        self.voice_btn = tk.Button(self.parent, text="🎤 Voice Command", command=self.voice_processor.listen_and_execute)
        self.voice_btn.pack(pady=5)

        threading.Thread(target=self.monitor_priorities, daemon=True).start()

    def toggle_priority_adjustment(self):
        self.priority_manager.enabled = self.priority_toggle.get()

    def monitor_priorities(self):
        while True:
            if self.priority_manager.enabled:
                self.priority_manager.adjust_priorities()
            time.sleep(10)

    def setup_process_management_ui(self):
        # --- Search bar ---
        search_frame = tk.Frame(self.parent)
        search_frame.pack(fill='x', padx=10, pady=(10, 0))

        tk.Label(search_frame, text="Search:").pack(side='left')
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side='left', fill='x', expand=True, padx=5)
        self.search_entry.bind('<KeyRelease>', self.on_search)

        # --- Process Treeview ---
        self.proc_tree = ttk.Treeview(self.parent, columns=('PID', 'Name', 'CPU', 'Memory', 'Status'), show='headings')
        for col in self.proc_tree["columns"]:
            self.proc_tree.heading(col, text=col)
            self.proc_tree.column(col, width=120)
        self.proc_tree.pack(fill='both', expand=True, padx=10, pady=10)

        # --- Buttons ---
        button_frame = tk.Frame(self.parent)
        button_frame.pack(pady=5)

        self.refresh_btn = tk.Button(button_frame, text="Refresh", command=self.refresh_process_list)
        self.refresh_btn.grid(row=0, column=0, padx=5)

        self.kill_btn = tk.Button(button_frame, text="End Task", command=self.kill_process)
        self.kill_btn.grid(row=0, column=1, padx=5)

        self.suspend_btn = tk.Button(button_frame, text="Suspend", command=self.suspend_process)
        self.suspend_btn.grid(row=0, column=2, padx=5)

        self.resume_btn = tk.Button(button_frame, text="Resume", command=self.resume_process)
        self.resume_btn.grid(row=0, column=3, padx=5)

        # --- AI Suggestions ---
        self.suggestion_label = tk.Label(self.parent, text="AI Suggestions:", font=("Arial", 12, "bold"))
        self.suggestion_label.pack(pady=5)

        self.suggestion_list = tk.Listbox(self.parent, height=5)
        self.suggestion_list.pack(fill='x', padx=10, pady=(0, 10))

        self.refresh_process_list()

    def refresh_process_list(self):
        self.processes = []
        for row in self.proc_tree.get_children():
            self.proc_tree.delete(row)
        self.suggestion_list.delete(0, tk.END)

        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
            try:
                info = proc.info
                pid = info['pid']
                name = info['name']
                cpu = info['cpu_percent']
                mem = info['memory_percent']
                status = info['status']

                proc_tuple = (pid, name, f"{cpu}%", f"{mem}%", status)
                self.processes.append(proc_tuple)
                self.proc_tree.insert('', 'end', values=proc_tuple)

                # Update AI suggestion
                self.recommender.update_activity(pid, cpu)
                recs = self.recommender.get_recommendation(pid, name, cpu, status)
                for rec in recs:
                    self.suggestion_list.insert(tk.END, rec)

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    def update_treeview(self, processes):
        for row in self.proc_tree.get_children():
            self.proc_tree.delete(row)
        for proc in processes:
            self.proc_tree.insert('', 'end', values=proc)

    def on_search(self, event):
        query = self.search_var.get().lower()
        if not query:
            filtered = self.processes
        else:
            filtered = []
            for proc in self.processes:
                pid_str = str(proc[0])
                name = proc[1].lower() if proc[1] else ""
                if query in pid_str or query in name:
                    filtered.append(proc)
        self.update_treeview(filtered)

    def get_selected_pid(self):
        selected = self.proc_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No process selected.")
            return None
        return int(self.proc_tree.item(selected[0])['values'][0])

    def kill_process(self, pid=None):
        pid = pid or self.get_selected_pid()
        if pid is not None:
            try:
                psutil.Process(pid).terminate()
                self.refresh_process_list()
                messagebox.showinfo("Success", f"Process {pid} terminated.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def suspend_process(self, pid=None):
        pid = pid or self.get_selected_pid()
        if pid is not None:
            try:
                psutil.Process(pid).suspend()
                self.refresh_process_list()
                messagebox.showinfo("Success", f"Process {pid} suspended.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def resume_process(self, pid=None):
        pid = pid or self.get_selected_pid()
        if pid is not None:
            try:
                psutil.Process(pid).resume()
                self.refresh_process_list()
                messagebox.showinfo("Success", f"Process {pid} resumed.")
            except Exception as e:
                messagebox.showerror("Error", str(e))
