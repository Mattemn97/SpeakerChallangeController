/**
 * js/audio.js
 * Gestisce la riproduzione audio sfruttando le Web Audio API / HTML5 Audio.
 */

class MusicPlayer {
    constructor() {
        // Creiamo un elemento audio HTML5 (non visibile nella pagina)
        this.audioElement = new Audio();
        this.currentFadeInterval = null; // Riferimento per bloccare i fade se interrotti
    }

    /**
     * Carica un file audio nell'elemento player.
     * @param {File} fileObject - L'oggetto File proveniente dall'input type="file".
     * @returns {boolean} True se il caricamento è avviato.
     */
    loadSong(fileObject) {
        if (!fileObject) {
            console.warn("Nessun file fornito al MusicPlayer.");
            return false;
        }

        // Se c'è già una canzone caricata, revochiamo l'URL precedente per liberare memoria
        if (this.audioElement.src) {
            URL.revokeObjectURL(this.audioElement.src);
        }

        // Crea un URL temporaneo interno al browser per il file caricato
        const objectUrl = URL.createObjectURL(fileObject);
        this.audioElement.src = objectUrl;
        this.audioElement.load();
        return true;
    }

    /**
     * Avvia la riproduzione del brano.
     */
    playSong() {
        // La play() in JS restituisce una Promise. Gestiamo eventuali errori (es. blocco autoplay del browser).
        this.audioElement.play().catch(error => {
            console.error("Errore durante la riproduzione:", error);
            alert("Impossibile riprodurre l'audio. Assicurati di aver interagito con la pagina prima di avviare.");
        });
    }

    /**
     * Ferma la riproduzione e riporta il brano all'inizio.
     */
    stopSong() {
        this.audioElement.pause();
        this.audioElement.currentTime = 0; // Riporta la testina all'inizio
        // Interrompe eventuali fade in corso
        if (this.currentFadeInterval) {
            clearInterval(this.currentFadeInterval);
        }
    }

    /**
     * Imposta il volume istantaneamente.
     * @param {number} volume - Float da 0.0 a 1.0.
     */
    setVolume(volume) {
        // Limita il valore tra 0 e 1 per evitare errori
        this.audioElement.volume = Math.max(0.0, Math.min(1.0, volume));
    }

    /**
     * Crea un effetto fade (dissolvenza) asincrono.
     * In JS usiamo setInterval per modificare il volume a piccoli step senza bloccare la pagina.
     * @param {number} startVolume - Volume iniziale (0.0 - 1.0).
     * @param {number} endVolume - Volume finale (0.0 - 1.0).
     * @param {number} durationSec - Durata in secondi.
     * @returns {Promise} Una Promise che si risolve quando il fade è completo.
     */
    fadeVolume(startVolume, endVolume, durationSec = 1.0) {
        return new Promise((resolve) => {
            // Pulizia di vecchi fade in corso
            if (this.currentFadeInterval) {
                clearInterval(this.currentFadeInterval);
            }

            this.setVolume(startVolume);
            
            const durationMs = durationSec * 1000;
            const steps = 50; // Quanti aggiornamenti fare (50 step = animazione fluida)
            const intervalTime = durationMs / steps;
            const volumeStep = (endVolume - startVolume) / steps;
            
            let currentStep = 0;

            this.currentFadeInterval = setInterval(() => {
                currentStep++;
                let newVolume = startVolume + (volumeStep * currentStep);
                this.setVolume(newVolume);

                if (currentStep >= steps) {
                    clearInterval(this.currentFadeInterval);
                    this.setVolume(endVolume); // Assicura che arrivi esattamente al target
                    resolve(); // Segnala che il fade è finito
                }
            }, intervalTime);
        });
    }
}

// Creiamo un'istanza globale del player da usare in tutta l'app
const globalPlayer = new MusicPlayer();

/**
 * Funzioni helper globali per fade in/out veloci, come avevi in Python.
 */
function fadeOut(player) {
    return player.fadeVolume(1.0, 0.0, 1.0);
}

function fadeIn(player) {
    return player.fadeVolume(0.0, 1.0, 1.0);
}

function playGong(player) {
    // Nel web, per il gong, usiamo una sintesi vocale o un suono predefinito se non carichiamo un file gong.mp3
    // Per semplicità e per non forzare l'utente a caricare un file extra per il gong,
    // usiamo l'API Web Audio per generare un "BEEP" di fine prova!
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioCtx.createOscillator();
    const gainNode = audioCtx.createGain();

    oscillator.type = 'sine';
    oscillator.frequency.setValueAtTime(440, audioCtx.currentTime); // Frequenza nota La
    oscillator.frequency.exponentialRampToValueAtTime(110, audioCtx.currentTime + 1); // Scende di tono

    gainNode.gain.setValueAtTime(1, audioCtx.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 1); // Fade out del beep

    oscillator.connect(gainNode);
    gainNode.connect(audioCtx.destination);

    oscillator.start();
    oscillator.stop(audioCtx.currentTime + 1.5);
}