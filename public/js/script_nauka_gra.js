// Klasa do zarządzania licznikiem
class Timer {
	constructor(updateCallback) {
		this.time = 0; // Czas w dziesiątych częściach sekundy
		this.interval = null; // ID interwału
		this.updateCallback = updateCallback; // Funkcja aktualizacji widoku
	}
	// Rozpocznij licznik
	start() {
		if (this.interval) return; // Jeśli już działa, nie uruchamiaj ponownie
		this.interval = setInterval(() => {
			this.time += 1; // Dodaj 0.1 sekundy
			this.update(); // Aktualizuj widok
		}, 100);
	}

	// Zatrzymaj licznik
	pause() {
		clearInterval(this.interval);
		this.interval = null;
	}

	// Ustaw licznik na określoną wartość
	set(timeInSeconds) {
		this.time = Math.round(timeInSeconds * 10); // Konwertuj sekundy na dziesiąte części sekundy
		this.update();
	}

	// Zwróć czas w formacie sekundowym z dokładnością do 0.1 sekundy
	getTime() {
		return (this.time / 10).toFixed(1);
	}

	// Aktualizuj widok
	update() {
		if (this.updateCallback) {
			this.updateCallback(this.getTime());
		}
	}
}

// Funkcja aktualizacji wyświetlania w HTML
const displayElement = document.getElementById('timer');

const timer = new Timer((time) => {
	displayElement.textContent = `Czas: ${time}s`; // Zaktualizuj tekst w elemencie
});

// Przykład: start licznika
timer.start(); // Rozpocznij licznik

// Przykładowe działania: zatrzymanie po 5 sekundach, ustawienie na 10.5 s, ponowne uruchomienie
setTimeout(() => {
	timer.pause(); // Zatrzymaj licznik po 5 sekundach
	timer.set(10.5); // Ustaw czas na 10.5 sekundy
	timer.start(); // Rozpocznij licznik od nowej wartości
}, 5000); // Po 5 sekundach

function answer(show, text) {
	console.log('gówno')
	const element = document.getElementById('answer');
	if (show) {
		element.classList.add('visible');
		element.classList.remove('hidden');
	  } else {
		element.classList.add('hidden');
		element.classList.remove('visible');
	  }
	element.textContent = text
}

function question(text) {
	const element = document.getElementById('question');
	element.textContent = text
}

function points(number) {
	const element = document.getElementById('points');
	element.textContent = 'punkty: ' + number
}

function max_points(number) {
	const element = document.getElementById('max_points');
	element.textContent = 'Najwięcej punktów: ' + number
}

function init() {
	answer(true, 'test')
	question('testowe pytanie')
	points(3)
	max_points(5)
}

document.addEventListener('DOMContentLoaded', init);