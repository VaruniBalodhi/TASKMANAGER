import tkinter as tk
from tkinter import ttk

# Import your modules
from process_management.process_tab import EnhancedProcessTab
from system_monitoring.performance_tab import PerformanceTab, AppHistoryTab
from user_authentication.login import LoginWindow
from user_authentication.alerts import AlertManager
from ai_engine.voice_control import VoiceCommandProcessor
from ai_engine.process_recommender import ProcessRecommender
from ai_engine.priority_manager import PriorityManager

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

    performance_tab_frame = tk.Frame(notebook)
    performance_tab = PerformanceTab(performance_tab_frame)
    notebook.add(performance_tab_frame, text="Performance")

    app_history_tab_frame = tk.Frame(notebook)
    app_history_tab = AppHistoryTab(app_history_tab_frame)
    notebook.add(app_history_tab_frame, text="App History")

    # AI modules
    voice_processor = VoiceCommandProcessor(process_tab)
    recommender = ProcessRecommender()
    priority_manager = PriorityManager()
    alert_manager = AlertManager(root)

    def refresh_all():
        process_tab.refresh_process_list()
        performance_tab.update_metrics()
        app_history_tab.update_history()
        priority_manager.adjust_priorities()

        recommendations = []
        for item in process_tab.proc_tree.get_children():
            pid, name, cpu_str, mem_str, status = process_tab.proc_tree.item(item, 'values')

            try:
                cpu = float(cpu_str.strip('%'))
                mem = float(mem_str.strip(' MB'))  # adjust if your mem format differs

                # Check thresholds and show alerts
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
    login_root = tk.Tk()
    login_app = LoginWindow(login_root, on_success=open_main_app)
    login_root.mainloop()
