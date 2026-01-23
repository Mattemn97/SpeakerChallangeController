"""
Speaker Challenge Controller - Applicazione per gestire prove di parlato in tempo reale.

Questo programma fornisce tre modalità di sfida:
- Intervista: prova di intervista con musica di sottofondo
- Improvvisazione: prova di improvvisazione con news casuali
- Back2Back: cambio rapido tra due brani musicali

Autore: Speaker Challenge
Data: 2026
"""

import os
import time
import random
import colorama
import pygame

# Inizializza colorama per supportare colori ANSI su Windows
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

def formatta_tempo(secondi: int) -> str:
    """
    Converte i secondi in formato MM:SS.

    Args:
        secondi (int): Numero di secondi da formattare.

    Returns:
        str: Stringa nel formato MM:SS (es. "01:30").
    """
    secondi = max(0, int(secondi))
    minuti = secondi // 60
    secondi_restanti = secondi % 60
    return f"{minuti:02d}:{secondi_restanti:02d}"


def nome_file(percorso: str) -> str:
    """
    Estrae il nome del file dal percorso, rimuovendo l'estensione .mp3.

    Args:
        percorso (str): Percorso completo del file.

    Returns:
        str: Nome del file senza estensione.
    """
    return os.path.basename(percorso).replace(".mp3", "")


def clear_screen() -> None:
    """
    Cancella il terminale in modo compatibile con Windows e Unix/Linux.
    """
    os.system("cls" if os.name == "nt" else "clear")

def load_config(file_path: str = "config.txt") -> dict:
    """
    Carica la configurazione dal file config.txt.

    Analizza il file di configurazione e popola un dizionario con:
    - Colori (COLOR_* = colore)
    - Volumi (VOL_AUDIO = float tra 0 e 1)
    - Percorsi (FOLDER, PATH = percorso)
    - Valori interi (tutto il resto)

    Args:
        file_path (str): Percorso del file di configurazione. Default: "config.txt".

    Returns:
        dict: Dizionario con la configurazione caricata.
    """
    config = {"COLORS": {}}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for num, line in enumerate(f, start=1):
                line = line.strip()

                # Ignora righe vuote e commenti
                if not line or line.startswith("#"):
                    continue

                # Divide la riga in chiave e valore
                key, value = line.split("=", 1)
                key, value = key.strip(), value.strip()

                try:
                    # Gestisce diverse tipologie di configurazione
                    if key.startswith("COLOR_"):
                        config["COLORS"][
                            key.replace("COLOR_", "").lower()
                        ] = COLOR_MAP.get(value.lower(), "")
                    elif key.endswith("VOL_AUDIO"):
                        config[key] = float(value)
                    elif key.endswith("FOLDER") or key.endswith("PATH"):
                        config[key] = str(
                            value.strip().strip('"').replace("\\", "/")
                        )
                    else:
                        config[key] = int(value)

                except ValueError:
                    print(
                        COLOR_MAP.get("red")
                        + f"Valore non valido nel config alla riga {num}\n"
                    )

    except FileNotFoundError:
        print(
            COLOR_MAP.get("red") + "File config.txt non trovato\n"
        )

    except PermissionError:
        print(
            COLOR_MAP.get("red")
            + "Permessi insufficienti per leggere config.txt\n"
        )

    return config

def estrai_news_casuale(config: dict, file_path: str = "news.txt") -> str | None:
    """
    Estrae una news casuale dal file news.txt e la rimuove dal file.

    Args:
        config (dict): Dizionario di configurazione.
        file_path (str): Percorso del file delle news. Default: "news.txt".

    Returns:
        str | None: Una news casuale, oppure None se il file non esiste.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            righe = [r.strip() for r in f if r.strip()]

        if not righe:
            print(
                config["COLORS"]["warning"] + "Nessuna news disponibile\n"
            )
            return None

        # Sceglie una news casuale e la rimuove dal file
        scelta = random.choice(righe)
        righe.remove(scelta)

        # Salva le news rimanenti
        with open(file_path, "w", encoding="utf-8") as f:
            for r in righe:
                f.write(r + "\n")

        return scelta

    except FileNotFoundError:
        print(
            config["COLORS"]["warning"] + "File news.txt non trovato\n"
        )
        return None

class MusicPlayer:
    """
    Gestisce la riproduzione audio mediante pygame.mixer.

    Fornisce funzionalità per caricare, riprodurre, pausare e controllare
    il volume della musica.
    """

    def __init__(self, config: dict) -> None:
        """
        Inizializza il player musicale.

        Args:
            config (dict): Dizionario di configurazione.
        """
        self.config = config
        self.current_song = None

        try:
            pygame.mixer.init()
        except pygame.error:
            print(
                config["COLORS"]["warning"]
                + "Errore inizializzazione audio\n"
            )

    def load_song(self, path: str) -> bool:
        """
        Carica un file audio dal percorso specificato.

        Args:
            path (str): Percorso del file audio.

        Returns:
            bool: True se il caricamento è riuscito, False altrimenti.
        """
        if not os.path.isfile(path):
            print(
                self.config["COLORS"]["warning"]
                + "File audio non trovato\n"
            )
            return False

        try:
            pygame.mixer.music.load(path)
            self.current_song = path
            return True
        except pygame.error:
            print(
                self.config["COLORS"]["warning"]
                + "Errore caricamento file audio\n"
            )
            return False

    def play_song(self) -> None:
        """
        Avvia la riproduzione del brano caricato.
        """
        try:
            pygame.mixer.music.play()
        except pygame.error:
            print(
                self.config["COLORS"]["warning"]
                + "Errore durante la riproduzione audio\n"
            )

    def set_volume(self, volume: float) -> None:
        """
        Imposta il volume della musica.

        Args:
            volume (float): Volume tra 0.0 (silenzioso) e 1.0 (massimo).
        """
        volume = max(0.0, min(1.0, volume))  # Limita tra 0 e 1
        pygame.mixer.music.set_volume(volume)

    def fade_volume(
        self,
        start_volume: float,
        end_volume: float,
        duration: float = 1.0,
    ) -> None:
        """
        Sfuma il volume da un valore iniziale a uno finale.

        Realizza una transizione lineare del volume nel tempo specificato.

        Args:
            start_volume (float): Volume iniziale (0.0 - 1.0).
            end_volume (float): Volume finale (0.0 - 1.0).
            duration (float): Durata della transizione in secondi. Default: 1.0.
        """
        start_volume = max(0.0, min(1.0, start_volume))
        end_volume = max(0.0, min(1.0, end_volume))

        start_time = time.time()

        while True:
            elapsed = time.time() - start_time

            if elapsed >= duration:
                pygame.mixer.music.set_volume(end_volume)
                break

            # Interpolazione lineare del volume
            progress = elapsed / duration
            current_volume = start_volume + (
                end_volume - start_volume
            ) * progress
            pygame.mixer.music.set_volume(current_volume)

            time.sleep(0.01)  # Aggiorna ogni 10ms per una transizione fluida

    def stop_song(self) -> None:
        """
        Ferma la riproduzione del brano corrente.
        """
        pygame.mixer.music.stop()

def fade_out(player: MusicPlayer, config: dict) -> None:
    """
    Riduce il volume al minimo in un secondo (fade out).

    Args:
        player (MusicPlayer): Istanza del player musicale.
        config (dict): Dizionario di configurazione.
    """
    player.fade_volume(config["MAX_VOL_AUDIO"], config["MIN_VOL_AUDIO"], 1.0)


def fade_in(player: MusicPlayer, config: dict) -> None:
    """
    Aumenta il volume al massimo in un secondo (fade in).

    Args:
        player (MusicPlayer): Istanza del player musicale.
        config (dict): Dizionario di configurazione.
    """
    player.fade_volume(config["MIN_VOL_AUDIO"], config["MAX_VOL_AUDIO"], 1.0)


def play_gong(player: MusicPlayer, config: dict) -> None:
    """
    Riproduce il suono del gong (segnale di fine prova).

    Args:
        player (MusicPlayer): Istanza del player musicale.
        config (dict): Dizionario di configurazione.
    """
    player.set_volume(config["MAX_VOL_AUDIO"])
    player.load_song(config["GONG_PATH"])
    player.play_song()
    time.sleep(5)

def run_intervista(config: dict) -> None:
    """
    Esecuzione della modalità Intervista.

    Procedure:
    1. Riproduce una canzone casuale dalla cartella INTERVISTA_FOLDER
    2. Countdown di 15 secondi prima dell'inizio
    3. Intervista di durata INTERVISTA_TIMER_TOT secondi
    4. Suono del gong alla fine

    Args:
        config (dict): Dizionario di configurazione.
    """
    clear_screen()
    print(config["COLORS"]["mode"] + "\n--- Modalità Intervista ---")

    # Valida la cartella configurata
    folder = (
        config.get("INTERVISTA_FOLDER", "")
        .strip()
        .strip('"')
        .replace("\\", "/")
    )
    if not os.path.isdir(folder):
        print(
            config["COLORS"]["warning"] + "Cartella intervista non valida\n"
        )
        return

    # Cerca i file audio nella cartella
    songs = [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith((".mp3", ".wav"))
    ]

    if not songs:
        print(
            config["COLORS"]["warning"] + "Nessuna canzone trovata\n"
        )
        return

    duration = config.get("INTERVISTA_TIMER_TOT", 30)

    # Seleziona una canzone casuale
    song = random.choice(songs)
    print(
        config["COLORS"]["canzone"]
        + f"CANZONE RIPRODOTTA: {nome_file(song)}"
    )

    # Inizializza e avvia la riproduzione
    player = MusicPlayer(config)
    player.load_song(song)
    player.play_song()
    fade_in(player, config)

    # Countdown prima dell'inizio
    for sec in range(15, 0, -1):
        print(
            config["COLORS"]["inizio"]
            + f"INIZIO PROVA:  {formatta_tempo(sec)}",
            end="\r",
        )
        time.sleep(1)

    fade_out(player, config)
    print(" ")

    # Intervista principale
    for sec in range(duration, 0, -1):
        print(
            config["COLORS"]["termine"]
            + f"TERMINE PROVA: {formatta_tempo(sec)}",
            end="\r",
        )
        time.sleep(1)

    fade_out(player, config)

    # Suono di fine prova
    play_gong(player, config)

    player.stop_song()
    print("\n" + config["COLORS"]["mode"] + "Intervista terminata\n")

def run_improvvisazione(config: dict) -> None:
    """
    Esecuzione della modalità Improvvisazione.

    Procedure:
    1. Riproduce una canzone casuale dalla cartella IMPROVVISAZIONE_FOLDER
    2. Countdown di 15 secondi prima dell'inizio
    3. Prova di improvvisazione con una news casuale inserita a metà
    4. Suono del gong alla fine

    Args:
        config (dict): Dizionario di configurazione.
    """
    clear_screen()
    print(config["COLORS"]["mode"] + "\n--- Modalità Improvvisazione ---")

    # Valida la cartella configurata
    folder = (
        config.get("IMPROVVISAZIONE_FOLDER", "")
        .strip()
        .strip('"')
        .replace("\\", "/")
    )
    if not os.path.isdir(folder):
        print(
            config["COLORS"]["warning"]
            + "Cartella improvvisazione non valida\n"
        )
        return

    # Cerca i file audio nella cartella
    songs = [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith((".mp3", ".wav"))
    ]

    if not songs:
        print(
            config["COLORS"]["warning"] + "Nessuna canzone trovata\n"
        )
        return

    duration = config.get("IMPROVVISAZIONE_TIMER_TOT", 60)
    sec_news = random.randint(
        config["IMPROVVISAZIONE_TIMER_MIN"],
        config["IMPROVVISAZIONE_TIMER_MAX"],
    )

    # Seleziona una canzone casuale
    song = random.choice(songs)
    print(
        config["COLORS"]["canzone"]
        + f"CANZONE RIPRODOTTA: {nome_file(song)}"
    )

    # Inizializza e avvia la riproduzione
    player = MusicPlayer(config)
    player.load_song(song)
    player.play_song()
    fade_in(player, config)

    # Countdown prima dell'inizio
    for sec in range(15, 0, -1):
        if sec == 0:
            print(" " * 50, end="\r")
            time.sleep(0.1)
        else:
            print(
                config["COLORS"]["inizio"]
                + f"INIZIO PROVA: {formatta_tempo(sec)}",
                end="\r",
            )
            time.sleep(1)

    fade_out(player, config)

    # Improvvisazione principale con news casuale
    for sec in range(duration, -1, -1):
        if sec == 0:
            print(" " * 50, end="\r")
            time.sleep(0.1)
        elif sec == sec_news:
            news = estrai_news_casuale(config)
            print(
                config["COLORS"]["news"] + f"BREAKING NEWS: {news}"
            )
        else:
            print(
                config["COLORS"]["termine"]
                + f"TERMINE PROVA: {formatta_tempo(sec)}",
                end="\r",
            )
            time.sleep(1)

    fade_out(player, config)

    # Suono di fine prova
    play_gong(player, config)

    player.stop_song()
    print(
        "\n" + config["COLORS"]["mode"] + "Improvvisazione terminata\n"
    )

def run_back2back(config: dict) -> None:
    """
    Esecuzione della modalità Back2Back.

    Procedure:
    1. Seleziona due canzoni casuali
    2. Riproduce la prima canzone per metà durata
    3. Cambia brano (transizione)
    4. Riproduce la seconda canzone per l'altra metà
    5. Suono del gong alla fine

    Args:
        config (dict): Dizionario di configurazione.
    """
    clear_screen()
    print(config["COLORS"]["mode"] + "\n--- Modalità Back2Back ---")

    # Valida la cartella configurata
    folder = (
        config.get("BACK2BACK_FOLDER", "")
        .strip()
        .strip('"')
        .replace("\\", "/")
    )
    if not os.path.isdir(folder):
        print(
            config["COLORS"]["warning"] + "Cartella Back2Back non valida\n"
        )
        return

    # Cerca i file audio nella cartella
    songs = [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith((".mp3", ".wav"))
    ]

    # Seleziona due canzoni casuali diverse
    song1, song2 = random.sample(songs, 2)
    print(
        config["COLORS"]["canzone"] + f"CANZONE ATTUALE: {nome_file(song1)}"
    )
    print(
        config["COLORS"]["canzone"]
        + f"CANZONE SUCCESSIVA: {nome_file(song2)}"
    )

    # Calcola i tempi della prova
    total = config["BACK2BACK_TIMER_TOT"]
    duration = random.randint(
        config["BACK2BACK_TIMER_LOW_MIN"],
        config["BACK2BACK_TIMER_LOW_MAX"],
    )
    half = duration // 2
    max_audio = (total // 2) - half

    # Inizializza e avvia la riproduzione del primo brano
    player = MusicPlayer(config)
    player.load_song(song1)
    player.play_song()
    fade_in(player, config)

    # Countdown prima dell'inizio
    for sec in range(max_audio, -1, -1):
        if sec == 0:
            print(" " * 50, end="\r")
            time.sleep(0.1)
        else:
            print(
                config["COLORS"]["inizio"]
                + f"INIZIO PROVA: {formatta_tempo(sec)}",
                end="\r",
            )
            time.sleep(1)

    fade_out(player, config)

    # Countdown per il cambio brano
    for sec in range(half, -1, -1):
        if sec == 0:
            print(" " * 50, end="\r")
            time.sleep(0.1)
        else:
            print(
                config["COLORS"]["cambio"]
                + f"CAMBIO BRANO: {formatta_tempo(sec)}",
                end="\r",
            )
            time.sleep(1)

    # Carica e riproduce il secondo brano
    player.load_song(song2)
    player.play_song()

    # Countdown finale
    for sec in range(half, -1, -1):
        if sec == 0:
            print(" " * 50, end="\r")
            time.sleep(0.1)
        else:
            print(
                config["COLORS"]["termine"]
                + f"TERMINE PROVA: {formatta_tempo(sec)}",
                end="\r",
            )
            time.sleep(1)

    fade_out(player, config)

    # Suono di fine prova
    play_gong(player, config)

    player.stop_song()
    print(config["COLORS"]["mode"] + "Back2Back terminato\n")

def run_articolo(config: dict) -> None:
    """
    Esecuzione della modalità Esposizione articolo.

    Procedure:
    1. Riproduce una canzone casuale dalla cartella ARTICOLO_FOLDER
    2. Countdown di 15 secondi prima dell'inizio
    3. Esposizione dell'articolo di durata random tra ARTICOLO_TIMER_MIN e ARTICOLO_TIMER_MAX secondi
    4. Suono del gong alla fine

    Args:
        config (dict): Dizionario di configurazione.
    """
    clear_screen()
    print(config["COLORS"]["mode"] + "\n--- Modalità Esposizione articolo ---")

    # Valida la cartella configurata
    folder = (
        config.get("ARTICOLO_FOLDER", "")
        .strip()
        .strip('"')
        .replace("\\", "/")
    )
    if not os.path.isdir(folder):
        print(
            config["COLORS"]["warning"] + "Cartella articolo non valida\n"
        )
        return

    # Cerca i file audio nella cartella
    songs = [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith((".mp3", ".wav"))
    ]

    if not songs:
        print(
            config["COLORS"]["warning"] + "Nessuna canzone trovata\n"
        )
        return

    duration= random.randint(
        config["ARTICOLO_TIMER_MIN"],
        config["ARTICOLO_TIMER_MAX"],
    )

    # Seleziona una canzone casuale
    song = random.choice(songs)
    print(
        config["COLORS"]["canzone"]
        + f"CANZONE RIPRODOTTA: {nome_file(song)}"
    )

    # Inizializza e avvia la riproduzione
    player = MusicPlayer(config)
    player.load_song(song)
    player.play_song()
    fade_in(player, config)

    # Countdown prima dell'inizio
    for sec in range(15, 0, -1):
        print(
            config["COLORS"]["inizio"]
            + f"INIZIO PROVA:  {formatta_tempo(sec)}",
            end="\r",
        )
        time.sleep(1)

    fade_out(player, config)
    print(" ")

    # Intervista principale
    for sec in range(duration, 0, -1):
        print(
            config["COLORS"]["termine"]
            + f"TERMINE PROVA: {formatta_tempo(sec)}",
            end="\r",
        )
        time.sleep(1)

    fade_out(player, config)

    # Suono di fine prova
    play_gong(player, config)

    player.stop_song()
    print("\n" + config["COLORS"]["mode"] + "Esposizione articolo terminata\n")


def main_menu() -> None:
    """
    Mostra il menu principale e gestisce le scelte dell'utente.

    Consente di selezionare una modalità di prova o di uscire dal programma.
    """
    CONFIG = load_config()

    while True:
        print(
            CONFIG["COLORS"]["mode"]
            + "\n=== SPEAKER CHALLENGE TERMINAL ==="
        )
        print(CONFIG["COLORS"]["menu"] + "[1] Articolo")
        print(CONFIG["COLORS"]["menu"] + "[2] Back2Back")
        print(CONFIG["COLORS"]["menu"] + "[3] Improvvisazione")
        print(CONFIG["COLORS"]["menu"] + "[4] Intervista")
        print(CONFIG["COLORS"]["menu"] + "[Q] Esci")

        choice = input("Scelta: ").strip().lower()

        if choice == "1":
            run_articolo(CONFIG)
        elif choice == "2":
            run_back2back(CONFIG)
        elif choice == "3":
            run_improvvisazione(CONFIG)
        elif choice == "4":
            run_intervista(CONFIG)
        elif choice == "q":
            print(CONFIG["COLORS"]["mode"] + "Ciao!")
            break
        else:
            print(
                CONFIG["COLORS"]["warning"] + "Scelta non valida\n"
            )


if __name__ == "__main__":
    main_menu()
