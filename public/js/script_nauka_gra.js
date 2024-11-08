
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
