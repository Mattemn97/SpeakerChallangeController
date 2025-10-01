import os
import time
import threading
from player import MusicPlayer

def run(config):
    print(config["COLORS"]["title"] + "\n--- Modalità Intervista ---")

    # Carica file dalle config
    song_path = config.get("INTERVISTA_FILE", "")
    if not song_path or not os.path.isfile(song_path):
        print(config["COLORS"]["warning"] + "File per intervista non valido in config.txt\n")
        return

    duration = config.get("INTERVISTA_DURATION", 30)  # durata in secondi
    print(config["COLORS"]["success"] + f"File intervista: {os.path.basename(song_path)}")
    print(config["COLORS"]["success"] + f"Durata impostata: {duration}s")

    # Inizializza player
    player = MusicPlayer()
    player.set_volume(1.0)

    def interview_sequence():
        # Riproduzione a volume massimo
        player.load_song(song_path)
        player.play_song()
        player.set_volume(1.0)
        print(config["COLORS"]["success"] + f"Riproduzione iniziata: {os.path.basename(song_path)} (volume 100%)")

        # Timer della durata
        for sec in range(duration, 0, -1):
            print(config["COLORS"]["timer"] + f"Tempo rimanente: {sec}s", end="\r")
            time.sleep(1)

        # Stop finale
        player.stop_song()
        print("\n" + config["COLORS"]["success"] + "Riproduzione intervista terminata\n")

    # Esegue la sequenza in un thread
    t = threading.Thread(target=interview_sequence, daemon=True)
    t.start()

    # Comandi interattivi
    while t.is_alive():
        cmd = input("\nComandi: [S]top, [Q]uit → ").strip().lower()
        if cmd == "s":
            player.stop_song()
            print(config["COLORS"]["warning"] + "Riproduzione fermata manualmente")
        elif cmd == "q":
            player.stop_song()
            print(config["COLORS"]["success"] + "Uscita da Intervista\n")
            break
