/**
 * js/main.js
 * Controller principale dell'interfaccia utente (Tabs e Inizializzazione).
 */

// Variabile globale per tenere traccia dei timer (setInterval) attivi
let currentTimerInterval = null;

/**
 * Gestisce il cambio delle schede (Tabs) basato su W3.CSS.
 */
function openTab(evt, tabName) {
    // 1. Ferma eventuali prove in corso quando si cambia scheda
    stopAll();

    let i, tabcontent, tablinks;
    
    // 2. Nasconde tutti i contenuti delle schede
    tabcontent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    
    // 3. Rimuove il colore attivo (w3-red) da tutti i bottoni
    tablinks = document.getElementsByClassName("tablink");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" w3-red", "");
    }
    
    // 4. Mostra la scheda corrente e aggiunge il colore attivo al bottone cliccato
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " w3-red";
}

/**
 * Ferma tutto: Audio, Fade e Timer.
 * Equivale a un reset di sicurezza.
 */
function stopAll() {
    globalPlayer.stopSong();
    
    if (currentTimerInterval) {
        clearInterval(currentTimerInterval);
        currentTimerInterval = null;
    }

    // Nascondi eventuali popup delle news
    const newsDisplay = document.getElementById("newsDisplay");
    if (newsDisplay) newsDisplay.classList.add("hidden");
    
    // Ripristina l'aspetto dei timer
    const timers = document.querySelectorAll(".timer-display");
    timers.forEach(t => {
        t.innerText = "00:00";
        t.className = "timer-display"; // resetta i colori
    });
}

// Inizializzazione al caricamento della pagina
document.addEventListener('DOMContentLoaded', () => {
    // Carica le configurazioni salvate
    ConfigManager.loadConfig();

    // Collega l'evento di salvataggio al form
    document.getElementById('configForm').addEventListener('submit', (e) => {
        e.preventDefault();
        ConfigManager.saveConfig();
        alert('Impostazioni salvate con successo!');
    });
});