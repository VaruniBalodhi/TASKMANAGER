import time
import psutil

class ProcessRecommender:
    def __init__(self, cpu_threshold=50, idle_threshold=0.5, idle_duration=60):
        self.cpu_threshold = cpu_threshold
        self.idle_threshold = idle_threshold
        self.idle_duration = idle_duration
        self.last_seen = {}

    def update_activity(self, pid, cpu):
        if cpu > self.idle_threshold:
            self.last_seen[pid] = time.time()

    def get_recommendation(self, pid, name, cpu, status):
        recommendations = []
        now = time.time()

        if cpu > self.cpu_threshold and status == 'running':
            recommendations.append(f"PID {pid} ({name}): High CPU — consider ending.")
        elif cpu <= self.idle_threshold and status == 'running':
            last_active = self.last_seen.get(pid, now)
            if now - last_active > self.idle_duration:
                recommendations.append(f"PID {pid} ({name}): Idle for long — consider suspending.")

        return recommendations
