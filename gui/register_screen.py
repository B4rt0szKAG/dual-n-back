import tkinter as tk
from backend_server.Classes.user import User
from backend_server.client import *
from backend_server.Exceptions.logOutExceptions import NoAuthFile,ErrorlogOut,TokenDoesntExistInDB
class RegisterSrcreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Register", font=("Helvetica", 18)).pack(pady=20)

        tk.Label(self, text="Username:").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        tk.Label(self, text="Name:").pack()
        self.name_entry = tk.Entry(self)
        self.name_entry.pack(pady=5)

        tk.Label(self, text="Last Name:").pack()
        self.LastName_entry = tk.Entry(self)
        self.LastName_entry.pack(pady=5)

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
        name = self.name_entry.get()
        lastname = self.LastName_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()


        tempUser = User(
            username = username,
            name =  name,
            lastname = lastname,
            email = email,
            password = password
        )
        register(tempUser)
        print("Registration attempted:",tempUser.username,tempUser.name,tempUser.lastname,tempUser.email,tempUser.password)
