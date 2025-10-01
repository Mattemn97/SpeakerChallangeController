import os
import time
import random
import threading
from player import MusicPlayer

def run(config):
    print(config["COLORS"]["title"] + "\n--- Modalità Back2Back ---")

    # Carica cartella dalle config
    songs_folder = config.get("B2B_FOLDER", "")
    if not songs_folder or not os.path.isdir(songs_folder):
        print(config["COLORS"]["warning"] + "Cartella canzoni back-2-back non valida in config.txt\n")
        return

    # Scegli due canzoni casuali
    all_songs = [os.path.join(songs_folder, f) for f in os.listdir(songs_folder) if f.lower().endswith((".mp3", ".wav"))]
    if len(all_songs) < 2:
        print(config["COLORS"]["warning"] + "Servono almeno due file audio nella cartella.\n")
        return

    song1, song2 = random.sample(all_songs, 2)
    print(config["COLORS"]["success"] + f"Canzoni selezionate:\n 1) {os.path.basename(song1)}\n 2) {os.path.basename(song2)}")

    # Timer casuale
    duration = random.randint(config["B2B_TIMER_MIN"], config["B2B_TIMER_MAX"])
    half_time = duration // 2
    print(config["COLORS"]["success"] + f"Timer impostato a {duration}s (cambio a metà: {half_time}s)\n")

    # Inizializza player
    player = MusicPlayer()
    player.set_volume(1.0)  # parte a 100%

    def back2back_sequence():
        # Attesa fino a 30s dalla fine
        wait_time = max(0, duration - 30)
        print(config["COLORS"]["timer"] + f"Attendo {wait_time}s prima della prima canzone...")
        time.sleep(wait_time)

        # --- Prima canzone ---
        player.load_song(song1, 1)
        player.play_song()
        print(config["COLORS"]["success"] + f"Riproduzione avviata: {os.path.basename(song1)} (volume 100%)")

        for sec in range(half_time, 0, -1):
            new_vol = max(0.2, sec / half_time)
            player.set_volume(new_vol)
            print(config["COLORS"]["timer"] + f"[{os.path.basename(song1)}] Tempo rimanente: {sec}s Vol: {new_vol:.2f}", end="\r")
            time.sleep(1)

        print("\n" + config["COLORS"]["warning"] + "Cambio brano!")
        player.stop_song()

        # --- Seconda canzone ---
        player.load_song(song2, 2)
        player.play_song()
        player.set_volume(0.2)
        print(config["COLORS"]["success"] + f"Riproduzione avviata: {os.path.basename(song2)} (volume 20%)")

        for sec in range(half_time, 0, -1):
            new_vol = min(1.0, 0.2 + (1.0 - 0.2) * (1 - sec / half_time))
            player.set_volume(new_vol)
            print(config["COLORS"]["timer"] + f"[{os.path.basename(song2)}] Tempo rimanente: {sec}s Vol: {new_vol:.2f}", end="\r")
            time.sleep(1)

        print("\n" + config["COLORS"]["warning"] + "Stop finale")
        player.stop_song()
        print(config["COLORS"]["success"] + "Back2Back terminato\n")

    # Esegue la sequenza in un thread per non bloccare input
    t = threading.Thread(target=back2back_sequence, daemon=True)
    t.start()

    # Comandi interattivi
    while t.is_alive():
        cmd = input("\nComandi: [S]top, [Q]uit → ").strip().lower()
        if cmd == "s":
            player.stop_song()
            print(config["COLORS"]["warning"] + "Riproduzione fermata manualmente")
        elif cmd == "q":
            player.stop_song()
            print(config["COLORS"]["success"] + "Uscita da Back2Back\n")
            break
