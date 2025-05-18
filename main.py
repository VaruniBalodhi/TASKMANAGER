import tkinter as tk
from tkinter import ttk
from process_management.process_tab import EnhancedProcessTab
from system_monitoring.performance_tab import PerformanceTab, AppHistoryTab
from user_authentication.login import LoginWindow

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Task Manager")
        self.root.geometry("1200x700")

        self.tabs = ttk.Notebook(root)
        self.proc_tab = ttk.Frame(self.tabs)
        self.perf_tab = ttk.Frame(self.tabs)
        self.hist_tab = ttk.Frame(self.tabs)

        self.tabs.add(self.proc_tab, text="Processes")
        self.tabs.add(self.perf_tab, text="Performance")
        self.tabs.add(self.hist_tab, text="App History")
        self.tabs.pack(expand=True, fill="both")

        self.process_tab = EnhancedProcessTab(self.proc_tab)
        self.performance_tab = PerformanceTab(self.perf_tab)
        self.history_tab = AppHistoryTab(self.hist_tab)

def launch_task_manager():
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    login_root = tk.Tk()
    LoginWindow(login_root, launch_task_manager)
    login_root.mainloop()
