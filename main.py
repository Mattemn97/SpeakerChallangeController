import os
import time
import random
import colorama
import pygame
from contextlib import redirect_stdout

colorama.init(autoreset=True)

COLOR_MAP = {
    "black": colorama.Fore.BLACK,
    "red": colorama.Fore.RED,
    "green": colorama.Fore.GREEN,
    "yellow": colorama.Fore.YELLOW,
    "blue": colorama.Fore.BLUE,
    "magenta": colorama.Fore.MAGENTA,
    "cyan": colorama.Fore.CYAN,
    "white": colorama.Fore.WHITE,
}

def formatta_tempo(secondi: int):
    secondi = max(0, int(secondi))
    minuti = secondi // 60
    secondi_restanti = secondi % 60
    return f"{minuti:02d}:{secondi_restanti:02d}"

def nome_file(percorso: str):
    return os.path.basename(percorso).replace(".mp3", "")

def load_config(file_path="config.txt"):
    config = {"COLORS": {}}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for num, line in enumerate(f, start=1):
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                key, value = line.split("=", 1)
                key, value = key.strip(), value.strip()

                try:
                    if key.startswith("COLOR_"):
                        config["COLORS"][key.replace("COLOR_", "").lower()] = COLOR_MAP.get(value.lower(), "")
                    elif key.endswith("VOL_AUDIO"):
                        config[key] = float(value)
                    elif key.endswith("FOLDER") or key.endswith("PATH"):
                        config[key] = str(value.strip().strip('"').replace("\\", "/"))
                    else:
                        config[key] = int(value)

                except ValueError:
                    print(COLOR_MAP.get("red") +
                          f"Valore non valido nel config alla riga {num}\n")

    except FileNotFoundError:
        print(COLOR_MAP.get("red") +
              "File config.txt non trovato\n")

    except PermissionError:
        print(COLOR_MAP.get("red") +
              "Permessi insufficienti per leggere config.txt\n")

    return config

def estrai_news_casuale(config, file_path="news.txt"):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            righe = [r.strip() for r in f if r.strip()]

        if not righe:
            print(config["COLORS"]["warning"] +
                  "Nessuna news disponibile\n")
            return None

        scelta = random.choice(righe)
        righe.remove(scelta)

        with open(file_path, "w", encoding="utf-8") as f:
            for r in righe:
                f.write(r + "\n")

        return scelta

    except FileNotFoundError:
        print(config["COLORS"]["warning"] +
              "File news.txt non trovato\n")
        return None

class MusicPlayer:
    def __init__(self, config):
        self.config = config
        self.current_song = None
        try:
            pygame.mixer.init()
        except pygame.error:
            print(config["COLORS"]["warning"] +
                  "Errore inizializzazione audio\n")

    def load_song(self, path):
        if not os.path.isfile(path):
            print(self.config["COLORS"]["warning"] +
                  "File audio non trovato\n")
            return False

        try:
            pygame.mixer.music.load(path)
            self.current_song = path
            return True
        except pygame.error:
            print(self.config["COLORS"]["warning"] +
                  "Errore caricamento file audio\n")
            return False

    def play_song(self):
        try:
            pygame.mixer.music.play()
        except pygame.error:
            print(self.config["COLORS"]["warning"] +
                  "Errore durante la riproduzione audio\n")

    def set_volume(self, volume: float):
        volume = max(0.0, min(1.0, volume))  # limita tra 0 e 1
        pygame.mixer.music.set_volume(volume)

    def stop_song(self):
        pygame.mixer.music.stop()

# ==================================================
# MODALITÀ INTERVISTA
# ==================================================
def run_intervista(config):
    print(config["COLORS"]["mode"] + "\n--- Modalità Intervista ---")

    folder = config.get("INTERVISTA_FOLDER", "").strip().strip('"').replace("\\", "/")
    if not os.path.isdir(folder):
        print(config["COLORS"]["warning"] + "Cartella intervista non valida\n")
        return

    songs = [os.path.join(folder, f) for f in os.listdir(folder)
             if f.lower().endswith((".mp3", ".wav"))]

    if not songs:
        print(config["COLORS"]["warning"] + "Nessuna canzone trovata\n")
        return

    duration = config.get("INTERVISTA_TIMER_TOT", 30)

    song = random.choice(songs)
    print(config["COLORS"]["canzone"] + f"CANZONE RIPRODOTTA: {nome_file(song)}")

    player = MusicPlayer(config)
    player.load_song(song)
    player.play_song()
    player.set_volume(config["MAX_VOL_AUDIO"])

    for sec in range(15, 0, -1):
        print(config["COLORS"]["inizio"] + f"INIZIO PROVA:  {formatta_tempo(sec)}", end="\r")
        time.sleep(1)

    player.set_volume(config["MIN_VOL_AUDIO"])
    print(" ")

    for sec in range(duration, 0, -1):
        print(config["COLORS"]["termine"] + f"TERMINE PROVA: {formatta_tempo(sec)}", end="\r")
        time.sleep(1)
    
    player.set_volume(config["MAX_VOL_AUDIO"])
    player.load_song(config["GONG_PATH"])
    player.play_song()
    time.sleep(5)

    player.stop_song()
    print("\n" + config["COLORS"]["mode"] + "Intervista terminata\n")


# ==================================================
# MODALITÀ IMPROVVISAZIONE
# ==================================================
def run_improvvisazione(config):
    print(config["COLORS"]["mode"] + "\n--- Modalità Improvvisazione ---")

    folder = config.get("IMPROVVISAZIONE_FOLDER", "").strip().strip('"').replace("\\", "/")
    if not os.path.isdir(folder):
        print(config["COLORS"]["warning"] + "Cartella improvvisazione non valida\n")
        return

    songs = [os.path.join(folder, f) for f in os.listdir(folder)
             if f.lower().endswith((".mp3", ".wav"))]

    if not songs:
        print(config["COLORS"]["warning"] + "Nessuna canzone trovata\n")
        return

    duration = config.get("IMPROVVISAZIONE_TIMER_TOT", 60)
    sec_news = random.randint(config["IMPROVVISAZIONE_TIMER_MIN"], config["IMPROVVISAZIONE_TIMER_MAX"])

    song = random.choice(songs)
    print(config["COLORS"]["canzone"] + f"CANZONE RIPRODOTTA: {nome_file(song)}")

    player = MusicPlayer(config)
    player.load_song(song)
    player.play_song()

    player.set_volume(config["MAX_VOL_AUDIO"])

    for sec in range(15, 0, -1):
        if sec == 0:
            print(" "*50, end="\r")
            time.sleep(0.1)
        else:
            print(config["COLORS"]["inizio"] + f"INIZIO PROVA: {formatta_tempo(sec)}", end="\r")
            time.sleep(1)
    
    player.set_volume(config["MIN_VOL_AUDIO"])

    for sec in range(duration, -1, -1):
        if sec == 0:
            print(" "*50, end="\r")
            time.sleep(0.1)
        elif sec == sec_news:
            print(config["COLORS"]["news"] + f"BREAKING NEWS: {estrai_news_casuale(config)}")
        else:
            print(config["COLORS"]["termine"] + f"TERMINE PROVA: {formatta_tempo(sec)}", end="\r")
            time.sleep(1)
    
    player.set_volume(config["MAX_VOL_AUDIO"])
    player.load_song(config["GONG_PATH"])
    player.play_song()
    time.sleep(5)

    player.stop_song()
    print("\n" + config["COLORS"]["mode"] + "Improvvisazione terminata\n")


# ==================================================
# MODALITÀ BACK2BACK
# ==================================================
def run_back2back(config):
    print(config["COLORS"]["mode"] + "\n--- Modalità Back2Back ---")

    folder = config.get("BACK2BACK_FOLDER", "").strip().strip('"').replace("\\", "/")
    if not os.path.isdir(folder):
        print(config["COLORS"]["warning"] + "Cartella Back2Back non valida\n")
        return

    songs = [os.path.join(folder, f) for f in os.listdir(folder)
             if f.lower().endswith((".mp3", ".wav"))]

    song1, song2 = random.sample(songs, 2)
    print(config["COLORS"]["canzone"] + f"CANZONE ATTUALE: {nome_file(song1)}")
    print(config["COLORS"]["canzone"] + f"CANZONE SUCCESSIVA: {nome_file(song2)}")

    total = config["BACK2BACK_TIMER_TOT"]
    duration = random.randint(config["BACK2BACK_TIMER_LOW_MIN"], config["BACK2BACK_TIMER_LOW_MAX"])
    half = duration // 2
    max_audio = (total // 2) - half

    player = MusicPlayer(config)
    player.load_song(song1)
    player.play_song()
    player.set_volume(config["MAX_VOL_AUDIO"])

    for sec in range(max_audio, -1, -1):
        if sec == 0:
            print(" "*50, end="\r")
            time.sleep(0.1)
        else:
            print(config["COLORS"]["inizio"] + f"INIZIO PROVA: {formatta_tempo(sec)}", end="\r")
            time.sleep(1)

    player.set_volume(config["MIN_VOL_AUDIO"])
    for sec in range(half, -1, -1):
        if sec == 0:
            print(" "*50, end="\r")
            time.sleep(0.1)
        else:
            print(config["COLORS"]["cambio"] + f"CAMBIO BRANO: {formatta_tempo(sec)}", end="\r")
            time.sleep(1)

    player.load_song(song2)
    player.play_song()

    for sec in range(half, -1, -1):
        if sec == 0:
            print(" "*50, end="\r")
            time.sleep(0.1)
        else:
            print(config["COLORS"]["termine"] + f"TERMINE PROVA: {formatta_tempo(sec)}", end="\r")
            time.sleep(1)
    
    player.set_volume(config["MAX_VOL_AUDIO"])
    player.load_song(config["GONG_PATH"])
    player.play_song()
    time.sleep(5)

    player.stop_song()
    print(config["COLORS"]["mode"] + "Back2Back terminato\n")


CONFIG = load_config()

def main_menu():
    while True:
        print(CONFIG["COLORS"]["mode"] + "\n=== SPEAKER CHALLENGE TERMINAL ===")
        print(CONFIG["COLORS"]["menu"] + "[1] Back2Back")
        print(CONFIG["COLORS"]["menu"] + "[2] Improvvisazione")
        print(CONFIG["COLORS"]["menu"] + "[3] Intervista")
        print(CONFIG["COLORS"]["menu"] + "[Q] Esci")

        choice = input("Scelta: ").strip().lower()

        if choice == "1":
            run_back2back(CONFIG)
        elif choice == "2":
            run_improvvisazione(CONFIG)
        elif choice == "3":
            run_intervista(CONFIG)
        elif choice == "q":
            print(CONFIG["COLORS"]["mode"] + "Ciao!")
            break
        else:
            print(CONFIG["COLORS"]["warning"] + "Scelta non valida\n")

if __name__ == "__main__":
    main_menu()
