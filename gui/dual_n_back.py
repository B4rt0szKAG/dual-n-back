import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk, ImageColor
from collections import deque
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
        self.active_images = {}
        self.turn_index = 0
        self.n_back = 2
        self.score=0
        self.turn_time = 3000
        self.running = False
        self.default_button_color = tk.Button(self).cget("background")

        #elementy do losowanie
        self.letters = ('c','h','k', 'l', 'q', 'r', 's', 't')
        self.pentominoes = ('f', 'p', 't', 'u', 'v', 'w', 'x', 'z')
        self.colors = (
            ('blue', (77, 109, 227)),
            ('yellow', (246, 219, 66)),
            ('white', (246, 246, 246)),
            ('red', (227, 88, 75)),
            ('magenta', (204, 75, 227)),
            ('grey', (87, 87, 87)),
            ('green', (134, 227, 82)),
            ('cyan', (65, 244, 241))
        )
        #buffory
        self.voice_queue = deque()
        self.position_queue = deque()
        self.color_queue = deque()
        self.shape_queue = deque()

        # Tryby gry domyślne
        self.mode_voice = True
        self.mode_shape = False
        self.mode_color = False
        self.mode_position = True

        # Aktualny wybor
        self.choice_voice = False
        self.choice_shape = False
        self.choice_color = False
        self.choice_position = False

        # Konfiguracja wag: środkowe wiersze i kolumny mogą się skalować
        pygame.mixer.init()
        for i in range(6):
            self.columnconfigure(i, weight=1)
            self.rowconfigure(i, weight=1)

        # Label na górze w komórce (1,2)
        label1 = tk.Label(self, text="Witaj w Dual N-Back!", font=("Helvetica", 16))
        label1.grid(row=1, column=2, columnspan = 2, sticky="nesw", pady=10)

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
        #inicjalizacja gry

        self.mode_voice = self.controller.mode_voice.get()
        self.mode_shape = self.controller.mode_shape.get()
        self.mode_color = self.controller.mode_color.get()
        self.mode_position = self.controller.mode_position.get()
        self.multiplier = (1 + self.mode_voice) * (1 + self.mode_shape) * (1 + self.mode_color) * (1 + self.mode_position)

        if self.mode_voice:
            self.button1 = tk.Button(self, text="voice", command=self.toggle_voice)
            self.button1.grid(row=5, column=0, columnspan=3, sticky="nesw", pady=10)
        if self.mode_position:
            self.button2 = tk.Button(self, text="position", command=self.toggle_position)
            self.button2.grid(row=5, column=3, columnspan=3, sticky="nesw", pady=10)
        if self.mode_shape:
            self.button3 = tk.Button(self, text="shape", command=self.toggle_shape)
            self.button3.grid(row=4, column=0, columnspan=3, sticky="nesw", pady=10)
        if self.mode_color:
            self.button4 = tk.Button(self, text="color", command=self.toggle_color)
            self.button4.grid(row=4, column=3, columnspan=3, sticky="nesw", pady=10)


        self.sequence = []
        self.turn_index = 0
        self.running = True

        #rozpoczecie gry
        self.after(self.turn_time // 2 , self.next_turn)

    def next_turn(self):
        if not self.running:
            return

        #ustawienia domyslne
        row = 1
        col = 1
        color=self.colors[0]

        if self.mode_voice:
            letter = random.choice(self.letters)
            play_letter(letter)
            self.voice_queue.append(letter)

        if self.mode_position:
            row = random.randint(0, 2)
            col = random.randint(0, 2)
        self.position_queue.append((row, col))

        if self.mode_color:
            color = random.choice(self.colors)
            self.color_queue.append(color[0])

        if self.mode_shape:
            shape=random.choice(self.pentominoes)
            self.show_shape(shape,color[1],row, col)
            self.shape_queue.append(shape)
        else:
            self.show_image(color[0], row, col)


        self.turn_index += 1

        self.after(self.turn_time // 2, lambda: self.end_turn(row, col))


    def end_turn(self, row, col):

        self.grid_labels[row][col].configure(image="")
        self.active_images.pop((row, col), None)
        self.calculating_result()


        if self.turn_index < 6:
            self.after(self.turn_time // 2, self.next_turn)
        else:
            self.after(self.turn_time // 2,lambda: self.end_game())


    def end_game(self, event=None):
        self.controller.reset_game_screen()
        self.controller.show_frame("StartScreen")

    def calculating_result(self):
        flag = self.turn_index > self.n_back

        if self.mode_voice:
            if flag: curr_sol_voice = self.voice_queue.popleft()
            expected = self.voice_queue[-1] if flag else None

            if self.choice_voice:
                if flag and curr_sol_voice == expected:
                    self.flash_button(self.button1, True)
                    self.score += 1
                else:
                    self.flash_button(self.button1, False)
            else:
                self.choice_voice=True
                if flag and curr_sol_voice == expected:
                    self.flash_button(self.button1, False)
                else:
                    self.flash_button(self.button1, True)
                    if flag: self.score += 1
            self.after(self.turn_time // 2, self.toggle_voice)

        if self.mode_shape:
            if flag: curr_sol_shape = self.shape_queue.popleft()
            expected = self.shape_queue[-1] if flag else None

            if self.choice_shape:
                if flag and curr_sol_shape == expected:
                    self.flash_button(self.button3, True)
                    self.score += 1
                else:
                    self.flash_button(self.button3, False)
            else:
                self.choice_shape=True

                if flag and curr_sol_shape == expected:
                    self.flash_button(self.button3, False)
                else:
                    self.flash_button(self.button3, True)
                    if flag: self.score += 1
            self.after(self.turn_time // 2, self.toggle_shape)

        if self.mode_color:
            if flag: curr_sol_color = self.color_queue.popleft()
            expected = self.color_queue[-1] if flag else None

            if self.choice_color:

                if flag and curr_sol_color == expected:
                    self.flash_button(self.button4, True)
                    self.score += 1
                else:
                    self.flash_button(self.button4, False)
            else:
                self.choice_color=True

                if flag and curr_sol_color == expected:
                    self.flash_button(self.button4, False)
                else:
                    self.flash_button(self.button4, True)
                    if flag: self.score += 1
            self.after(self.turn_time // 2, self.toggle_color)

        if self.mode_position:
            if flag: curr_sol_position = self.position_queue.popleft()
            expected = self.position_queue[-1] if flag else None

            if self.choice_position:

                if flag and curr_sol_position == expected:
                    self.flash_button(self.button2, True)
                    self.score += 1
                else:
                    self.flash_button(self.button2, False)
            else:
                self.choice_position=True

                if flag and curr_sol_position == expected:
                    self.flash_button(self.button2, False)
                else:
                    self.flash_button(self.button2, True)
                    if flag: self.score += 1
            self.after(self.turn_time // 2, self.toggle_position)

    def flash_button(self, button, success):
        color = "lightgreen" if success else "red"
        button.config(bg=color)
        self.after(500, lambda: button.config(bg=self.default_button_color))

    def show_shape(self, shape, color_rgb, row, col):
        img_path = os.path.join("resources", "sprites", "pentominoes", f"pento-{shape}.png")

        if not os.path.exists(img_path):
            print(f"Obrazek {img_path} nie istnieje.")
            return

        base_img = Image.open(img_path).convert("RGBA")

        new_data = []
        for pixel in base_img.getdata():
            if pixel[:3] == (255, 255, 255):
                new_data.append((*color_rgb, pixel[3]))
            else:
                new_data.append(pixel)

        base_img.putdata(new_data)
        scaled_img = base_img.resize((int(self.cell_size * 0.98), int(self.cell_size * 0.98)), Image.LANCZOS)

        sprite_img = ImageTk.PhotoImage(scaled_img)

        self.grid_labels[row][col].configure(image=sprite_img)
        self.active_images[(row, col)] = sprite_img

    def show_image(self, color, row, col):
        img_path = os.path.join("resources", "pictures", "colored-squares", f"spr_square_{color}.png")
        base_img = Image.open(img_path)
        scaled_img = base_img.resize((int(self.cell_size * 0.98), int(self.cell_size * 0.98)), Image.LANCZOS)
        square_img = ImageTk.PhotoImage(scaled_img)

        self.grid_labels[row][col].configure(image=square_img)
        self.active_images[(row, col)] = square_img

    def toggle_voice(self):
        self.choice_voice = not self.choice_voice
        self.button1.config(bg="white" if self.choice_voice else self.default_button_color)

    def toggle_position(self):
        self.choice_position = not self.choice_position
        self.button2.config(bg="white" if self.choice_position else self.default_button_color)

    def toggle_shape(self):
        self.choice_shape = not self.choice_shape
        self.button3.config(bg="white" if self.choice_shape else self.default_button_color)

    def toggle_color(self):
        self.choice_color = not self.choice_color
        self.button4.config(bg="white" if self.choice_color else self.default_button_color)


def play_letter(letter):
    base_path = os.path.dirname(__file__)
    sound_path = os.path.join(base_path, "..", "resources", "sounds", "letters", f"{letter}.wav")
    sound_path = os.path.normpath(sound_path)
    if os.path.exists(sound_path):
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()
    else:
        print("Plik nie istnieje:", sound_path)