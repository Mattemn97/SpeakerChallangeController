/**
 * js/modes.js
 * Logica specifica per le singole modalità di prova.
 */

/**
 * Utility per gestire i countdown in modo asincrono.
 * Restituisce una Promise che si risolve quando il timer arriva a 0.
 */
function runTimerAsync(elementId, seconds, colorClass, onTick = null) {
    return new Promise((resolve) => {
        const display = document.getElementById(elementId);
        display.className = `timer-display ${colorClass}`;
        let remaining = seconds;

        display.innerText = formattaTempo(remaining);

        currentTimerInterval = setInterval(() => {
            remaining--;
            if (remaining >= 0) {
                display.innerText = formattaTempo(remaining);
                if (onTick) onTick(remaining); // Esegue callback custom (es. per mostrare news)
            }

            if (remaining <= 0) {
                clearInterval(currentTimerInterval);
                resolve();
            }
        }, 1000);
    });
}

/**
 * Estrae un file casuale dall'input type="file"
 */
function getRandomFileFromInput(inputId) {
    const input = document.getElementById(inputId);
    if (!input.files || input.files.length === 0) {
        alert("Nessun file caricato per questa modalità. Vai in Impostazioni.");
        return null;
    }
    const filesArray = Array.from(input.files);
    return sceltaCasuale(filesArray);
}

// ==========================================
// MODALITÀ: INTERVISTA
// ==========================================
async function startIntervista() {
    stopAll();
    const config = ConfigManager.getConfig();
    const file = getRandomFileFromInput('fileIntervista');
    if (!file) return;

    document.getElementById('trackIntervista').innerText = `IN RIPRODUZIONE: ${estraiNomeFile(file)}`;
    
    globalPlayer.loadSong(file);
    globalPlayer.playSong();
    fadeIn(globalPlayer);

    // Countdown preparazione (15s)
    await runTimerAsync('timerIntervista', 15, 'timer-prep');
    
    fadeOut(globalPlayer);

    // Countdown prova
    await runTimerAsync('timerIntervista', config.intervistaTime, '');

    fadeOut(globalPlayer);
    playGong(globalPlayer);
    document.getElementById('trackIntervista').innerText = "Prova Terminata";
}

// ==========================================
// MODALITÀ: IMPROVVISAZIONE
// ==========================================
async function startImprovvisazione() {
    stopAll();
    const config = ConfigManager.getConfig();
    const file = getRandomFileFromInput('fileImprovvisazione');
    if (!file) return;

    document.getElementById('trackImprovvisazione').innerText = `IN RIPRODUZIONE: ${estraiNomeFile(file)}`;
    
    globalPlayer.loadSong(file);
    globalPlayer.playSong();
    fadeIn(globalPlayer);

    // Decidi quando mostrare la news (tra 1/3 e 2/3 del tempo totale)
    const minNewsTime = Math.floor(config.improvvisazioneTime * 0.3);
    const maxNewsTime = Math.floor(config.improvvisazioneTime * 0.7);
    const triggerNewsSecond = randomInt(minNewsTime, maxNewsTime);

    // Countdown preparazione (15s)
    await runTimerAsync('timerImprovvisazione', 15, 'timer-prep');
    
    fadeOut(globalPlayer);

    // Countdown prova con controllo news
    await runTimerAsync('timerImprovvisazione', config.improvvisazioneTime, '', (sec) => {
        // Se il timer arriva al secondo "trigger", mostra la news
        if (sec === triggerNewsSecond) {
            const result = estraiNewsCasuale(config.newsArray);
            if (result) {
                document.getElementById('newsContent').innerText = result.news;
                document.getElementById('newsDisplay').classList.remove('hidden');
            }
        }
        // Colore rosso negli ultimi 10 secondi
        if (sec <= 10) {
            document.getElementById('timerImprovvisazione').classList.add('timer-warning');
        }
    });

    fadeOut(globalPlayer);
    playGong(globalPlayer);
    document.getElementById('trackImprovvisazione').innerText = "Prova Terminata";
}

// ==========================================
// MODALITÀ: BACK2BACK
// ==========================================
async function startBack2Back() {
    stopAll();
    const config = ConfigManager.getConfig();
    
    const input = document.getElementById('fileBack2Back');
    if (!input.files || input.files.length < 2) {
        alert("Carica almeno 2 brani per il Back2Back nelle Impostazioni.");
        return;
    }

    // Seleziona due brani diversi
    const filesArray = Array.from(input.files);
    const index1 = randomInt(0, filesArray.length - 1);
    let index2 = randomInt(0, filesArray.length - 1);
    while (index1 === index2 && filesArray.length > 1) {
        index2 = randomInt(0, filesArray.length - 1);
    }
    
    const file1 = filesArray[index1];
    const file2 = filesArray[index2];

    const halfTime = Math.floor(config.back2backTime / 2);

    document.getElementById('trackBack2Back').innerText = `ATTUALE: ${estraiNomeFile(file1)}`;
    document.getElementById('trackNextBack2Back').innerText = `SUCCESSIVO: ${estraiNomeFile(file2)}`;

    // Brano 1
    globalPlayer.loadSong(file1);
    globalPlayer.playSong();
    fadeIn(globalPlayer);

    // Countdown prima metà
    await runTimerAsync('timerBack2Back', halfTime, 'timer-prep');
    
    // Cambio Brano
    document.getElementById('timerBack2Back').innerText = "CAMBIO!";
    document.getElementById('timerBack2Back').classList.add('timer-warning');
    
    globalPlayer.loadSong(file2);
    globalPlayer.playSong();
    
    document.getElementById('trackBack2Back').innerText = `ATTUALE: ${estraiNomeFile(file2)}`;
    document.getElementById('trackNextBack2Back').innerText = "SUCCESSIVO: ---";

    // Countdown seconda metà
    await runTimerAsync('timerBack2Back', halfTime, '');

    fadeOut(globalPlayer);
    playGong(globalPlayer);
    document.getElementById('trackBack2Back').innerText = "Prova Terminata";
}

// ==========================================
// MODALITÀ: ARTICOLO
// ==========================================
async function startArticolo() {
    stopAll();
    const config = ConfigManager.getConfig();
    const file = getRandomFileFromInput('fileArticolo');
    if (!file) return;

    document.getElementById('trackArticolo').innerText = `IN RIPRODUZIONE: ${estraiNomeFile(file)}`;
    
    globalPlayer.loadSong(file);
    globalPlayer.playSong();
    fadeIn(globalPlayer);

    // Countdown preparazione (15s)
    await runTimerAsync('timerArticolo', 15, 'timer-prep');
    
    fadeOut(globalPlayer);

    // Countdown prova
    await runTimerAsync('timerArticolo', config.articoloTime, '');

    fadeOut(globalPlayer);
    playGong(globalPlayer);
    document.getElementById('trackArticolo').innerText = "Prova Terminata";
}