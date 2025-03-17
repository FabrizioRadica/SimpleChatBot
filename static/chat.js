document.addEventListener('DOMContentLoaded', function () {

    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const messageArea = document.getElementById('messageArea');

    // Funzione per inviare un messaggio e ottenere risposta dall'API
    async function sendMessage() {
        const messageText = messageInput.value.trim();
        const selectedModel = aiModel;

        if (messageText) {
            // Aggiunge il messaggio dell'utente alla chat
            const messageElement = document.createElement('div');
            messageElement.classList.add('message', 'sent');
            messageElement.textContent = messageText;
            messageArea.appendChild(messageElement);

            // Pulisce l'input
            messageInput.value = '';

            // Mostra indicatore di caricamento
            const loadingElement = document.createElement('div');
            loadingElement.classList.add('loading');
            loadingElement.textContent = `${assistantName} sta scrivendo...`;
            messageArea.appendChild(loadingElement);

            // Scorri verso il basso
            messageArea.scrollTop = messageArea.scrollHeight;

            try {
                // Richiesta all'API
                const response = await fetch(`/generate?api_prompt=${encodeURIComponent(messageText)}&api_model=${selectedModel}`);

                if (!response.ok) {
                    throw new Error('Errore nella richiesta API');
                }

                const aiResponse = await response.text();

                // Rimuove l'indicatore di caricamento
                messageArea.removeChild(loadingElement);

                // Aggiunge la risposta dell'AI
                const responseElement = document.createElement('div');
                responseElement.classList.add('message', 'received');
                responseElement.textContent = aiResponse;
                messageArea.appendChild(responseElement);

            } catch (error) {
                // Rimuove l'indicatore di caricamento
                messageArea.removeChild(loadingElement);

                // Mostra messaggio di errore
                const errorElement = document.createElement('div');
                errorElement.classList.add('message', 'received');
                errorElement.textContent = 'Mi dispiace, si è verificato un errore nella comunicazione. Riprova più tardi.';
                messageArea.appendChild(errorElement);
                console.error('Errore:', error);
            }

            // Scorri verso il basso per mostrare la risposta
            messageArea.scrollTop = messageArea.scrollHeight;
        }
    }

    // Event listener per il pulsante di invio
    sendButton.addEventListener('click', sendMessage);

    // Event listener per il tasto Enter nell'input
    messageInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});