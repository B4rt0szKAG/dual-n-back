import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class StatsScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Twoje statystyki", font=("Helvetica", 18)).pack(pady=20)

        # Dane przykładowe
        self.session_numbers = list(range(1, 6))  # Sesje 1 do 5
        self.scores = [2, 4, 3, 5, 4]             # Wyniki punktowe

        # Tworzenie wykresu
        fig, ax = plt.subplots(figsize=(5, 3), dpi=100)
        ax.plot(self.session_numbers, self.scores, marker='o', linestyle='-', color='blue')
        ax.set_title("Postęp gracza")
        ax.set_xlabel("Sesja")
        ax.set_ylabel("Wynik")
        ax.grid(True)

        # Osadzenie wykresu w Tkinterze
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

        # Przycisk powrotu
        tk.Button(self, text="Powrót do menu", command=lambda: controller.show_frame("StartScreen")).pack(pady=10)
