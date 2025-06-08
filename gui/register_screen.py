import tkinter as tk

class RegisterSrcreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Register", font=("Helvetica", 18)).pack(pady=20)

        tk.Label(self, text="Username:").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        tk.Label(self, text="Email:").pack()
        self.email_entry = tk.Entry(self)
        self.email_entry.pack(pady=5)

        tk.Label(self, text="Password:").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self, text="Register", command=self.register).pack(pady=10)
        tk.Button(self, text="Back to Login", command=lambda: controller.show_frame("LoginScreen")).pack()
        tk.Button(self, text="Back to Menu", command=lambda: controller.show_frame("MenuScreen")).pack(pady=20)


    def register(self):
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        print("Registration attempted:", username, email, password)
