
window.onload = function() {
	// Pobranie parametrów z URL
	const urlParams = new URLSearchParams(window.location.search);

	// Obiekt, który będzie przechowywał wszystkie parametry
	let paramsList = [];

	// Funkcja do konwersji wartości na boolean
	function toBoolean(value) {
	  if (value === "true") return true;
	  if (value === "false") return false;
	  return value; // Jeśli wartość nie jest "true" ani "false", zwróci ją taką, jaka jest
	}

	// Iterowanie przez wszystkie parametry
	urlParams.forEach((value, key) => {
	  // Dekodowanie wartości, jeśli są zakodowane
	  let decodedKey = decodeURIComponent(key);
	  let decodedValue = decodeURIComponent(value);

	  // Przekonwertowanie wartości na boolean, jeśli to możliwe
	  let finalValue = toBoolean(decodedValue);

	  // Dodanie do listy jako obiekt
	  paramsList.push({ key: decodedKey, value: finalValue });

	  // Możesz również wyświetlić je w konsoli
	  console.log(decodedKey + ": " + finalValue);
	});

	// Wyświetlanie wyników na stronie
	let output = '<ul>';
	paramsList.forEach(param => {
	  output += `<li><strong>${param.key}:</strong> ${param.value}</li>`;
	});
	output += '</ul>';
	document.getElementById('output').innerHTML = output;
  }

async function checkBackendVariable() {
	try {
		// Symulacja żądania do backendu
		const response = await fetch('/backend-status'); // Ustaw swój endpoint
		const data = await response.json();

		// Zmienna sterująca
		const showElement = data.showElement;

		// Wyświetl/ukryj element na podstawie zmiennej
		const element = document.getElementById('dynamicElement');
		element.style.display = showElement ? 'block' : 'none';
	} catch (error) {
		console.error('Error fetching backend variable:', error);
	}
}

// Sprawdzaj wartość co 2 sekundy
setInterval(checkBackendVariable, 2000);

function handleClick() {
	fetch('/api/data', {
		method: 'POST', // Możesz użyć 'GET', 'PUT', 'DELETE' itp.
		headers: {
		  'Content-Type': 'application/json'
		},
		body: JSON.stringify({ key: true }) // Dane wysyłane w żądaniu
	  })
  }