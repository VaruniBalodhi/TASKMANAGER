import psutil
import os

class PriorityManager:
    def __init__(self):
        self.enabled = True

    def adjust_priorities(self):
        for proc in psutil.process_iter(['pid', 'cpu_percent', 'name', 'status']):
            try:
                p = psutil.Process(proc.info['pid'])
                cpu = proc.info['cpu_percent']
                status = proc.info['status']

                # Adjust priority based on CPU usage and status
                if cpu > 50:
                    p.nice(psutil.HIGH_PRIORITY_CLASS if os.name == 'nt' else -10)
                elif status == psutil.STATUS_SLEEPING:
                    p.nice(psutil.IDLE_PRIORITY_CLASS if os.name == 'nt' else 19)
                elif "chrome" in proc.info['name'].lower():
                    p.nice(psutil.NORMAL_PRIORITY_CLASS if os.name == 'nt' else 0)

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
