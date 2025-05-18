import tkinter as tk
from tkinter import messagebox

class LoginWindow:
    def __init__(self, master, on_success):
        self.master = master
        self.master.title("Login")
        self.master.geometry("300x180")
        self.on_success = on_success

        tk.Label(master, text="Username").pack(pady=5)
        self.username = tk.Entry(master)
        self.username.pack()

        tk.Label(master, text="Password").pack(pady=5)
        self.password = tk.Entry(master, show="*")
        self.password.pack()

        tk.Button(master, text="Login", command=self.validate).pack(pady=10)

    def validate(self):
        if self.username.get() == "admin" and self.password.get() == "password":
            messagebox.showinfo("Login", "Welcome Admin!")
            self.master.destroy()
            self.on_success()
        else:
            messagebox.showerror("Error", "Invalid credentials")
