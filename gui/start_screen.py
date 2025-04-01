import tkinter as tk

class StartScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.columnconfigure(0, weight=1)
        self.rowconfigure((0,1), weight=1)

        label1 = tk.Label(self, text="Witaj w Dual N-Back!", font=("Helvetica", 16))
        label1.grid(row=0, column=0)

        button1=tk.Button(self, text="Przejdź do menu", command= lambda: self.controller.show_frame("MenuScreen"))
        button1.grid(row=1, column=0)
