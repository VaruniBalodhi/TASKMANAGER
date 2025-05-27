import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

USER_FILE = "user_authentication/users.json"

# Ensure users.json exists with a default user
def load_users():
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w") as f:
            json.dump({
                "admin": {"password": "admin123", "role": "admin"},
                "user": {"password": "user123", "role": "user"}
            }, f)
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

class LoginWindow:
    def __init__(self, master, on_success):
        self.master = master
        self.on_success = on_success
        self.master.title("Login")
        self.master.geometry("350x300")

        tk.Label(master, text="Smart Task Manager", font=("Arial", 14, "bold")).pack(pady=15)

        tk.Label(master, text="Username:").pack()
        self.username_entry = tk.Entry(master)
        self.username_entry.pack()

        tk.Label(master, text="Password:").pack()
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.pack()

        tk.Label(master, text="Role:").pack()
        self.role_combo = ttk.Combobox(master, values=["user", "admin"], state="readonly")
        self.role_combo.current(0)
        self.role_combo.pack()

        tk.Button(master, text="Login", command=self.login).pack(pady=10)
        tk.Button(master, text="Register", command=self.open_register).pack()

        self.users = load_users()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_combo.get()

        user = self.users.get(username)
        if user and user["password"] == password and user["role"] == role:
            messagebox.showinfo("Login Success", f"Welcome {username} ({role})!")
            self.master.destroy()
            self.on_success()
        else:
            messagebox.showerror("Login Failed", "Invalid username, password, or role.")

    def open_register(self):
        register_window = tk.Toplevel(self.master)
        register_window.title("Register")
        register_window.geometry("300x300")

        tk.Label(register_window, text="Register New User", font=("Arial", 12, "bold")).pack(pady=10)

        tk.Label(register_window, text="Username:").pack()
        username_entry = tk.Entry(register_window)
        username_entry.pack()

        tk.Label(register_window, text="Password:").pack()
        password_entry = tk.Entry(register_window, show="*")
        password_entry.pack()

        tk.Label(register_window, text="Role:").pack()
        role_combo = ttk.Combobox(register_window, values=["user", "admin"], state="readonly")
        role_combo.current(0)
        role_combo.pack()

        def register_user():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            role = role_combo.get()

            if not username or not password:
                messagebox.showerror("Error", "Please fill in all fields.")
                return

            if username in self.users:
                messagebox.showerror("Error", "Username already exists.")
            else:
                self.users[username] = {"password": password, "role": role}
                save_users(self.users)
                messagebox.showinfo("Success", f"User '{username}' registered!")
                register_window.destroy()

        tk.Button(register_window, text="Register", command=register_user).pack(pady=15)
