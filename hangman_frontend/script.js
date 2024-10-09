const startButton = document.getElementById('startGame');
const guessButton = document.getElementById('submitGuess');
const gameStatusDisplay = document.getElementById('gameStatus');
const wordDisplay = document.getElementById('wordDisplay');
const incorrectGuessesDisplay = document.getElementById('incorrectGuessesDisplay');
const inputLetter = document.getElementById('inputLetter');

let currentGameId = null;


async function startNewGame() {
    try {
        const response = await fetch('http://127.0.0.1:8000/game/new/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const data = await response.json();
            currentGameId = data.id;
            updateGameStatus("Game started! Let's play!");
            fetchGameState();
        } else {
            updateGameStatus('Failed to start a new game.');
        }
    } catch (error) {
        console.error('Error starting new game:', error);
        updateGameStatus('Error starting new game.');
    }
}


async function fetchGameState() {
    if (!currentGameId) return;

    try {
        const response = await fetch(`http://127.0.0.1:8000/game/${currentGameId}/`); 
        const data = await response.json();

        if (data.state === 'Lost') {
            updateGameStatus('You lost! The word was: ' + data.current_word);
        } else if (data.state === 'Won') {
            updateGameStatus('You won! Great job!');
        } else {
            updateGameStatus(data.state); 
        }
        wordDisplay.textContent = `Word: ${data.current_word}`; 
        incorrectGuessesDisplay.textContent = `Incorrect guesses left: ${data.max_incorrect_guesses - data.incorrect_guesses}`; 
    } catch (error) {
        console.error('Error fetching game state:', error);
    }
}


async function submitGuess() {
    const letter = inputLetter.value;
    if (!currentGameId || !letter) return;

    try {
        const response = await fetch(`http://127.0.0.1:8000/game/${currentGameId}/guess/`, { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ letter })
        });

        if (response.ok) {
            await fetchGameState(); 
            inputLetter.value = ''; 
        } else {
            updateGameStatus('Invalid guess. Please try again.');
        }
    } catch (error) {
        console.error('Error submitting guess:', error);
    }
}


function updateGameStatus(message) {
    gameStatusDisplay.textContent = `Game Status: ${message}`; 
}


startButton.addEventListener('click', startNewGame);
guessButton.addEventListener('click', submitGuess);
