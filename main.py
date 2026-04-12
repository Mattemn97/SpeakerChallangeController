#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Speaker Challenge Controller - Sistema Enterprise per la gestione di prove di parlato in tempo reale.

Funzionalità principali:
- Modalità operative: Intervista, Improvvisazione, Back2Back, Articolo.
- Interfaccia CLI avanzata tramite libreria 'rich'.
- Architettura disaccoppiata (Business Logic / Presentation Layer).
- Logging strutturato delle operazioni.

Autore: Speaker Challenge
Data: 2026
"""

import time
import random
from pathlib import Path
from typing import Dict, List, Optional, Any

import pygame
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeRemainingColumn,
)

# Importazione del logger aziendale come da standard
from custom_logger import logger


# ==========================================
# CORE: Logica di Business e Gestione Dati
# ==========================================

def load_configuration(config_path: Path = Path("config.txt")) -> Dict[str, Any]:
    """
    Analizza e carica il file di configurazione nel sistema.
    
    :param config_path: Percorso del file di configurazione.
    :return: Dizionario contenente i parametri validati.
    """
    config: Dict[str, Any] = {}
    
    if not config_path.exists():
        logger.warning(f"File di configurazione {config_path} non trovato. Verranno utilizzati i valori di default.")
        return config

    try:
        content = config_path.read_text(encoding="utf-8")
        for line_num, line in enumerate(content.splitlines(), start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")

            try:
                # Ignoriamo COLOR_ per migrazione a rich, processiamo il resto
                if key.startswith("COLOR_"):
                    continue
                elif key.endswith("VOL_AUDIO"):
                    config[key] = float(value)
                elif key.endswith("FOLDER") or key.endswith("PATH") or key.endswith("FILE"):
                    config[key] = str(Path(value).as_posix())
                else:
                    config[key] = int(value)
            except ValueError:
                logger.error(f"Errore di conversione nel file di configurazione alla riga {line_num}: {key}={value}")

    except PermissionError:
        logger.error(f"Permessi insufficienti per leggere il file {config_path}.")
    except Exception as e:
        logger.critical(f"Errore critico durante la lettura della configurazione: {e}", exc_info=True)

    return config


def extract_random_news(news_file: Path = Path("news.txt")) -> Optional[str]:
    """
    Estrae una notizia casuale dal file specificato, rimuovendola per evitare ripetizioni.
    
    :param news_file: Percorso del file contenente le notizie.
    :return: Stringa contenente la notizia, o None se non disponibile.
    """
    if not news_file.exists():
        logger.warning(f"File notizie {news_file.name} non trovato.")
        return None

    try:
        lines = [line.strip() for line in news_file.read_text(encoding="utf-8").splitlines() if line.strip()]

        if not lines:
            logger.warning("Nessuna notizia disponibile nel file.")
            return None

        selected_news = random.choice(lines)
        lines.remove(selected_news)

        news_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
        logger.info(f"Notizia estratta con successo. Rimanenti: {len(lines)}")
        return selected_news

    except Exception as e:
        logger.critical(f"Errore critico durante l'accesso al file notizie: {e}", exc_info=True)
        return None


def get_audio_files(folder_path_str: str) -> List[Path]:
    """
    Scansiona la directory specificata alla ricerca di file audio supportati.
    
    :param folder_path_str: Percorso della cartella come stringa.
    :return: Lista di oggetti Path corrispondenti ai file audio.
    """
    folder = Path(folder_path_str)
    if not folder.is_dir():
        logger.warning(f"Directory audio non trovata o non valida: {folder.resolve()}")
        return []
    
    return [f for f in folder.iterdir() if f.is_file() and f.suffix.lower() in (".mp3", ".wav")]


class AudioEngine:
    """
    Motore di riproduzione audio incapsulato per gestire la libreria pygame in modo sicuro.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.current_track: Optional[Path] = None
        
        try:
            pygame.mixer.init()
            logger.info("Motore audio (pygame.mixer) inizializzato con successo.")
        except pygame.error as e:
            logger.critical(f"Impossibile inizializzare il sottosistema audio: {e}", exc_info=True)

    def load_track(self, track_path: Path) -> bool:
        if not track_path.exists():
            logger.error(f"Traccia audio non trovata: {track_path.resolve()}")
            return False
            
        try:
            pygame.mixer.music.load(str(track_path))
            self.current_track = track_path
            logger.debug(f"Traccia caricata in memoria: {track_path.name}")
            return True
        except pygame.error as e:
            logger.error(f"Errore durante il caricamento della traccia {track_path.name}: {e}")
            return False

    def play(self) -> None:
        try:
            pygame.mixer.music.play()
            logger.info(f"Riproduzione avviata: {self.current_track.name if self.current_track else 'Sconosciuta'}")
        except pygame.error as e:
            logger.error(f"Errore in fase di riproduzione: {e}")

    def stop(self) -> None:
        pygame.mixer.music.stop()
        logger.debug("Riproduzione interrotta.")

    def set_volume(self, volume: float) -> None:
        volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(volume)

    def transition_volume(self, start_vol: float, end_vol: float, duration_sec: float = 1.0) -> None:
        """
        Esegue una transizione fluida del volume nel tempo specificato.
        """
        start_vol = max(0.0, min(1.0, start_vol))
        end_vol = max(0.0, min(1.0, end_vol))
        start_time = time.time()

        logger.debug(f"Inizio transizione volume da {start_vol} a {end_vol} in {duration_sec}s")

        while True:
            elapsed = time.time() - start_time
            if elapsed >= duration_sec:
                self.set_volume(end_vol)
                break

            progress = elapsed / duration_sec
            current_vol = start_vol + (end_vol - start_vol) * progress
            self.set_volume(current_vol)
            time.sleep(0.01)

    def fade_in(self) -> None:
        min_vol = self.config.get("MIN_VOL_AUDIO", 0.0)
        max_vol = self.config.get("MAX_VOL_AUDIO", 1.0)
        self.transition_volume(min_vol, max_vol)

    def fade_out(self) -> None:
        min_vol = self.config.get("MIN_VOL_AUDIO", 0.0)
        max_vol = self.config.get("MAX_VOL_AUDIO", 1.0)
        self.transition_volume(max_vol, min_vol)

    def play_gong(self) -> None:
        gong_path = Path(self.config.get("GONG_PATH", "gong.mp3"))
        if self.load_track(gong_path):
            self.set_volume(self.config.get("MAX_VOL_AUDIO", 1.0))
            self.play()
            time.sleep(5)


# ==========================================
# UI: Logica di Presentazione e Terminale
# ==========================================

def display_welcome_banner(console: Console) -> None:
    console.clear()
    console.print("[bold blue]=============================================[/bold blue]")
    console.print("[bold white]      SPEAKER CHALLENGE CONTROLLER           [/bold white]")
    console.print("[bold blue]=============================================[/bold blue]\n")


def execute_countdown(console: Console, description: str, seconds: int) -> None:
    """Gestisce un'attesa visuale tramite progress bar standardizzata."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeRemainingColumn(),
        console=console
    ) as progress:
        task = progress.add_task(f"[cyan]{description}[/cyan]", total=seconds)
        for _ in range(seconds):
            time.sleep(1)
            progress.advance(task)


def show_pre_execution_summary(console: Console, mode_name: str, tracks: List[Path], duration: int) -> None:
    """Mostra una tabella riassuntiva prima di avviare l'esecuzione."""
    table = Table(title="Riepilogo Parametri di Prova", header_style="bold magenta")
    table.add_column("Parametro", style="dim")
    table.add_column("Valore")

    table.add_row("Modalita", mode_name)
    table.add_row("Tracce Selezionate", ", ".join([t.stem for t in tracks]))
    table.add_row("Durata Stimata", f"{duration} secondi")

    console.print(table)
    console.print()


# ==========================================
# CONTROLLER: Orchestrazione delle Modalità
# ==========================================

def run_standard_mode(config: Dict[str, Any], console: Console, mode_name: str, folder_key: str, timer_key: str) -> None:
    """Gestisce l'esecuzione generica per Intervista e Articolo."""
    tracks = get_audio_files(config.get(folder_key, ""))
    if not tracks:
        console.print(f"[bold red]Errore: Nessuna traccia audio reperita per la modalità {mode_name}.[/bold red]")
        return

    selected_track = random.choice(tracks)
    duration = config.get(timer_key, 30)

    if mode_name == "Articolo":
        min_t = config.get("ARTICOLO_TIMER_MIN", 30)
        max_t = config.get("ARTICOLO_TIMER_MAX", 60)
        duration = random.randint(min_t, max_t)

    show_pre_execution_summary(console, mode_name, [selected_track], duration)
    
    if not Confirm.ask("Avviare la prova ora?"):
        logger.info("Prova annullata dall'utente.")
        return

    engine = AudioEngine(config)
    if not engine.load_track(selected_track):
        return

    engine.play()
    engine.fade_in()

    execute_countdown(console, "Preparazione all'inizio della prova...", 15)
    
    engine.fade_out()
    console.print("\n[bold green]--- INIZIO PROVA ---[/bold green]\n")
    
    execute_countdown(console, "Svolgimento della prova in corso...", duration)

    engine.fade_out()
    engine.play_gong()
    engine.stop()
    
    console.print(f"\n[bold blue]Sessione '{mode_name}' completata.[/bold blue]")


def run_improvvisazione(config: Dict[str, Any], console: Console) -> None:
    """Gestisce la logica avanzata della modalità Improvvisazione."""
    tracks = get_audio_files(config.get("IMPROVVISAZIONE_FOLDER", ""))
    if not tracks:
        console.print("[bold red]Errore: Nessuna traccia audio reperita per la modalità Improvvisazione.[/bold red]")
        return

    selected_track = random.choice(tracks)
    duration = config.get("IMPROVVISAZIONE_TIMER_TOT", 60)
    news_trigger_sec = random.randint(
        config.get("IMPROVVISAZIONE_TIMER_MIN", 10),
        config.get("IMPROVVISAZIONE_TIMER_MAX", 50)
    )

    show_pre_execution_summary(console, "Improvvisazione", [selected_track], duration)
    
    if not Confirm.ask("Avviare la prova ora?"):
        return

    engine = AudioEngine(config)
    engine.load_track(selected_track)
    engine.play()
    engine.fade_in()

    execute_countdown(console, "Preparazione all'inizio della prova...", 15)
    engine.fade_out()
    
    console.print("\n[bold green]--- INIZIO PROVA ---[/bold green]\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        console=console
    ) as progress:
        task = progress.add_task("[cyan]Improvvisazione in corso...[/cyan]", total=duration)
        
        for sec_passed in range(duration):
            if sec_passed == news_trigger_sec:
                news_text = extract_random_news(Path("news.txt"))
                if news_text:
                    progress.console.print(f"\n[bold yellow]NOTIZIA LAMPO:[/bold yellow] [white]{news_text}[/white]\n")
                    logger.info("Notizia lampo mostrata a schermo.")

            time.sleep(1)
            progress.advance(task)

    engine.fade_out()
    engine.play_gong()
    engine.stop()
    console.print("\n[bold blue]Sessione 'Improvvisazione' completata.[/bold blue]")


def run_back2back(config: Dict[str, Any], console: Console) -> None:
    """Gestisce la modalità Back2Back con transizione tra due brani."""
    tracks = get_audio_files(config.get("BACK2BACK_FOLDER", ""))
    if len(tracks) < 2:
        console.print("[bold red]Errore: Richieste almeno 2 tracce audio per la modalità Back2Back.[/bold red]")
        return

    track_1, track_2 = random.sample(tracks, 2)
    total_duration = config.get("BACK2BACK_TIMER_TOT", 60)
    
    # Suddivisione temporale coerente con la logica originale
    t_low = random.randint(
        config.get("BACK2BACK_TIMER_LOW_MIN", 15),
        config.get("BACK2BACK_TIMER_LOW_MAX", 30)
    )
    half = t_low // 2
    part1_duration = (total_duration // 2) - half
    part2_duration = half * 2  # Adattato alla logica originaria di transizione

    show_pre_execution_summary(console, "Back2Back", [track_1, track_2], total_duration)

    if not Confirm.ask("Avviare la prova ora?"):
        return

    engine = AudioEngine(config)
    engine.load_track(track_1)
    engine.play()
    engine.fade_in()

    console.print("\n[bold green]--- FASE 1: TRACCIA PRIMARIA ---[/bold green]\n")
    execute_countdown(console, f"Riproduzione: {track_1.stem}", part1_duration)
    
    engine.fade_out()
    console.print("\n[bold yellow]--- TRANSIZIONE IN CORSO ---[/bold yellow]\n")
    execute_countdown(console, "Cambio brano...", half)

    engine.load_track(track_2)
    engine.play()
    engine.set_volume(config.get("MAX_VOL_AUDIO", 1.0))

    console.print("\n[bold green]--- FASE 2: TRACCIA SECONDARIA ---[/bold green]\n")
    execute_countdown(console, f"Riproduzione: {track_2.stem}", half)

    engine.fade_out()
    engine.play_gong()
    engine.stop()
    console.print("\n[bold blue]Sessione 'Back2Back' completata.[/bold blue]")


# ==========================================
# ENTRYPOINT: Menu Principale
# ==========================================

def main() -> None:
    console = Console()
    config = load_configuration()
    logger.info("Avvio del Controller Speaker Challenge completato.")

    while True:
        display_welcome_banner(console)
        
        menu_options = {
            "1": "Esposizione Articolo",
            "2": "Sfida Back2Back",
            "3": "Prova di Improvvisazione",
            "4": "Simulazione Intervista",
            "Q": "Termina Applicazione"
        }

        # Stampa formattata delle opzioni
        for key, text in menu_options.items():
            console.print(f"  [bold cyan][{key}][/bold cyan] {text}")
        
        console.print()
        scelta = Prompt.ask("Selezionare una modalità operativa", choices=list(menu_options.keys()), show_choices=False)

        if scelta == "1":
            run_standard_mode(config, console, "Articolo", "ARTICOLO_FOLDER", "ARTICOLO_TIMER_TOT")
        elif scelta == "2":
            run_back2back(config, console)
        elif scelta == "3":
            run_improvvisazione(config, console)
        elif scelta == "4":
            run_standard_mode(config, console, "Intervista", "INTERVISTA_FOLDER", "INTERVISTA_TIMER_TOT")
        elif scelta.upper() == "Q":
            console.print("[bold green]Arresto del sistema. Arrivederci.[/bold green]")
            logger.info("Arresto dell'applicazione richiesto dall'utente.")
            break
        
        # Pausa prima di ricaricare il menu per leggere i report finali
        if scelta.upper() != "Q":
            Prompt.ask("\n[dim]Premere Invio per tornare al menu principale...[/dim]")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Interruzione manuale (KeyboardInterrupt) rilevata. Uscita forzata.")
        Console().print("\n[bold yellow]Esecuzione interrotta dall'operatore.[/bold yellow]")
    except Exception as unexpected_e:
        logger.critical(f"Errore fatale imprevisto nel thread principale: {unexpected_e}", exc_info=True)
        Console().print("\n[bold red]Errore di sistema critico. Consultare i file di log aziendali.[/bold red]")