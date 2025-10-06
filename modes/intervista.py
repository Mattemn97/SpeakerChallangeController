import os
import time
from player import MusicPlayer

def run(config):
    print(config["COLORS"]["title"] + "\n--- Modalità Intervista ---")

    # Carica file dalle config
    song = config.get("INTERVISTA_FILE", "").strip().strip('"').replace("\\", "/")
    if not song or not os.path.isfile(song):
        print(config["COLORS"]["warning"] + "File per intervista non valido in config.txt\n")
        return

    duration = config.get("INTERVISTA_DURATION", 30)  # durata in secondi
    print(config["COLORS"]["success"] + f"File intervista: {os.path.basename(song)}")
    print(config["COLORS"]["success"] + f"Durata impostata: {duration}s")

    # Inizializza player
    player = MusicPlayer()

    # Riproduzione a volume massimo
    player.load_song(song)
    player.play_song()    
    player.set_volume(config["MAX_VOL_AUDIO"])
    print(config["COLORS"]["success"] + f"Riproduzione iniziata: {os.path.basename(song)} (volume 100%)")

    for sec in range(10, 0, -1):
        print(config["COLORS"]["timer"] + f"[{os.path.basename(song)}] Tempo rimanente: {sec}s al {str(config["MAX_VOL_AUDIO"] * 100)}%", end="\r")
        time.sleep(1)
    print("\n")

    player.set_volume(config["MIN_VOL_AUDIO"])
    for sec in range(duration, 0, -1):
        print(config["COLORS"]["timer"] + f"[{os.path.basename(song)}] Tempo rimanente: {sec}s al {str(config["MIN_VOL_AUDIO"] * 100)}%", end="\r")
        time.sleep(1)
    print("\n")

    # Stop finale
    player.stop_song()
    print("\n" + config["COLORS"]["success"] + "Riproduzione intervista terminata\n")
