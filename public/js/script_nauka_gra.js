// Klasa do zarządzania licznikiem
class Timer {
	constructor() {
		this.time = 0; // Czas w dziesiątych częściach sekundy
		this.interval = null; // ID interwału
	}
	// Rozpocznij licznik
	start() {
		console.log('started timer in')
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
		element.textContent = this.getTime() + 's'
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

function done_button(show) {
	const element = document.getElementById('done_button')
	if (show) {
		element.classList.add('visible');
		element.classList.remove('hidden');
	  } else {
		element.classList.add('hidden');
		element.classList.remove('visible');
	  }
}

function user_choice_buttons(show) {
	const element = document.getElementById('button_wrong')
	const element2 = document.getElementById('button_correct')
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
	// Get the DOM element where the list will be displayed
	const chancesElement = document.getElementById('chances');

	// Clear the existing content of the element
	chancesElement.innerHTML = '';

	// Create a list element
	const list = document.createElement('ul');

	// Iterate through the dictionary and add list items
	for (const [key, value] of Object.entries(data)) {
		const listItem = document.createElement('li');
		listItem.textContent = `${key}: ${value}`;
		list.appendChild(listItem);
	}

	// Append the list to the chances element
	chancesElement.appendChild(list);
}

async function sendRequest(data, method, url) {
	try {
		if (method = 'GET') {
			const response = await fetch(url, {
				method: 'GET'
				});

				// Sprawdzanie, czy odpowiedź jest w porządku
				if (!response.ok) {
					throw new Error(`HTTP error! Status: ${response.status}`);
				}

				// Odczytanie odpowiedzi w formacie JSON
				const jsonResponse = await response.json();

				// Zwrócenie odpowiedzi lub dalsze przetwarzanie
				console.log('Odpowiedź z serwera:', jsonResponse);

				return jsonResponse;
		} else { const response = await fetch(url, {
				method: 'POST', // Typ żądania
				headers: {
					'Content-Type': 'application/json' // Typ treści
				},
				body: JSON.stringify(data) // Konwersja danych na format JSON
				});

				// Sprawdzanie, czy odpowiedź jest w porządku
				if (!response.ok) {
					throw new Error(`HTTP error! Status: ${response.status}`);
				}

				// Odczytanie odpowiedzi w formacie JSON
				const jsonResponse = await response.json();

				// Zwrócenie odpowiedzi lub dalsze przetwarzanie
				console.log('Odpowiedź z serwera:', jsonResponse);

				return jsonResponse;
			}
		} catch (error) {
			console.error('Błąd podczas wysyłania żądania:', error);
	}

}

function init() {
	data = sendRequest('', 'GET', '/nauka/init')
	console.log(data)
}

document.addEventListener('DOMContentLoaded', init);