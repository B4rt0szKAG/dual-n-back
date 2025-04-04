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
        image_label1 = tk.Label(self, image=image, bd=2, relief="solid")
        image_label2 = tk.Label(self, image=image, bd=2, relief="solid")
        image_label3 = tk.Label(self, image=image, bd=2, relief="solid")
        image_label4 = tk.Label(self, image=image, bd=2, relief="solid")
        image_label5 = tk.Label(self, image=image, bd=2, relief="solid")
        image_label6 = tk.Label(self, image=image, bd=2, relief="solid")
        image_label7 = tk.Label(self, image=image, bd=2, relief="solid")
        image_label8 = tk.Label(self, image=image, bd=2, relief="solid")
        image_label9 = tk.Label(self, image=image, bd=2, relief="solid")
        image_label1.grid(row=1, column=1)
        image_label2.grid(row=1, column=2)
        image_label3.grid(row=1, column=3)
        image_label4.grid(row=2, column=1)
        image_label5.grid(row=2, column=2)
        image_label6.grid(row=2, column=3)
        image_label7.grid(row=3, column=1)
        image_label8.grid(row=3, column=2)
        image_label9.grid(row=3, column=3)
        #show_square((2,1), image_label1, image)


