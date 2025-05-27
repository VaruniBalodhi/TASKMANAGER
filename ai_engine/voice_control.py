import speech_recognition as sr
import psutil
import re
import tkinter.messagebox as messagebox

class VoiceCommandProcessor:
    def __init__(self, process_tab):
        self.process_tab = process_tab

    def listen_and_execute(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening for command...")
            messagebox.showinfo("Voice", "Listening for command...")
            try:
                audio = recognizer.listen(source, timeout=5)
                command = recognizer.recognize_google(audio).lower()
                print("Recognized:", command)
                self.process_command(command)
            except sr.UnknownValueError:
                messagebox.showerror("Error", "Could not understand the command.")
            except sr.RequestError:
                messagebox.showerror("Error", "Voice recognition service is unavailable.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def process_command(self, command):
        if "end task for" in command:
            name = command.replace("end task for", "").strip()
            self.terminate_process_by_name(name)
        elif "pause all background tasks" in command:
            self.pause_background_processes()
        elif "resume all tasks" in command:
            self.resume_all_processes()
        else:
            messagebox.showwarning("Unknown", f"Command not recognized: {command}")

    def terminate_process_by_name(self, name):
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'].lower() == name.lower():
                    self.process_tab.kill_process(proc.info['pid'])
                    return
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        messagebox.showinfo("Not Found", f"No process named {name} found.")

    def pause_background_processes(self):
        for proc in psutil.process_iter(['pid', 'name', 'status']):
            try:
                if proc.status() == psutil.STATUS_SLEEPING:
                    proc.suspend()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        self.process_tab.refresh_process_list()
        messagebox.showinfo("Paused", "Background tasks suspended.")

    def resume_all_processes(self):
        for proc in psutil.process_iter(['pid']):
            try:
                proc.resume()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        self.process_tab.refresh_process_list()
        messagebox.showinfo("Resumed", "All tasks resumed.")
