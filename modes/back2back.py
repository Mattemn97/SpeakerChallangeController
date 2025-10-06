import os
import time
import random
import threading
from player import MusicPlayer

def run(config):
    print(config["COLORS"]["title"] + "\n--- Modalità Back2Back ---")

    # Carica cartella dalle config
    songs_folder = config.get("B2B_FOLDER", "").strip().strip('"').replace("\\", "/")
    if not songs_folder or not os.path.isdir(songs_folder):
        print(config["COLORS"]["warning"] + f"Cartella canzoni back-2-back non valida in config.txt: {songs_folder}\n")
        return

    # Scegli due canzoni casuali
    all_songs = [os.path.join(songs_folder, f) for f in os.listdir(songs_folder) if f.lower().endswith((".mp3", ".wav"))]
    if len(all_songs) < 2:
        print(config["COLORS"]["warning"] + "Servono almeno due file audio nella cartella.\n")
        return

    song1, song2 = random.sample(all_songs, 2)
    print(config["COLORS"]["success"] + f"Canzoni selezionate:\n 1) {os.path.basename(song1)}\n 2) {os.path.basename(song2)}")

    # Timer casuale
    total_duration = config["B2B_TIMER_TOT"]
    half_duration = int(total_duration / 2)
    duration = random.randint(config["B2B_TIMER_MIN"], config["B2B_TIMER_MAX"])
    half_time = int(duration / 2)

    max_audio_duration = half_duration - half_time
    print(config["COLORS"]["success"] + f"Timer impostato a {total_duration}s (cambio a metà: {half_time}s)")

    # Inizializza player
    player = MusicPlayer()

    # --- Prima canzone ---
    player.load_song(song1, 1)
    player.play_song()
    player.set_volume(config["MAX_VOL_AUDIO"])

    for sec in range(max_audio_duration, 0, -1):
        print(config["COLORS"]["timer"] + f"[{os.path.basename(song1)}] Tempo rimanente: {sec}s al {str(config["MAX_VOL_AUDIO"] * 100)}%", end="\r")
        time.sleep(1)
    print("\n")
    player.set_volume(config["MIN_VOL_AUDIO"])
    for sec in range(half_time, 0, -1):
        print(config["COLORS"]["timer"] + f"[{os.path.basename(song1)}] Tempo rimanente: {sec}s al {str(config["MIN_VOL_AUDIO"] * 100)}%", end="\r")
        time.sleep(1)

    print("\n")
    print(config["COLORS"]["warning"] + "Cambio brano!")

    player.load_song(song2, 1)
    player.play_song()
    player.set_volume(config["MIN_VOL_AUDIO"])
    print("\n")
    for sec in range(half_time, 0, -1):
        print(config["COLORS"]["timer"] + f"[{os.path.basename(song2)}] Tempo rimanente: {sec}s al {str(config["MIN_VOL_AUDIO"] * 100)}%", end="\r")
        time.sleep(1)
    print("\n")
    player.set_volume(config["MAX_VOL_AUDIO"])
    for sec in range(max_audio_duration, 0, -1):
        print(config["COLORS"]["timer"] + f"[{os.path.basename(song2)}] Tempo rimanente: {sec}s al {str(config["MAX_VOL_AUDIO"] * 100)}%", end="\r")
        time.sleep(1)

    print("\n" + config["COLORS"]["warning"] + "Stop finale")
    player.stop_song()
    print(config["COLORS"]["success"] + "Back2Back terminato\n")

