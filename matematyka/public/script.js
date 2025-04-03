class Timer {
	constructor() {
		this.time = 0; // Czas w dziesiątych częściach sekundy
		this.interval = null; // ID interwału
	}
	// Rozpocznij licznik
	start() {
		console.log('started timer in');
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
		const element = document.getElementById('timer');
		element.textContent = this.getTime() + 's';
	}
}

async function request(endpoint, metoda, dane) {
	const opcje = {
		method: metoda,
		headers: {
			'Content-Type': 'application/json'
		}
	};

	if (metoda === 'POST') {
		opcje.body = JSON.stringify(dane);
	}

	try {
		const response = await fetch(endpoint, opcje);
		if (!response.ok) {
			throw new Error('Błąd HTTP: ${response.status}');
		}
		return await response.json();
	} catch (error) {
		console.error('Błąd: ', error);
		return null
	}
}

timer = new Timer()

async function load_question() {
	answer = await request('/generate', 'GET', {})
	question = answer['question']

	document.getElementById("question").innerText = question
}

async function user_answer() {
	answer = document.getElementById("answer").value
	document.getElementById("answer").value = ''

	answer = await request('/move', 'POST', {answer: answer})

	correct = answer['answer']

	await load_question()
	answer = await request('/moves', 'GET', {})
	moves = answer['moves']
	document.getElementById("question").innerText = document.getElementById("question").innerText + ' ' + correct + '    ' + moves
}

async function init() {
	await request('/start', 'GET', {})
	load_question()

	timer.start()
}

document.addEventListener("DOMContentLoaded", init)
document.getElementById('answer').addEventListener('keydown', function(event) {
	if (event.key === 'Enter') {
		user_answer()
	}
})
