import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import os


class GameScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.frame_size = 600
        self.cell_size = self.frame_size // 3
        self.grid_labels =[[],[],[]]

        # Konfiguracja wag: środkowe wiersze i kolumny mogą się skalować
        for i in range(6):
            self.columnconfigure(i, weight=1)
            self.rowconfigure(i, weight=1)

        # Label na górze w komórce (1,2)
        label1 = tk.Label(self, text="Witaj w Dual N-Back!", font=("Helvetica", 16))
        label1.grid(row=1, column=2, columnspan = 2, sticky="nesw", pady=10)

        # Przyciski w (3,1) i (3,3)
        button1 = tk.Button(self, text="voice", command=lambda: self.action())
        button1.grid(row=5, column= 0 , columnspan = 3, sticky="nesw", pady=10)

        button2 = tk.Button(self, text="position", command=lambda: self.action())
        button2.grid(row=5, column=3, columnspan = 3, sticky="nesw", pady=10)

        # Centralny nierozszerzalny Frame (2,2)
        center_frame = tk.Frame(self, width=self.frame_size, height=self.frame_size, bg="white", bd=2, relief="solid")
        center_frame.grid(row=2, column=2, rowspan = 2, columnspan = 2)
        center_frame.grid_propagate(False)
        center_frame.pack_propagate(False)

        #dodanie obrazu
        img_path = os.path.join("resources", "colored-squares", "spr_square_blue.png")
        base_img = Image.open(img_path)
        scaled_img = base_img.resize((int( self.cell_size * 0.8), int( self.cell_size * 0.8)), Image.LANCZOS)
        self.square_img = ImageTk.PhotoImage(scaled_img)



        for i in range(3):
            center_frame.columnconfigure(i, minsize= self.cell_size, weight=0)
            center_frame.rowconfigure(i, minsize= self.cell_size, weight=0)
            for j in range(3):
                lbl = tk.Label(center_frame, bd=1, relief="solid", bg="white")
                lbl.grid(row=i, column=j, padx=0, pady=0, sticky="nsew")
                self.grid_labels[i].append(lbl)
        center_frame.grid_propagate(False)




        lbl_with_image = self.grid_labels[2][2]
        lbl_with_image.configure(image=self.square_img)



    def action(self):
        print("action")




