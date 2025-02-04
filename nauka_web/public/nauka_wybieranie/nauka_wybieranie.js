// Funkcja ładująca dane z API i generująca checkboxy
async function loadCheckboxes() {
	try {
	  const response = await fetch('/api/nauka/data');
	  if (!response.ok) {
		throw new Error(`Błąd HTTP: ${response.status}`);
	  }
  
	  // Pobierz obiekt JSON i uzyskaj listę kluczy
	  const data = await response.json();
	  const keys = Object.keys(data); // Lista kluczy obiektu
  
	  // Znajdź kontener do dodawania checkboxów
	  const container = document.getElementById('checkboxContainer');
	  container.innerHTML = ''; // Czyszczenie kontenera
  
	  // Generowanie checkboxów na podstawie kluczy obiektu
	  keys.forEach((key, index) => {
		// Tworzymy główny kontener wiersza
		const row = document.createElement('div');
		row.className = 'checkbox-row';
  
		// Tworzymy label, który będzie opakowywał checkbox, niestandardowy kwadrat i tekst
		const label = document.createElement('label');
		label.className = 'checkbox-label';
		label.htmlFor = `checkbox-${index}`;
  
		// Tworzymy input typu checkbox
		const checkbox = document.createElement('input');
		checkbox.type = 'checkbox';
		checkbox.id = `checkbox-${index}`;
		checkbox.checked = false;
		checkbox.dataset.key = key;
  
		// Tworzymy niestandardowy kwadrat checkboxa
		const customCheckbox = document.createElement('div');
		customCheckbox.className = 'checkbox-custom';
  
		// Tworzymy element tekstowy dla etykiety
		const textSpan = document.createElement('span');
		textSpan.className = 'checkbox-text';
		textSpan.textContent = key;
  
		// Dodajemy wszystkie elementy do labela (kolejność ma znaczenie: input, custom checkbox, tekst)
		label.appendChild(checkbox);
		label.appendChild(customCheckbox);
		label.appendChild(textSpan);
  
		// Dodajemy label do wiersza
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
	if (!areAnyCheckboxesChecked()) {
	  alert('Musisz wybrać przynajmniej jeden checkbox!');
	  return;
	}
  
	const user = document.querySelector('.user').value;
	if (!user) {
	  alert('Nazwa użytkownika nie może być pusta!');
	  return;
	}
  
	try {
	  const userExists = await user_exist(user);
	  if (!userExists) {
		alert('Nieprawidłowa nazwa użytkownika! Spróbuj ponownie.');
		return;
	  }
  
	  const status = getCheckboxStatus();
	  const params = new URLSearchParams();
  
	  Object.keys(status).forEach(key => {
		params.append(key, status[key]);
	  });
  
	  params.append("user", user);
	  window.location.href = `/nauka/gra?${params.toString()}`;
	} catch (error) {
	  console.error('Błąd podczas sprawdzania użytkownika:', error);
	  alert('Wystąpił błąd. Spróbuj ponownie później.');
	}
  }
  
  async function user_exist(user) {
	try {
	  const response = await sendRequest({ user }, "POST", "/api/nauka/user_exist");
	  return response.exists;
	} catch (error) {
	  console.error('Błąd podczas sprawdzania użytkownika:', error);
	  return false;
	}
  }
  
  async function sendRequest(data, method, url) {
	try {
	  const options = {
		method,
		headers: { 'Content-Type': 'application/json' },
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

  async function loadVersion() {
    try {
        const response = await fetch('/version');
        if (!response.ok) throw new Error(`Błąd HTTP: ${response.status}`);
        const data = await response.json();
        document.getElementById('version').textContent = `Wersja: ${data.version}`;
    } catch (error) {
        console.error('Błąd ładowania wersji:', error);
        document.getElementById('version').textContent = 'Wersja: brak danych';
    }
}

document.addEventListener('DOMContentLoaded', loadVersion);

  
  // Inicjalizacja po załadowaniu dokumentu
  document.addEventListener('DOMContentLoaded', loadCheckboxes);
  document.getElementById('getCheckboxStatus').addEventListener('click', redirectToGame);
  document.getElementById('addModuleButton').addEventListener('click', function() {
	window.location.href = '/nauka/add_module';
  });
  