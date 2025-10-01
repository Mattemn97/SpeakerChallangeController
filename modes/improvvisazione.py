import os
import time
import random
import threading
from player import MusicPlayer 

def run(config):
    print(config["COLORS"]["title"] + "\n--- Modalità Improvvisazione ---")

    # Carica cartella dalle config
    songs_folder = config.get("IMPROV_FOLDER", "")
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
    player = MusicPlayer()
    player.set_volume(1.0)

    # Tempo casuale per volume basso
    low_duration = random.randint(config["IMPROV_TIMER_MIN"], config["IMPROV_TIMER_MAX"])
    print(config["COLORS"]["success"] + f"Volume basso per {low_duration}s")

    def improv_sequence():
        # --- Inizio a volume massimo 10s ---
        player.load_song(song)
        player.play_song()
        player.set_volume(1.0)
        print(config["COLORS"]["success"] + f"Riproduzione iniziata: {os.path.basename(song)} (volume 100%)")
        time.sleep(10)

        # --- Volume basso ---
        player.set_volume(0.2)
        print(config["COLORS"]["warning"] + f"Volume abbassato al 20% per {low_duration}s")
        for sec in range(low_duration, 0, -1):
            print(config["COLORS"]["timer"] + f"Tempo rimanente a volume basso: {sec}s", end="\r")
            time.sleep(1)

        # --- Volume massimo finale 10s ---
        player.set_volume(1.0)
        print(config["COLORS"]["success"] + "\nVolume massimo finale per 10s")
        time.sleep(10)

        # --- Stop ---
        player.stop_song()
        print(config["COLORS"]["success"] + "Riproduzione improvvisazione terminata\n")

    # Esegue la sequenza in un thread
    t = threading.Thread(target=improv_sequence, daemon=True)
    t.start()

    # Comandi interattivi
    while t.is_alive():
        cmd = input("\nComandi: [S]top, [Q]uit → ").strip().lower()
        if cmd == "s":
            player.stop_song()
            print(config["COLORS"]["warning"] + "Riproduzione fermata manualmente")
        elif cmd == "q":
            player.stop_song()
            print(config["COLORS"]["success"] + "Uscita da Improvvisazione\n")
            break
