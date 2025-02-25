import tkinter as tk
from tkinter import filedialog
import pygame
import os
import time
from threading import Thread

# Definizione colori
theme_colors = {
    "primary": "#53abd5",
    "text": "#ffffff",
    "accent1": "#ffd5c2",
    "accent2": "#f28f3b",
    "accent3": "#c8553d",
    "opposite1": "#a6cb4e",
    "opposite2": "#cb4ea6"
}


class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Mode Selector")
        self.root.geometry("1920x1080")
        self.root.configure(bg=theme_colors["primary"])

        pygame.mixer.init()

        self.mode = tk.StringVar(value="Back2Back")
        self.timer_value = tk.IntVar(value=30)
        self.volume = tk.DoubleVar(value=0.5)
        self.current_song = ""
        self.next_song = ""
        self.timer_running = False
        self.time_remaining = tk.StringVar(value="")

        self.create_main_menu()

    def create_main_menu(self):
        self.clear_frame()

        tk.Label(self.root, text="Seleziona Modalità", bg=theme_colors["primary"], fg=theme_colors["text"],
                 font=("Arial", 24, "bold")).pack(pady=20)

        button_styles = {"font": ("Arial", 18), "width": 20, "height": 2}
        tk.Button(self.root, text="Back2Back", command=lambda: self.create_mode_screen("Back2Back"),
                  bg=theme_colors["accent1"], fg="black", **button_styles).pack(pady=10)
        tk.Button(self.root, text="Improvvisazione", command=lambda: self.create_mode_screen("Improvvisazione"),
                  bg=theme_colors["accent2"], fg="black", **button_styles).pack(pady=10)
        tk.Button(self.root, text="Intervista", command=lambda: self.create_mode_screen("Intervista"),
                  bg=theme_colors["accent3"], fg="black", **button_styles).pack(pady=10)

    def create_mode_screen(self, mode):
        self.clear_frame()
        self.mode.set(mode)

        tk.Label(self.root, text=f"Modalità: {mode}", bg=theme_colors["primary"], fg=theme_colors["text"],
                 font=("Arial", 24, "bold")).pack(pady=20)
        tk.Button(self.root, text="Seleziona Canzone", command=lambda: self.load_song(1), bg=theme_colors["opposite1"],
                  fg="black", font=("Arial", 18), width=20, height=2).pack(pady=10)

        self.song_label = tk.Label(self.root, text="Nessuna canzone selezionata", bg=theme_colors["primary"],
                                   fg=theme_colors["text"], font=("Arial", 16))
        self.song_label.pack(pady=10)

        if mode == "Back2Back":
            tk.Button(self.root, text="Seleziona Seconda Canzone", command=lambda: self.load_song(2),
                      bg=theme_colors["opposite1"], fg="black", font=("Arial", 18), width=20, height=2).pack(pady=10)
            self.next_song_label = tk.Label(self.root, text="Nessuna seconda canzone selezionata",
                                            bg=theme_colors["primary"], fg=theme_colors["text"], font=("Arial", 16))
            self.next_song_label.pack(pady=10)

        tk.Label(self.root, text="Timer Sirena (sec):", bg=theme_colors["primary"], fg=theme_colors["text"],
                 font=("Arial", 18)).pack()
        self.timer_entry = tk.Entry(self.root, textvariable=self.timer_value, font=("Arial", 18))
        self.timer_entry.pack(pady=5)

        self.timer_display = tk.Label(self.root, textvariable=self.time_remaining, bg=theme_colors["primary"],
                                      fg=theme_colors["text"], font=("Arial", 18, "bold"))
        self.timer_display.pack(pady=5)

        tk.Label(self.root, text="Volume", bg=theme_colors["primary"], fg=theme_colors["text"],
                 font=("Arial", 18)).pack()
        self.volume_slider = tk.Scale(self.root, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL,
                                      variable=self.volume, command=self.set_volume, bg=theme_colors["opposite2"],
                                      fg="black")
        self.volume_slider.pack(pady=10)

        tk.Button(self.root, text="Play", command=self.play_song, bg=theme_colors["opposite1"], fg="black",
                  font=("Arial", 18), width=15, height=2).pack(pady=5)
        tk.Button(self.root, text="Stop", command=self.stop_song, bg=theme_colors["opposite2"], fg="black",
                  font=("Arial", 18), width=15, height=2).pack(pady=5)
        tk.Button(self.root, text="Indietro", command=self.create_main_menu, bg=theme_colors["accent3"], fg="black",
                  font=("Arial", 18), width=15, height=2).pack(pady=20)

    def clear_frame(self):
        pygame.mixer.music.stop()
        for widget in self.root.winfo_children():
            widget.destroy()

    def load_song(self, song_number):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav")])
        if file_path:
            if song_number == 1:
                self.current_song = file_path
                self.song_label.config(text=os.path.basename(file_path))
            else:
                self.next_song = file_path
                self.next_song_label.config(text=os.path.basename(file_path))

    def play_song(self):
        if self.current_song:
            pygame.mixer.music.load(self.current_song)
            pygame.mixer.music.set_volume(self.volume.get())
            pygame.mixer.music.play()
            if self.mode.get() in ["Back2Back", "Improvvisazione", "Intervista"]:
                self.start_timer()

    def stop_song(self):
        pygame.mixer.music.stop()
        self.time_remaining.set("")

    def set_volume(self, _):
        pygame.mixer.music.set_volume(self.volume.get())

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            Thread(target=self.run_timer, daemon=True).start()

    def run_timer(self):
        sec = self.timer_value.get()
        while sec > 0:
            self.time_remaining.set(f"Tempo rimanente: {sec}s")
            time.sleep(1)
            sec -= 1
        self.time_remaining.set("Tempo scaduto!")
        self.timer_running = False


if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()
