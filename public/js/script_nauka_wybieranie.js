// Funkcja ładująca dane z API i generująca checkboxy
async function loadCheckboxes() {
	try {
	  const response = await fetch('/nauka/api/list');
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
		const checkbox = document.createElement('input');
		checkbox.type = 'checkbox';
		checkbox.id = `checkbox-${index}`;
		checkbox.checked = false; // Domyślnie odznaczone
		checkbox.dataset.key = key; // Przypisanie nazwy klucza jako atrybutu
  
		const label = document.createElement('label');
		label.htmlFor = checkbox.id;
		label.textContent = key; // Ustaw nazwę klucza jako tekst etykiety
  
		// Dodanie checkboxa i etykiety do kontenera
		container.appendChild(checkbox);
		container.appendChild(label);
		container.appendChild(document.createElement('br')); // Nowa linia
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
function redirectToGame() {
	if (!areAnyCheckboxesChecked()) {
		alert('Musisz wybrać przynajmniej jeden checkbox!');
		return; // Jeśli żaden checkbox nie jest zaznaczony, nie robimy nic
	}

	const status = getCheckboxStatus();
	const params = new URLSearchParams();

	// Dodaj status checkboxów jako parametry URL
	Object.keys(status).forEach(key => {
		params.append(key, status[key]);
	});

	// Przekierowanie na stronę /nauka/gra z parametrami
	window.location.href = `/nauka/gra?${params.toString()}`;
}

// Wywołanie funkcji po załadowaniu dokumentu
document.addEventListener('DOMContentLoaded', loadCheckboxes);

// Dodanie nasłuchiwacza zdarzeń do przycisku
document.getElementById('getCheckboxStatus').addEventListener('click', redirectToGame);
