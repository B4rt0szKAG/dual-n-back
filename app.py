import tkinter as tk
from gui.start_screen import StartScreen
from gui.menu_screen import MenuScreen
from gui.dual_n_back import GameScreen
from gui.login_screen import LoginScreen
from gui.register_screen import RegisterSrcreen

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self._fullscreen = False
        self.title("Dual N-Back")
        self._geometry = "1024x768"
        self.geometry(self._geometry)
        self.frames = {}
        self.container = tk.Frame(self)
        self.resizable(False, False)

        # Tryby gry
        self.mode_voice = tk.BooleanVar(value=True)
        self.mode_shape = tk.BooleanVar(value=False)
        self.mode_color = tk.BooleanVar(value=False)
        self.mode_position = tk.BooleanVar(value=True)

        self.container.pack(fill="both", expand=True)

        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)

        for F in (StartScreen, GameScreen, LoginScreen, RegisterSrcreen, MenuScreen):
            frame = F(parent=self.container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartScreen")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

        if name == "GameScreen":
            frame.start_game()

        
    def set_window_mode(self, new_geometry):
        if self._fullscreen:
            self._fullscreen = False
            self.attributes("-fullscreen", False)
        self.geometry(new_geometry)

    def toggle_fullscreen(self):
        self._fullscreen = not self._fullscreen
        self.attributes("-fullscreen", self._fullscreen)
        if not self._fullscreen:
            self.geometry(self._geometry)


    def reset_game_screen(self):
        self.frames["GameScreen"].destroy()
        new_frame = GameScreen(parent=self.container, controller=self)
        self.frames["GameScreen"] = new_frame
        new_frame.grid(row=0, column=0, sticky="nsew")

    def logout(self):
        print("wylogowanie")