/**
 * js/config.js
 * Gestione delle impostazioni dell'app e salvataggio nel Local Storage.
 */

const ConfigManager = {
    // Nomi delle chiavi per il localStorage
    keys: {
        timeIntervista: 'sc_timeIntervista',
        timeImprovvisazione: 'sc_timeImprovvisazione',
        newsText: 'sc_newsText',
        timeBack2Back: 'sc_timeBack2Back',
        timeArticolo: 'sc_timeArticolo'
    },

    /**
     * Salva i valori attuali degli input nel localStorage.
     */
    saveConfig: function() {
        localStorage.setItem(this.keys.timeIntervista, document.getElementById('timeIntervista').value);
        localStorage.setItem(this.keys.timeImprovvisazione, document.getElementById('timeImprovvisazione').value);
        localStorage.setItem(this.keys.newsText, document.getElementById('newsTextarea').value);
        localStorage.setItem(this.keys.timeBack2Back, document.getElementById('timeBack2Back').value);
        localStorage.setItem(this.keys.timeArticolo, document.getElementById('timeArticolo').value);
    },

    /**
     * Carica i valori dal localStorage e popola gli input (se esistono).
     */
    loadConfig: function() {
        if (localStorage.getItem(this.keys.timeIntervista)) {
            document.getElementById('timeIntervista').value = localStorage.getItem(this.keys.timeIntervista);
        }
        if (localStorage.getItem(this.keys.timeImprovvisazione)) {
            document.getElementById('timeImprovvisazione').value = localStorage.getItem(this.keys.timeImprovvisazione);
        }
        if (localStorage.getItem(this.keys.newsText)) {
            document.getElementById('newsTextarea').value = localStorage.getItem(this.keys.newsText);
        }
        if (localStorage.getItem(this.keys.timeBack2Back)) {
            document.getElementById('timeBack2Back').value = localStorage.getItem(this.keys.timeBack2Back);
        }
        if (localStorage.getItem(this.keys.timeArticolo)) {
            document.getElementById('timeArticolo').value = localStorage.getItem(this.keys.timeArticolo);
        }
    },

    /**
     * Ottiene le configurazioni attuali come oggetto (simile al dict Python).
     */
    getConfig: function() {
        return {
            intervistaTime: parseInt(document.getElementById('timeIntervista').value) || 30,
            improvvisazioneTime: parseInt(document.getElementById('timeImprovvisazione').value) || 60,
            newsArray: document.getElementById('newsTextarea').value.split('\n').filter(line => line.trim() !== ''),
            back2backTime: parseInt(document.getElementById('timeBack2Back').value) || 60,
            articoloTime: parseInt(document.getElementById('timeArticolo').value) || 45
        };
    }
};