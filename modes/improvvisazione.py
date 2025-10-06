import os
import time
import random
import threading
from player import MusicPlayer 

def run(config):
    print(config["COLORS"]["title"] + "\n--- Modalità Improvvisazione ---")

    # Carica cartella dalle config
    songs_folder = config.get("IMPROV_FOLDER", "").strip().strip('"').replace("\\", "/")
    if not songs_folder or not os.path.isdir(songs_folder):
        print(config["COLORS"]["warning"] + "Cartella canzoni improvvisazione non valida in config.txt\n")
        return

    # Scegli una canzone casuale
    all_songs = [os.path.join(songs_folder, f) for f in os.listdir(songs_folder) if f.lower().endswith((".mp3", ".wav"))]
    if len(all_songs) < 1:
        print(config["COLORS"]["warning"] + "Servono almeno un file audio nella cartella.\n")
        return

    song = random.choice(all_songs)
    print(config["COLORS"]["success"] + f"Canzone selezionata: {os.path.basename(song)}")

    # Inizializza player
    total_duration = config["IMPROV_TIMER_TOT"]
    low_duration = random.randint(config["IMPROV_TIMER_MIN"], config["IMPROV_TIMER_MAX"])
    high_duration = int(total_duration / 2) - int(low_duration / 2)

    print(config["COLORS"]["success"] + f"Timer impostato a {total_duration}s")



    # Inizializza player
    player = MusicPlayer()

    # --- Prima canzone ---
    player.load_song(song, 1)
    player.play_song()
    player.set_volume(config["MAX_VOL_AUDIO"])

    for sec in range(high_duration, 0, -1):
        print(config["COLORS"]["timer"] + f"[{os.path.basename(song)}] Tempo rimanente: {sec}s al {str(config["MAX_VOL_AUDIO"] * 100)}%", end="\r")
        time.sleep(1)
    print("\n")

    player.set_volume(config["MIN_VOL_AUDIO"])
    for sec in range(low_duration, 0, -1):
        print(config["COLORS"]["timer"] + f"[{os.path.basename(song)}] Tempo rimanente: {sec}s al {str(config["MIN_VOL_AUDIO"] * 100)}%", end="\r")
        time.sleep(1)
    print("\n")


    player.set_volume(config["MAX_VOL_AUDIO"])
    for sec in range(high_duration, 0, -1):
        print(config["COLORS"]["timer"] + f"[{os.path.basename(song)}] Tempo rimanente: {sec}s al {str(config["MAX_VOL_AUDIO"] * 100)}%", end="\r")
        time.sleep(1)
    print("\n")

    # --- Stop ---
    player.stop_song()
    print(config["COLORS"]["success"] + "Riproduzione improvvisazione terminata\n")