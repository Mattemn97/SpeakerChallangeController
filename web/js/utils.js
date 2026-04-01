/**
 * js/utils.js
 * Funzioni di utilità generale per Speaker Challenge.
 */

/**
 * Converte i secondi in formato MM:SS.
 * @param {number} secondi - Numero di secondi da formattare.
 * @returns {string} Stringa nel formato MM:SS (es. "01:30").
 */
function formattaTempo(secondi) {
    // Ci assicuriamo che i secondi siano un numero intero positivo o zero
    secondi = Math.max(0, Math.floor(secondi));
    const minuti = Math.floor(secondi / 60);
    const secondiRestanti = secondi % 60;
    
    // padStart aggiunge lo zero iniziale se il numero è a una sola cifra (es. 9 -> "09")
    const minStr = String(minuti).padStart(2, '0');
    const secStr = String(secondiRestanti).padStart(2, '0');
    
    return `${minStr}:${secStr}`;
}

/**
 * Estrae il nome del file senza l'estensione.
 * In JavaScript lavoriamo con l'oggetto File, quindi leggiamo direttamente la proprietà name.
 * @param {File} file - L'oggetto File caricato dall'utente.
 * @returns {string} Nome del file pulito dall'estensione.
 */
function estraiNomeFile(file) {
    if (!file || !file.name) return "Audio Sconosciuto";
    // Rimuove l'estensione finale (es. .mp3, .wav)
    return file.name.replace(/\.[^/.]+$/, "");
}

/**
 * Genera un numero intero casuale compreso tra min e max (inclusi).
 * Sostituisce random.randint() di Python.
 * @param {number} min - Valore minimo.
 * @param {number} max - Valore massimo.
 * @returns {number} Intero casuale.
 */
function randomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

/**
 * Seleziona un elemento casuale da un array.
 * Sostituisce random.choice() di Python.
 * @param {Array} array - L'array da cui pescare.
 * @returns {*} Un elemento casuale dell'array.
 */
function sceltaCasuale(array) {
    if (!array || array.length === 0) return null;
    const indice = randomInt(0, array.length - 1);
    return array[indice];
}

/**
 * Estrae una news casuale da un array e la rimuove (per non ripeterla).
 * Ritorna un oggetto con la news estratta e l'array aggiornato.
 * @param {string[]} newsArray - Array di stringhe contenenti le news.
 * @returns {Object|null} { news: string, remainingNews: string[] }
 */
function estraiNewsCasuale(newsArray) {
    if (!newsArray || newsArray.length === 0) return null;
    
    const indice = randomInt(0, newsArray.length - 1);
    const newsEstratta = newsArray[indice];
    
    // Crea un nuovo array senza l'elemento estratto
    const remainingNews = [...newsArray];
    remainingNews.splice(indice, 1);
    
    return { news: newsEstratta, remainingNews: remainingNews };
}