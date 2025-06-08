import tkinter as tk
from backend_server.client import *
class LoginScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Login", font=("Helvetica", 18)).pack(pady=20)

        tk.Label(self, text="Username:").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        tk.Label(self, text="Password:").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self, text="Login", command=self.login).pack(pady=10)

        tk.Label(self, text="If you are not registered, register below!").pack(pady=5)
        tk.Button(self, text="Register", command=lambda: controller.show_frame("RegisterSrcreen")).pack()

        tk.Button(self, text="Back to Menu", command=lambda: controller.show_frame("MenuScreen")).pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        logIn(username,password)