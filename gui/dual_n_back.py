import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import os
import random
import pygame
import os

class GameScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.frame_size = 600
        self.cell_size = self.frame_size // 3
        self.grid_labels =[[],[],[]]
        self.sequence = []
        self.turn_index = 0
        self.n_back = 2
        self.turn_time = 3000
        self.running = False
        pygame.mixer.init()

        # Tryby gry domyślne
        self.mode_voice = True
        self.mode_shape = False
        self.mode_color = False
        self.mode_position = True

        # Konfiguracja wag: środkowe wiersze i kolumny mogą się skalować
        for i in range(6):
            self.columnconfigure(i, weight=1)
            self.rowconfigure(i, weight=1)

        # Label na górze w komórce (1,2)
        label1 = tk.Label(self, text="Witaj w Dual N-Back!", font=("Helvetica", 16))
        label1.grid(row=1, column=2, columnspan = 2, sticky="nesw", pady=10)

        # Przyciski w (3,1) i (3,3)
        self.button1 = tk.Button(self, text="voice", command=lambda: self.action())
        self.button1.grid(row=5, column= 0 , columnspan = 3, sticky="nesw", pady=10)

        self.button2 = tk.Button(self, text="position", command=lambda: self.action())
        self.button2.grid(row=5, column=3, columnspan = 3, sticky="nesw", pady=10)

        # Obsługa ESC
        self.bind_all("<Escape>", self.end_game)

        # Centralny nierozszerzalny Frame (2,2)
        center_frame = tk.Frame(self, width=self.frame_size, height=self.frame_size)
        center_frame.grid(row=2, column=2, rowspan = 2, columnspan = 2)
        center_frame.grid_propagate(False)
        center_frame.pack_propagate(False)

        #dodanie obrazu
        img_path = os.path.join("resources", "pictures", "colored-squares", "spr_square_blue.png")
        base_img = Image.open(img_path)
        scaled_img = base_img.resize((int( self.cell_size*0.98 ), int( self.cell_size*0.98 )), Image.LANCZOS)
        self.square_img = ImageTk.PhotoImage(scaled_img)

        for i in range(3):
            center_frame.columnconfigure(i, minsize= self.cell_size*0.99, weight=0)
            center_frame.rowconfigure(i, minsize= self.cell_size*0.99, weight=0)
            for j in range(3):
                lbl = tk.Label(center_frame, relief="solid")
                lbl.grid(row=i, column=j, padx=0, pady=0, sticky="nsew")
                self.grid_labels[i].append(lbl)
        center_frame.grid_propagate(False)



    def start_game(self):
        self.mode_voice = self.controller.mode_voice.get()
        self.mode_shape = self.controller.mode_shape.get()
        self.mode_color = self.controller.mode_color.get()
        self.mode_position = self.controller.mode_position.get()
        self.sequence = []
        self.turn_index = 0
        self.running = True
        self.after(self.turn_time // 2 , self.next_turn)

    def next_turn(self):
        if not self.running:
            return
        row = random.randint(0, 2)
        col = random.randint(0, 2)
        self.sequence.append((row, col))
        self.turn_index += 1

        play_letter("c")
        lbl = self.grid_labels[row][col]
        lbl.configure(image=self.square_img)

        self.after(self.turn_time // 2, lambda: self.end_turn(row, col))


    def end_turn(self, row, col):

        self.grid_labels[row][col].configure(image="")

        if self.turn_index < 3:
            self.after(self.turn_time // 2, self.next_turn)
        else:
            self.after(self.turn_time // 2, self.end_game)

    def reset(self):
        self.running = False
        self.sequence.clear()
        self.turn_index = 0
        for row in self.grid_labels:
            for lbl in row:
                lbl.configure(image="")

    def end_game(self, event=None):
        self.controller.reset_game_screen()
        self.controller.show_frame("StartScreen")

    def action(self):
        print("action")


def play_letter(letter):
    base_path = os.path.dirname(__file__)
    sound_path = os.path.join(base_path, "..", "resources", "sounds", "letters", f"{letter}.wav")
    sound_path = os.path.normpath(sound_path)
    if os.path.exists(sound_path):
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()
    else:
        print("Plik nie istnieje:", sound_path)