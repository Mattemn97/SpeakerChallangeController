import pytest
import tempfile
import os
from pathlib import Path
from your_module_name import load_config, COLOR_MAP  # ⬅️ sostituisci con il nome reale del tuo file .py

@pytest.fixture
def config_file(tmp_path: Path):
    """Crea un file di configurazione temporaneo con vari tipi di dati."""
    content = """
    # Configurazione di test
    COLOR_TITLE=red
    COLOR_INFO=green
    MAX_VOL_AUDIO=1.0
    MIN_VOL_AUDIO=0.05
    B2B_TIMER_MIN=40
    B2B_TIMER_MAX=60
    B2B_TIMER_TOT=90
    MUSIC_FOLDER=/path/to/music
    LOG_FILE=output.log
    """
    file_path = tmp_path / "config.txt"
    file_path.write_text(content.strip(), encoding="utf-8")
    return file_path

def test_load_config_colors(config_file):
    """Verifica che i colori vengano caricati e convertiti correttamente."""
    config = load_config(config_file)
    assert "title" in config["COLORS"]
    assert config["COLORS"]["title"] == COLOR_MAP["red"]
    assert config["COLORS"]["info"] == COLOR_MAP["green"]

def test_load_config_numeric_and_float(config_file):
    """Verifica la corretta conversione di interi e float."""
    config = load_config(config_file)
    assert isinstance(config["B2B_TIMER_MIN"], int)
    assert config["B2B_TIMER_MIN"] == 40
    assert isinstance(config["MAX_VOL_AUDIO"], float)
    assert config["MAX_VOL_AUDIO"] == 1.0

def test_load_config_paths(config_file):
    """Verifica la lettura di percorsi per file e cartelle."""
    config = load_config(config_file)
    assert config["MUSIC_FOLDER"] == "/path/to/music"
    assert config["LOG_FILE"] == "output.log"

def test_load_config_comments_and_blank_lines(tmp_path):
    """Verifica che commenti e righe vuote vengano ignorati."""
    text = """
    # commento
     
    COLOR_WARNING=yellow
    """
    file_path = tmp_path / "config.txt"
    file_path.write_text(text, encoding="utf-8")
    config = load_config(file_path)
    assert "warning" in config["COLORS"]
    assert config["COLORS"]["warning"] == COLOR_MAP["yellow"]

def test_load_config_invalid_color(tmp_path):
    """Verifica che un colore non valido venga gestito senza errori."""
    text = "COLOR_ALERT=unknowncolor"
    file_path = tmp_path / "config.txt"
    file_path.write_text(text, encoding="utf-8")
    config = load_config(file_path)
    assert config["COLORS"]["alert"] == ""  # Nessuna corrispondenza nel COLOR_MAP

def test_missing_file(monkeypatch, capsys):
    """Verifica il comportamento se il file non esiste."""
    config = load_config("non_esiste.txt")
    captured = capsys.readouterr()
    assert "File di configurazione non trovato" in captured.out
    assert config == {"COLORS": {}}
