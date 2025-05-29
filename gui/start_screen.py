import tkinter as tk

class StartScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.columnconfigure(0, weight=1)
        self.rowconfigure((0,1), weight=1)

        label1 = tk.Label(self, text="Witaj w Dual N-Back!", font=("Helvetica", 16))
        label1.grid(row=0, column=0)

        button1=tk.Button(self, text="Dual N-Back", command= lambda: self.controller.show_frame("GameScreen"))
        button1.grid(row=1, column=0)

        self.bind_all("<space>", lambda event: self.controller.show_frame("GameScreen"))

        # Pasek menu
        menu_bar = tk.Menu(controller)
        settings_menu = tk.Menu(menu_bar, tearoff=0)

        size_menu = tk.Menu(settings_menu, tearoff=0)
        # Przykładowe opcje zmiany rozmiaru okna
        size_menu.add_command(label="800x600", command=lambda: controller.set_window_mode("800x600"))
        size_menu.add_command(label="1024x768", command=lambda: controller.set_window_mode("1024x768"))
        size_menu.add_command(label="1920x1080", command=lambda: controller.set_window_mode("1920x1080"))
        size_menu.add_separator()
        size_menu.add_command(label="Fullscreen", command=lambda: controller.toggle_fullscreen())

        menu_bar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_cascade(label="Screen size", menu=size_menu)
        controller.config(menu=menu_bar)


        # Game Mode menu
        game_mode_menu = tk.Menu(menu_bar, tearoff=0)
        game_mode_menu.add_checkbutton(label="Voice", variable=controller.mode_voice)
        game_mode_menu.add_checkbutton(label="Shape", variable=controller.mode_shape)
        game_mode_menu.add_checkbutton(label="Color", variable=controller.mode_color)
        game_mode_menu.add_checkbutton(label="Position", variable=controller.mode_position)

        settings_menu.add_cascade(label="Game Mode", menu=game_mode_menu)

    def toggle_mode(self, mode_name):
        current = getattr(self.controller, f"mode_{mode_name}")
        setattr(self.controller, f"mode_{mode_name}", not current)
