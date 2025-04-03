import tkinter as tk
from tkinter import PhotoImage


def show_square(position, image_label, image):
    image_label.image = image
    image_label.grid(row=position[0], column=position[1])


class GameScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.columnconfigure((0,1,2,3,4), weight=1, uniform="1")
        self.rowconfigure((0,1,2,3,4), weight=1, uniform="1")

        label1 = tk.Label(self, text="Witaj w Dual N-Back!", font=("Helvetica", 16))
        label1.grid(row=0, column=2)

        button1=tk.Button(self, text="voice", command= lambda: self.controller.show_frame("MenuScreen"))
        button1.grid(row=4, column=1)

        button2 = tk.Button(self, text="position", command=lambda: self.controller.show_frame("MenuScreen"))
        button2.grid(row=4, column=3)

        image = PhotoImage(file="resources/colored-squares/spr_square_blue.png")
        image_label = tk.Label(self, image=image)
        show_square((2,1), image_label, image)


