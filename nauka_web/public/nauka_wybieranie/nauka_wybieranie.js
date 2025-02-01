// Funkcja ładująca dane z API i generująca checkboxy
async function loadCheckboxes() {
	try {
	  const response = await fetch('/api/nauka/data');
	  if (!response.ok) {
		throw new Error(`Błąd HTTP: ${response.status}`);
	  }
	  
	  // Pobierz obiekt JSON i uzyskaj listę kluczy
	  const data = await response.json();
	  const keys = Object.keys(data); // Pobiera listę kluczy obiektu
  
	  // Znajdź kontener do dodawania checkboxów
	  const container = document.getElementById('checkboxContainer');
	  container.innerHTML = ''; // Wyczyszczenie kontenera
  
	  // Generowanie checkboxów na podstawie kluczy obiektu
	  keys.forEach((key, index) => {
		const row = document.createElement('div');
		row.className = 'checkbox-row';
	  
		const checkbox = document.createElement('input');
		checkbox.type = 'checkbox';
		checkbox.id = `checkbox-${index}`;
		checkbox.checked = false;
		checkbox.dataset.key = key;
	  
		const label = document.createElement('label');
		label.htmlFor = checkbox.id;
		label.textContent = key;
	  
		row.appendChild(checkbox);
		row.appendChild(label);
	  
		container.appendChild(row);
	  });
	} catch (error) {
	  console.error('Błąd ładowania checkboxów:', error);
	}
}

// Funkcja pobierająca status checkboxów
function getCheckboxStatus() {
	const checkboxes = document.querySelectorAll('#checkboxContainer input[type="checkbox"]');
	const status = {};

	checkboxes.forEach(checkbox => {
		status[checkbox.dataset.key] = checkbox.checked;
	});

	return status;
}

// Funkcja sprawdzająca, czy przynajmniej jeden checkbox jest zaznaczony
function areAnyCheckboxesChecked() {
	const checkboxes = document.querySelectorAll('#checkboxContainer input[type="checkbox"]');
	return Array.from(checkboxes).some(checkbox => checkbox.checked);
}

// Funkcja przekierowująca na nową stronę z parametrami w URL

async function redirectToGame() {
	// Sprawdzanie, czy zaznaczono przynajmniej jeden checkbox
	if (!areAnyCheckboxesChecked()) {
		alert('Musisz wybrać przynajmniej jeden checkbox!');
		return;
	}

	// Pobranie nazwy użytkownika z pola input
	const user = document.querySelector('.user').value;
	if (!user) {
		alert('Nazwa użytkownika nie może być pusta!');
		return;
	}

	try {
		// Sprawdzenie, czy użytkownik istnieje
		const userExists = await user_exist(user); // Użycie await
		if (!userExists) {
			alert('Nieprawidłowa nazwa użytkownika! Spróbuj ponownie.');
			return;
		}

		// Pobranie statusów checkboxów
		const status = getCheckboxStatus();
		const params = new URLSearchParams();

		// Dodanie statusu checkboxów jako parametrów URL
		Object.keys(status).forEach(key => {
			params.append(key, status[key]);
		});

		params.append("user", user);

		// Przekierowanie na stronę /nauka/gra z parametrami
		window.location.href = `/nauka/gra?${params.toString()}`;
	} catch (error) {
		console.error('Błąd podczas sprawdzania użytkownika:', error);
		alert('Wystąpił błąd. Spróbuj ponownie później.');
	}
}

async function user_exist(user) {
	try {
		// Wywołanie asynchronicznego żądania
		const response = await sendRequest({ user }, "POST", "/api/nauka/user_exist");
		return response.exists; // Oczekujemy odpowiedzi w formacie { exists: true/false }
	} catch (error) {
		console.error('Błąd podczas sprawdzania użytkownika:', error);
		return false; // Jeśli wystąpił błąd, traktuj użytkownika jako nieistniejącego
	}
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

// Wywołanie funkcji po załadowaniu dokumentu
document.addEventListener('DOMContentLoaded', loadCheckboxes);

// Dodanie nasłuchiwacza zdarzeń do przycisku
document.getElementById('getCheckboxStatus').addEventListener('click', redirectToGame);
