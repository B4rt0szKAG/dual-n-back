import tkinter as tk

class StartScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.columnconfigure(0, weight=1)
        self.rowconfigure((0,1), weight=1)

        label1 = tk.Label(self, text=f"Witaj w Dual {controller.n_back}-Back!", font=("Helvetica", 16))
        label1.grid(row=0, column=0)

        button1=tk.Button(self, text="Dual N-Back", command= lambda: self.controller.show_frame("GameScreen"))
        button1.grid(row=1, column=0)

        #bindowanie
        self.bind_all("<space>", lambda event: self.controller.show_frame("GameScreen"))

        # Pasek menu
        menu_bar = tk.Menu(controller)

        # Opcja logowania
        menu_bar.add_command(label="Login", command=lambda: controller.logIn())

        # Opcja Wylogowania
        menu_bar.add_command(label="Logout", command=lambda: controller.logout())



        # Opcja statystyk
        menu_bar.add_command(label="Statistics", command=lambda: controller.show_frame("StatsScreen"))

        # Tryb gry
        game_mode_menu = tk.Menu(menu_bar, tearoff=0)
        game_mode_menu.add_checkbutton(label="Voice", variable=controller.mode_voice)
        game_mode_menu.add_checkbutton(label="Shape", variable=controller.mode_shape)
        game_mode_menu.add_checkbutton(label="Color", variable=controller.mode_color)
        game_mode_menu.add_checkbutton(label="Position", variable=controller.mode_position)

        menu_bar.add_cascade(label="Game Mode", menu=game_mode_menu)

        # Opcja czasu
        time_menu = tk.Menu(menu_bar, tearoff=0)
        time_menu.add_checkbutton(label="(2x)", variable=controller.set_time(2))
        time_menu.add_checkbutton(label="(4x)", variable=controller.set_time(4))
        time_menu.add_checkbutton(label="(8x)", variable=controller.set_time(8))
        time_menu.add_checkbutton(label="(16x)", variable=controller.set_time(16))
        time_menu.add_checkbutton(label="(32x)", variable=controller.set_time(32))
        menu_bar.add_cascade(label="Time", menu=time_menu)

        # Opcja n-back
        time_menu = tk.Menu(menu_bar, tearoff=0)
        time_menu.add_command(label="(1)", command=lambda: self.set_n_back_start(1, label1))
        time_menu.add_command(label="(2)", command=lambda: self.set_n_back_start(2, label1))
        time_menu.add_command(label="(3)", command=lambda: self.set_n_back_start(3, label1))
        time_menu.add_command(label="(4)", command=lambda: self.set_n_back_start(4, label1))
        time_menu.add_command(label="(5)", command=lambda: self.set_n_back_start(5, label1))
        time_menu.add_command(label="(6)", command=lambda: self.set_n_back_start(6, label1))
        time_menu.add_command(label="(7)", command=lambda: self.set_n_back_start(7, label1))
        time_menu.add_command(label="(8)", command=lambda: self.set_n_back_start(8, label1))
        menu_bar.add_cascade(label="N-back", menu=time_menu)

        # rozmiar okna
        size_menu = tk.Menu(menu_bar, tearoff=0)
        size_menu.add_command(label="1024x768", command=lambda: controller.set_window_mode("1024x768"))
        size_menu.add_command(label="1440x900", command=lambda: controller.set_window_mode("1440x900"))
        size_menu.add_command(label="1920x1080", command=lambda: controller.set_window_mode("1920x1080"))
        size_menu.add_separator()
        size_menu.add_command(label="Fullscreen", command=lambda: controller.toggle_fullscreen())

        menu_bar.add_cascade(label="Screen size", menu=size_menu)
        controller.config(menu=menu_bar)

    def toggle_mode(self, mode_name):
        current = getattr(self.controller, f"mode_{mode_name}")
        setattr(self.controller, f"mode_{mode_name}", not current)

    def set_rounds(self):
        try:
            value = int(self.rounds_var.get())
            if value < 1:
                raise ValueError
            self.controller.rounds.set(value)
            print(f"Ustawiono liczbę rund na: {value}")
        except ValueError:
            tk.messagebox.showerror("Błąd", "Podaj poprawną liczbę naturalną większą od zera.")

    def set_n_back_start(self, n_back, label):
        self.controller.set_n_back(n_back)
        label.config(text=f"Witaj w Dual {n_back}-Back!")
