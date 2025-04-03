import tkinter as tk
from gui.start_screen import StartScreen
from gui.menu_screen import MenuScreen
from gui.dual_n_back import GameScreen

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dual N-Back")
        self.geometry("400x300")
        self.frames = {}

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        for F in (StartScreen, MenuScreen, GameScreen):
            frame = F(parent=container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartScreen")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()