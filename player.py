import pygame
import os
from contextlib import redirect_stdout

class MusicPlayer:
    def __init__(self):
        with open(os.devnull, "w") as f, redirect_stdout(f):
            pygame.mixer.init()
        self.current_song = None

    def load_song(self, path, _id=0):
        """Carica il file audio"""
        if not os.path.isfile(path):
            raise FileNotFoundError(f"File non trovato: {path}")
        self.current_song = path
        pygame.mixer.music.load(path)

    def play_song(self):
        """Avvia la riproduzione"""
        if self.current_song is None:
            raise RuntimeError("Nessuna canzone caricata")
        pygame.mixer.music.play()

    def stop_song(self):
        """Ferma la riproduzione"""
        pygame.mixer.music.stop()

    def set_volume(self, volume: float):
        """Imposta il volume da 0.0 a 1.0"""
        volume = max(0.0, min(1.0, volume))  # limita tra 0 e 1
        pygame.mixer.music.set_volume(volume)
