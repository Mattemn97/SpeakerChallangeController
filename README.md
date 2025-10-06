# 🎤 Speaker Challenge Terminal

Benvenuto in **Speaker Challenge Terminal**, un programma da linea di comando pensato per allenarti come un vero speaker radiofonico!  
Tre modalità — *Back2Back*, *Improvvisazione* e *Intervista* — per testare voce, ritmo e fantasia con brani casuali e timer precisi.  
Tutto controllato da un file di configurazione personalizzabile e colorato grazie a **Colorama**.

---

## 🧩 Struttura del progetto

📂 SpeakerChallenge/
├── menu.py
├── utils.py
├── modes/
│   ├── back2back.py
│   ├── improvvisazione.py
│   └── intervista.py
├── config.txt
└── requirements.txt

- **menu.py** → entrypoint del programma: mostra il menu e gestisce la selezione delle modalità.  
- **utils.py** → gestisce caricamento configurazione e colori.  
- **modes/** → contiene gli script delle modalità di gioco.  
- **config.txt** → file di configurazione per tempi, volumi, percorsi e colori.  

---

## ⚙️ Installazione

1. Assicurati di avere **Python 3.9+** installato.
2. Clona o scarica questo repository.
3. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```
4. (Opzionale) Personalizza il file `config.txt` con i tuoi percorsi audio e preferenze.

---

## 🧠 Configurazione (`config.txt`)

Ecco un esempio:

```ini
# Configurazione Speaker Challenge

MAX_VOL_AUDIO=1.0
MIN_VOL_AUDIO=0.05

B2B_TIMER_MIN=40
B2B_TIMER_MAX=60
B2B_TIMER_TOT=90
B2B_FOLDER="C:\Users\matte\Music\Audio Libro"

IMPROV_TIMER_MIN=50
IMPROV_TIMER_MAX=60
IMPROV_TIMER_TOT=90
IMPROV_FOLDER="C:\Users\matte\Music\Audio Libro"

INTERVISTA_FILE="percorso_cartella"
INTERVISTA_DURATION=180

# Colori ANSI (standard di colorama)
COLOR_TITLE=magenta
COLOR_MENU=white
COLOR_WARNING=yellow
COLOR_SUCCESS=green
COLOR_TIMER=cyan
```

### 📄 Parametri principali

| Parametro | Descrizione |
|------------|-------------|
| `MAX_VOL_AUDIO`, `MIN_VOL_AUDIO` | Volume massimo e minimo delle tracce |
| `B2B_TIMER_*` | Durate e tempi della modalità Back2Back |
| `IMPROV_TIMER_*` | Durate e tempi per l’Improvvisazione |
| `INTERVISTA_FILE`, `INTERVISTA_DURATION` | File e durata per la modalità Intervista |
| `COLOR_*` | Colori personalizzabili per menu e messaggi |

---

## 🎮 Utilizzo

Avvia il programma da terminale:

```bash
python menu.py
```

Ti troverai davanti al menu principale:

```
=== SPEAKER CHALLENGE TERMINAL ===
[1] Modalità Back2Back
[2] Modalità Improvvisazione
[3] Modalità Intervista
[Q] Esci
```

Scegli una modalità e… via col microfono!

---

## 🔊 Modalità disponibili

### 🎧 1. Back2Back
Allenati nel passaggio tra due canzoni.  
Le tracce si alternano automaticamente: il volume **si abbassa e rialza di colpo**, senza sfumature.  
Tu devi gestire il parlato nel mezzo come un vero DJ da diretta!

### 🎙️ 2. Improvvisazione
Una canzone casuale parte, e tu hai un tempo limitato per improvvisare parlando sopra.  
Puoi regolare durata e cartella musicale nel `config.txt`.

### 💬 3. Intervista
Simula un’intervista radiofonica: il programma riproduce una traccia predefinita per una durata impostata, lasciandoti spazio per domande e risposte.

---

## 🎨 Colori e stile
Grazie a **Colorama**, tutti i messaggi del terminale sono colorati.  
Puoi modificare le tonalità nel file `config.txt` scegliendo tra:
`black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`.

---

## 🧰 File `utils.py`
Gestisce caricamento configurazione e mappatura colori.  
Ignora righe commentate (`#`), supporta valori numerici, float e stringhe.

Esempio di caricamento:
```python
from utils import load_config
config = load_config()
print(config["COLORS"]["title"])
```

---

## 🚀 Esempio di sessione
```bash
> python menu.py
=== SPEAKER CHALLENGE TERMINAL ===
[1] Modalità Back2Back
[2] Modalità Improvvisazione
[3] Modalità Intervista
[Q] Esci
Seleziona una modalità: 1

--- Modalità Back2Back ---
Caricamento canzoni casuali...
Brano 1 in riproduzione 🎵
(tempo scorre...)
Brano 2 parte di colpo! 💥
```

---

## 🧑‍💻 Autore
Progetto sviluppato da **Matteo Filippini**  
Versione terminale ideata per esercizi vocali e prove di conduzione.

---

## ☕ Licenza
Distribuito liberamente per uso personale e didattico.  
Se lo usi in radio… offri almeno un caffè all’autore 😉
