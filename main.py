import tkinter as tk
from tkinter import ttk, messagebox
import psutil

# ----- Your EnhancedProcessTab -----
class EnhancedProcessTab:
    def __init__(self, parent):
        self.parent = parent
        self.processes = []
        self.proc_tree = None
        self.search_var = tk.StringVar()
        self.setup_process_management_ui()

    def setup_process_management_ui(self):
        # Search bar
        search_frame = tk.Frame(self.parent)
        search_frame.pack(fill='x', padx=10, pady=(10, 0))

        tk.Label(search_frame, text="Search:").pack(side='left')
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side='left', fill='x', expand=True, padx=5)
        self.search_entry.bind('<KeyRelease>', self.on_search)

        # Treeview
        self.proc_tree = ttk.Treeview(self.parent, columns=('PID', 'Name', 'CPU', 'Memory', 'Status'), show='headings')
        for col in self.proc_tree["columns"]:
            self.proc_tree.heading(col, text=col)
            self.proc_tree.column(col, width=120)
        self.proc_tree.pack(fill='both', expand=True, padx=10, pady=10)

        # Refresh button
        btn_frame = tk.Frame(self.parent)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Refresh", command=self.refresh_process_list).pack(side='left', padx=5)

        self.refresh_process_list()

    def refresh_process_list(self):
        self.processes.clear()
        for row in self.proc_tree.get_children():
            self.proc_tree.delete(row)

        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
            try:
                info = proc.info
                proc_tuple = (
                    info['pid'],
                    info['name'],
                    f"{info['cpu_percent']:.1f}%",
                    f"{info['memory_percent']:.2f}%",
                    info['status']
                )
                self.processes.append(proc_tuple)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        for proc in self.processes:
            self.proc_tree.insert('', 'end', values=proc)

    def get_selected_pid(self):
        selected = self.proc_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No process selected.")
            return None
        return int(self.proc_tree.item(selected[0])['values'][0])

# ----- Stub AI Modules -----
class VoiceCommandProcessor:
    def __init__(self, process_tab):
        self.process_tab = process_tab
        self.active = False

    def start(self):
        self.active = True
        print("Voice control started")

    def stop(self):
        self.active = False
        print("Voice control stopped")

class ProcessRecommender:
    def get_recommendation(self, pid, name, cpu, status):
        # For demo, recommend killing high CPU processes
        if cpu > 50:
            return [f"Consider stopping process {name} (PID {pid}) - high CPU usage {cpu}%"]
        return []

    def update_activity(self, pid, cpu):
        pass

    def run_once(self):
        # Demo recommendations
        return ["Recommendation: Monitor CPU usage", "Recommendation: Optimize memory usage"]

class PriorityManager:
    def adjust_priorities(self):
        print("Adjusting process priorities")

class AlertManager:
    def __init__(self, root):
        self.root = root

    def check_and_alert(self, pid, name, cpu, mem):
        # Dummy alert: if CPU > 80%, alert
        if cpu > 80:
            self.show_alert(f"High CPU usage detected: {name} (PID {pid}) at {cpu}%")

    def show_alert(self, message):
        messagebox.showwarning("Alert", message)

# ----- Main Application -----
def open_main_app():
    root = tk.Tk()
    root.title("Smart Task Manager")
    root.geometry("1000x700")

    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)

    # Tabs
    process_tab_frame = tk.Frame(notebook)
    process_tab = EnhancedProcessTab(process_tab_frame)
    notebook.add(process_tab_frame, text="Processes")

    performance_tab_frame = tk.Frame(notebook)  # Stub frame for demo
    notebook.add(performance_tab_frame, text="Performance")

    app_history_tab_frame = tk.Frame(notebook)  # Stub frame for demo
    notebook.add(app_history_tab_frame, text="App History")

    # AI modules
    voice_processor = VoiceCommandProcessor(process_tab)
    recommender = ProcessRecommender()
    priority_manager = PriorityManager()
    alert_manager = AlertManager(root)

    # AI Control Tab
    ai_tab_frame = tk.Frame(notebook)
    notebook.add(ai_tab_frame, text="AI Control")

    def toggle_voice_control():
        if voice_processor.active:
            voice_processor.stop()
            voice_btn.config(text="Start Voice Control")
        else:
            voice_processor.start()
            voice_btn.config(text="Stop Voice Control")

    def run_recommender():
        recs = recommender.run_once()
        messagebox.showinfo("Recommendations", "\n".join(recs))

    def adjust_priorities():
        priority_manager.adjust_priorities()
        messagebox.showinfo("Priority Manager", "Priorities adjusted.")

    voice_btn = tk.Button(ai_tab_frame, text="Start Voice Control", command=toggle_voice_control)
    voice_btn.pack(pady=10, padx=10, fill='x')

    recommender_btn = tk.Button(ai_tab_frame, text="Run Recommender", command=run_recommender)
    recommender_btn.pack(pady=10, padx=10, fill='x')

    priority_btn = tk.Button(ai_tab_frame, text="Adjust Priorities", command=adjust_priorities)
    priority_btn.pack(pady=10, padx=10, fill='x')

    # Refresh loop
    def refresh_all():
        process_tab.refresh_process_list()

        # Example simple alert and recommendations scanning all processes in treeview
        recommendations = []
        for item in process_tab.proc_tree.get_children():
            pid, name, cpu_str, mem_str, status = process_tab.proc_tree.item(item, 'values')
            try:
                cpu = float(cpu_str.strip('%'))
                mem = float(mem_str.strip('%'))
                alert_manager.check_and_alert(int(pid), name, cpu, mem)
                recs = recommender.get_recommendation(int(pid), name, cpu, status)
                recommendations.extend(recs)
                recommender.update_activity(int(pid), cpu)
            except Exception:
                continue

        if recommendations:
            alert_manager.show_alert("\n".join(recommendations))

        root.after(5000, refresh_all)

    refresh_all()
    root.mainloop()

if __name__ == "__main__":
    open_main_app()
