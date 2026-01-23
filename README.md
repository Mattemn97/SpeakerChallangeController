# 🎤 Speaker Challenge Terminal

Applicazione Python interattiva da terminale per gestire **sfide vocali, improvvisazioni e interviste** con supporto audio completo, timer precisi e output completamente configurabile.

Ideale per: radio, podcast, spettacoli di improvvisazione, eventi dal vivo, competizioni di public speaking e allenamenti di comunicazione.

---

## ✨ Funzionalità principali

- ✅ Riproduzione audio casuale da cartelle dedicate
- ✅ Timer con countdown preciso in formato `MM:SS`
- ✅ Gestione dinamica del volume con transizioni fluide (fade in/out)
- ✅ Tre modalità di gioco configurabili
- ✅ Estrazione casuale di news da file `.txt` (modalità Improvvisazione)
- ✅ Output completamente colorato e personalizzabile
- ✅ Interfaccia intuitiva da terminale
- ✅ Gestione robusta degli errori senza crash
- ✅ Gong di notifica alla fine di ogni prova

---

## 🎮 Modalità disponibili

### 🔁 Back2Back
**Sfida di cambio rapido tra due brani**

Sequenza:
1. Seleziona casualmente **2 brani diversi**
2. Riproduce il primo brano
3. **Countdown iniziale** (tempo configurabile)
4. Abbassa il volume in modo fluido
5. **Countdown di cambio brano** (transizione)
6. Carica e riproduce il secondo brano
7. **Countdown finale**
8. Suono del gong e fine prova

**Parametri configurabili:**
- `BACK2BACK_FOLDER`: Cartella con i brani
- `BACK2BACK_TIMER_TOT`: Tempo totale della prova (secondi)
- `BACK2BACK_TIMER_LOW_MIN`: Durata minima di ogni brano (secondi)
- `BACK2BACK_TIMER_LOW_MAX`: Durata massima di ogni brano (secondi)

---

### 🎭 Improvvisazione
**Sfida di improvvisazione con breaking news casuale**

Sequenza:
1. Riproduce un brano casuale dalla cartella
2. **Countdown di 15 secondi** prima dell'inizio
3. Abbassa il volume per la prova
4. **Durante la prova**: una news casuale viene mostrata a un momento random
5. **Countdown fino al termine**
6. Suono del gong e fine prova

**Parametri configurabili:**
- `IMPROVVISAZIONE_FOLDER`: Cartella con i brani
- `IMPROVVISAZIONE_TIMER_TOT`: Durata totale dell'improvvisazione (secondi)
- `IMPROVVISAZIONE_TIMER_MIN`: Tempo minimo prima della news (secondi)
- `IMPROVVISAZIONE_TIMER_MAX`: Tempo massimo prima della news (secondi)

---

### 🎙️ Intervista
**Sfida di intervista con musica di sottofondo**

Sequenza:
1. Riproduce un brano casuale dalla cartella
2. Porta il volume al massimo
3. **Countdown di 15 secondi** prima dell'inizio dell'intervista
4. Abbassa il volume in modo fluido
5. **Countdown della durata dell'intervista**
6. Riporta il volume al massimo
7. Suono del gong e fine prova

**Parametri configurabili:**
- `INTERVISTA_FOLDER`: Cartella con i brani
- `INTERVISTA_TIMER_TOT`: Durata totale dell'intervista (secondi)

---

## 📁 Struttura dei file

```
project/
│
├── main.py                          # Programma principale
├── config.txt                       # File di configurazione
├── news.txt                         # News per la modalità Improvvisazione
├── README.md                        # Questo file
│
├── back2back/                       # Brani per modalità Back2Back
│   ├── brano1.mp3
│   ├── brano2.mp3
│   └── ...
│
├── improvvisazione/                 # Brani per modalità Improvvisazione
│   ├── brano1.mp3
│   ├── brano2.mp3
│   └── ...
│
└── intervista/                      # Brani per modalità Intervista
    ├── brano1.mp3
    ├── brano2.mp3
    └── ...
```

---

## ⚙️ Configurazione (`config.txt`)

Il file `config.txt` contiene tutte le impostazioni dell'applicazione. Ogni riga ha il formato `CHIAVE=VALORE`.

**Esempio completo:**

```ini
# ========================================
# PERCORSI DELLE CARTELLE
# ========================================
BACK2BACK_FOLDER=back2back
IMPROVVISAZIONE_FOLDER=improvvisazione
INTERVISTA_FOLDER=intervista
GONG_PATH=gong.mp3

# ========================================
# TIMER MODALITA' BACK2BACK (secondi)
# ========================================
BACK2BACK_TIMER_TOT=120
BACK2BACK_TIMER_LOW_MIN=30
BACK2BACK_TIMER_LOW_MAX=60

# ========================================
# TIMER MODALITA' IMPROVVISAZIONE (secondi)
# ========================================
IMPROVVISAZIONE_TIMER_TOT=90
IMPROVVISAZIONE_TIMER_MIN=20
IMPROVVISAZIONE_TIMER_MAX=60

# ========================================
# TIMER MODALITA' INTERVISTA (secondi)
# ========================================
INTERVISTA_TIMER_TOT=60

# ========================================
# VOLUME AUDIO (valori 0.0 - 1.0)
# ========================================
MAX_VOL_AUDIO=1.0
MIN_VOL_AUDIO=0.3

# ========================================
# COLORI DEL TERMINALE
# ========================================
# Valori supportati: black, red, green, yellow, blue, magenta, cyan, white
COLOR_MODE=cyan
COLOR_MENU=green
COLOR_CANZONE=blue
COLOR_INIZIO=yellow
COLOR_TERMINE=magenta
COLOR_CAMBIO=cyan
COLOR_NEWS=red
COLOR_WARNING=yellow
```

**Note sulla configurazione:**
- Le righe che iniziano con `#` sono commenti e vengono ignorate
- I percorsi FOLDER/PATH supportano sia `\` che `/` (vengono normalizzati)
- I volumi devono essere compresi tra `0.0` (silenzio) e `1.0` (massimo)
- I colori devono corrispondere ai nomi di colorama (case-insensitive)

---

## 📰 File `news.txt`

Contiene titoli di news casuali da mostrare durante la modalità **Improvvisazione**.

**Caratteristiche:**
- Una news per riga
- Ogni news viene scelta **casualmente**
- Dopo l'uso, la news viene **rimossa dal file**
- Ideale per aggiungere variabilità e difficoltà alle prove

**Esempio:**
```
Scoperto un pianeta dove piove caffè
Un robot vince un torneo di improvvisazione teatrale
Nuova legge obbliga le sveglie a suonare più gentili
La luna è stata brevettata come parco divertimenti
```

---

## 🔊 Audio e suoni

### Brani musicali
- Supportati i formati: `.mp3` e `.wav`
- Usare brani senza basso troppo marcato per non coprire la voce
- Durata consigliata: 30-120 secondi a seconda della modalità

### Gong
- File configurabile in `config.txt` (`GONG_PATH`)
- Riprodotto alla fine di ogni prova
- Volume sempre al massimo
- Durata riproduzione: 5 secondi

---

## 🛠 Classe MusicPlayer

Gestisce tutta la parte audio dell'applicazione:

```python
class MusicPlayer:
    def __init__(self, config)           # Inizializzazione
    def load_song(path) -> bool          # Carica un file audio
    def play_song()                      # Avvia la riproduzione
    def stop_song()                      # Ferma la riproduzione
    def set_volume(volume)               # Imposta il volume (istantaneo)
    def fade_volume(start, end, dur)     # Transizione volume fluida
```

---

## 🚀 Come avviare

### Prerequisiti
- Python 3.8+
- pip

### Installazione dipendenze
```bash
pip install pygame colorama
```

### Avvio
```bash
python main.py
```

### Menu principale
```
=== SPEAKER CHALLENGE TERMINAL ===
[1] Back2Back
[2] Improvvisazione
[3] Intervista
[Q] Esci

Scelta: _
```

Inserire il numero o la lettera desiderata e premere Enter.

---

## 📋 Funzioni principali

### Utilità
- **`formatta_tempo(secondi: int) -> str`** - Converte secondi in formato MM:SS
- **`nome_file(percorso: str) -> str`** - Estrae il nome file da un percorso
- **`clear_screen() -> None`** - Cancella il terminale (compatibile Windows/Linux)

### Configurazione
- **`load_config(file_path: str) -> dict`** - Carica il file config.txt

### Audio
- **`estrai_news_casuale(config: dict) -> str | None`** - Estrae una news casuale da news.txt
- **`fade_in(player, config) -> None`** - Aumenta il volume al massimo
- **`fade_out(player, config) -> None`** - Riduce il volume al minimo
- **`play_gong(player, config) -> None`** - Riproduce il gong finale

### Modalità
- **`run_back2back(config: dict) -> None`** - Esecuzione modalità Back2Back
- **`run_improvvisazione(config: dict) -> None`** - Esecuzione modalità Improvvisazione
- **`run_intervista(config: dict) -> None`** - Esecuzione modalità Intervista

---

## 🧠 Caratteristiche di design

✅ **Robusto**: Gestione completa degli errori senza crash
✅ **Modulare**: Codice organizzato in funzioni e classi logiche
✅ **Configurabile**: Tutti i parametri nel file `config.txt`
✅ **PEP 8 compliant**: Segue gli standard Python
✅ **Documentato**: Docstring completi per tutte le funzioni
✅ **Type hints**: Annotazioni di tipo per maggiore chiarezza
✅ **Live-friendly**: Output chiaro e intuitivo, gestione senza freeze

---

## 🎯 Casi di uso

### 📻 Radio
Creare sfide vocali in diretta per il pubblico con timer e musica di sottofondo

### 🎬 Podcast
Registrare improvvisazioni con news casuali per episodi più dinamici

### 🎭 Spettacoli improvvisazione
Gestire le prove degli attori con transizioni audio e timing preciso

### 🏆 Competizioni public speaking
Allenare i partecipanti con modalità cronometrate e controllate

### 📚 Scuole e università
Esercitazioni di comunicazione orale con supporto audio professionale

---

## 🐛 Troubleshooting

### Errore: "File config.txt non trovato"
- Assicurati che `config.txt` sia nella stessa cartella di `main.py`
- Verifica i permessi di lettura del file

### Errore: "File audio non trovato"
- Controlla i percorsi in `config.txt`
- Assicurati che i file .mp3 o .wav siano presenti nelle cartelle
- Usa percorsi relativi (es. `back2back/` invece di percorsi assoluti)

### Nessun suono
- Verifica che l'audio del sistema sia acceso
- Controlla i volumi in `config.txt` (MAX_VOL_AUDIO, MIN_VOL_AUDIO)
- Assicurati che pygame sia installato correttamente: `pip install pygame`

### Colori non visualizzati
- Su Windows: colorama dovrebbe renderizzare i colori ANSI automaticamente
- Su Linux/Mac: assicurati che il terminale supporti colori ANSI 256

---

## 📝 Note di sviluppo

- Il codice utilizza `pygame.mixer` per la gestione audio cross-platform
- Le transizioni di volume sono implementate con interpolazione lineare
- I timer usano `time.time()` per precisione millisecondare
- Le news vengono rimosse dal file per evitare ripetizioni

---

## 🤝 Contributi

Possibili miglioramenti futuri:
- [ ] Modalità torneo con ranking
- [ ] Log persistenti delle performance
- [ ] Modalità silenziosa per testing
- [ ] Supporto per controller MIDI
- [ ] Effetti audio personalizzati
- [ ] Interfaccia grafica (PyQt/Tkinter)
- [ ] Export statistics in CSV

---

## 📄 Licenza

Uso libero per scopi educativi e non commerciali.

---

## 👨‍💻 Autore

Speaker Challenge
Data di creazione: 2026

---

**Divertiti con le tue sfide vocali! 🎤**
