import tkinter as tk

class MenuScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.columnconfigure(0, weight=1)
        self.rowconfigure((0,1,2), weight=1)

        label1=tk.Label(self, text="To jest menu", font=("Helvetica", 14))
        label1.grid(row=0, column=0, sticky="nsew")

        button1=tk.Button(self, text="Dual n-back!", command= lambda: self.controller.show_frame("GameScreen"))
        button1.grid(row=1, column=0)

        button2=tk.Button(self, text="Powrót", command = lambda: self.controller.show_frame("StartScreen") )
        button2.grid(row=2, column=0)
