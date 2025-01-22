// Klasa do zarządzania licznikiem
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

function answer(show, text) {
	const element = document.getElementById('answer');
	if (show) {
		element.classList.add('visible');
		element.classList.remove('hidden');
	} else {
		element.classList.add('hidden');
		element.classList.remove('visible');
	}
	element.textContent = text;
}

function question(text) {
	const element = document.getElementById('question');
	element.textContent = text;
}

function points(number) {
	const element = document.getElementById('points');
	element.textContent = 'punkty: ' + number;
}

function max_points(number) {
	const element = document.getElementById('max_points');
	element.textContent = 'Najwięcej punktów: ' + number;
}

function done_button(show) {
	const element = document.getElementById('done_button');
	if (show) {
		element.classList.add('visible');
		element.classList.remove('hidden');
	} else {
		element.classList.add('hidden');
		element.classList.remove('visible');
	}
}

function user_choice_buttons(show) {
	const element = document.getElementById('button_wrong');
	const element2 = document.getElementById('button_correct');
	if (show) {
		element.classList.add('visible');
		element.classList.remove('hidden');
		
		element2.classList.add('visible');
		element2.classList.remove('hidden');
	} else {
		element.classList.add('hidden');
		element.classList.remove('visible');
		
		element2.classList.add('hidden');
		element2.classList.remove('visible');
	}
}

function updateChances(data) {
	const chancesElement = document.getElementById('chances');
	chancesElement.innerHTML = '';
	const list = document.createElement('ul');
	for (const [key, value] of Object.entries(data)) {
		const listItem = document.createElement('li');
		listItem.textContent = `${key}: ${value}`;
		list.appendChild(listItem);
	}
	chancesElement.appendChild(list);
}

async function sendRequest(data, method, url) {
	try {
		const options = {
			method,
			headers: {
				'Content-Type': 'application/json',
			},
		};
		if (method === 'POST') options.body = JSON.stringify(data);
		const response = await fetch(url, options);
		if (!response.ok) {
			throw new Error(`HTTP error! Status: ${response.status}`);
		}
		const jsonResponse = await response.json();
		console.log('Odpowiedź z serwera:', jsonResponse);
		return jsonResponse;
	} catch (error) {
		console.error('Błąd podczas wysyłania żądania:', error);
		throw error;
	}
}

function get_arguments() {
    // Pobierz aktualny URL
    const url = new URL(window.location.href);

    // Odczytaj parametry zapytania
    const params = new URLSearchParams(url.search);

    // Zwróć listę kluczy, które mają wartość 'true'
    const trueArguments = [];
    params.forEach((value, key) => {
        if (value === 'true') {
            trueArguments.push(key);
        }
    });

    // Pobierz parametr 'user' (jeśli istnieje)
    const user = [params.get("user")];

    // Zwróć obiekt z wynikami
    return {
        chances: trueArguments,
        user: user
    };
}


async function init() {
	try {
		points(0);
		max_points(0);
		question('Brak pytania')
		answer(false, 'odpowiedź nie załadowana')
		updateChances({'brak': 0})
		done_button(true)
		user_choice_buttons(false)
		const data = await sendRequest(get_arguments(), 'POST', '/api/nauka/init');
		if (data) {
			max_points(data.max_points);
			question(data.question)
			answer(data.show_answer, data.answer)
			updateChances(data.element_list)
		}
	} catch (error) {
		console.error('Błąd inicjalizacji:', error);
		showError('Nie udało się załadować danych początkowych.');
	}
}

document.addEventListener('DOMContentLoaded', init);

const timer = new Timer();
timer.start();
