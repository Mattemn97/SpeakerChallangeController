# 🎙️ Speaker Challenge Controller
Applicazione CLI in Python per allenare speaker, conduttori radio, podcaster e chiunque debba parlare in modo fluido sotto pressione, con musica, countdown e imprevisti.

Il programma gestisce diverse sfide di parlato in tempo reale, con riproduzione audio, timer, fade automatici e feedback visivo colorato a terminale.

## 🚀 Funzionalità principali
- Interfaccia da terminale, semplice e immediata
- Riproduzione musicale tramite pygame
- Countdown e timer formattati (MM:SS)
- Fade in / fade out automatici
- Gestione colori configurabile
- Estrazione casuale di news per l’improvvisazione
- Configurazione completamente esterna via config.txt

## 🎯 Modalità disponibili
### 📰 Articolo
- Simula l’esposizione di un articolo:
- Musica di sottofondo casuale
- Countdown di 15 secondi
- Tempo di esposizione random tra un minimo e un massimo
- Gong finale

### 🎧 Back2Back
- Allenamento su cambi musicali rapidi:
- Selezione di due brani casuali
- Riproduzione del primo brano
- Cambio netto a metà prova
- Riproduzione del secondo brano
- Gong finale

### ⚡ Improvvisazione
- Allenamento all’imprevisto:
- Musica di sottofondo
- Countdown di 15 secondi
- Prova di parlato
- Inserimento di una news casuale a metà
- Gong finale
(la news viene rimossa dal file dopo l’uso)

### 🎤 Intervista
- Simula una classica intervista radio:
- Musica di sottofondo
- Countdown di 15 secondi
- Tempo fisso di intervista
- Gong finale

## 📂 Struttura consigliata
```
SpeakerChallangeController/
│
├─ main.py
├─ config.txt
├─ news.txt
│
├─ audio/
│  ├─ articolo/
│  ├─ back2back/
│  ├─ improvvisazione/
│  ├─ intervista/
│  └─ gong.mp3
```

## 🗞️ File news.txt

Ogni riga è una news indipendente

Durante l’improvvisazione:
- una news viene scelta a caso
- viene rimossa dal file dopo l’uso

## ▶️ Avvio del programma
``` python
python main.py

Menu principale:

=== SPEAKER CHALLENGE TERMINAL ===
[1] Articolo
[2] Back2Back
[3] Improvvisazione
[4] Intervista
[Q] Esci
```
