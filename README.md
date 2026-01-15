# 🎤 Speaker Challenge Terminal

Applicazione Python da terminale per gestire **sfide vocali, improvvisazioni e interviste** con supporto audio, timer e colori configurabili.

Pensata per utilizzo live: radio, podcast, giochi di improvvisazione, eventi o allenamenti di public speaking.

---

## 🚀 Funzionalità principali

- Riproduzione audio casuale da cartelle dedicate
- Timer con countdown formattato `MM:SS`
- Gestione automatica del volume
- Modalità di gioco multiple
- Estrazione casuale di news da file `.txt`
- Output colorato e configurabile
- Interfaccia interamente da terminale

---

## 🧩 Modalità disponibili

### 🔁 Back2Back
- Riproduce **due brani consecutivi**
- Abbassa il volume a metà
- Cambio automatico del brano
- Countdown fino al termine

### 🎭 Improvvisazione
- Riproduce un brano casuale
- Dopo un tempo casuale:
  - abbassa il volume
  - mostra una **breaking news inventata**
- Countdown fino alla fine dell’improvvisazione

### 🎙 Intervista
- Riproduce un brano di sottofondo
- Abbassa il volume dopo 15 secondi
- Timer totale per la durata dell’intervista
- Riporta il volume al massimo prima della fine

---

## 📁 Struttura dei file

project/
│
├── main.py
├── config.txt
├── news.txt
│
├── back2back/
│ └── *.mp3 / *.wav
│
├── improvvisazione/
│ └── *.mp3 / *.wav
│
└── intervista/
└── *.mp3 / *.wav

---

## ⚙️ Configurazione (`config.txt`)

Esempio:

```
# Cartelle
BACK2BACK_FOLDER=music/back2back
IMPROVVISAZIONE_FOLDER=music/improvvisazione
INTERVISTA_FOLDER=music/intervista

#Timer (secondi)
BACK2BACK_TIMER_TOT=120
BACK2BACK_TIMER_MIN=30
BACK2BACK_TIMER_MAX=60

IMPROVVISAZIONE_TIMER_TOT=90
IMPROVVISAZIONE_TIMER_MIN=20
IMPROVVISAZIONE_TIMER_MAX=60

INTERVISTA_TIMER_TOT=60

# Volume (0.0 - 1.0)
MAX_VOL_AUDIO=1.0
MIN_VOL_AUDIO=0.3

# Colori
COLOR_MODE=cyan
COLOR_MENU=green
COLOR_WARNING=yellow
COLOR_TIMER=magenta
COLOR_NEWS=red
```


Tutti i messaggi di errore usano **sempre lo stesso colore** (`COLOR_WARNING`).

---

## 📰 File `news.txt`

Contiene titoli di news inventate, **una per riga**.

Ogni news:
- viene scelta casualmente
- viene mostrata una sola volta
- viene **rimossa dal file** dopo l’uso

Esempio:
```
Scoperto un pianeta dove piove caffè
Un robot vince un torneo di improvvisazione teatrale
Nuova legge obbliga le sveglie a suonare più gentili
```

---

## 🛠 Funzioni principali

### `formatta_tempo(secondi)`
Converte secondi in formato MM:SS

### `nome_file(percorso)`
Estrae il nome del file da un path completo.

### `estrai_news_casuale(config, file_path)`
Restituisce una news casuale e la rimuove dal file.

### `MusicPlayer`
Gestisce:
- caricamento brani
- play / stop
- volume
- inizializzazione sicura di `pygame`

---

## ▶️ Avvio del programma

```bash
python main.py

[1] Back2Back
[2] Improvvisazione
[3] Intervista
[Q] Esci
```

## 📦 Dipendenze
```bash
pip install pygame colorama
```

---

## 🧠 Note di design

- Nessun crash fatale: errori gestiti con messaggi leggibili
- Tutti i warning sono uniformi e configurabili
- Pensato per uso live, non per debug rumoroso
- Codice modulare e facilmente estendibile

---

## 🎉 Possibili estensioni

- Modalità torneo
- Log degli speaker
- Modalità silenziosa / verbose
- Supporto MIDI / controller esterni
- Randomizzazione effetti audio