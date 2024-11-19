const express = require('express');
const path = require('path');
const app = express();

const PORT = process.env.PORT || 3000;

// Ustawienie folderu "public" jako głównego folderu na pliki statyczne
app.use(express.static(path.join(__dirname, 'public')));

// Obsługa trasy głównej "/"
app.get('/', (req, res) => {
	res.sendFile(__dirname + "/public/html/index.html");
  });

app.get('/nauka/wybieranie', (req, res) => {
	res.sendFile(__dirname + "/public/html/nauka_wybieranie.html")
  })

app.get('/nauka/api/data', (req,   res) => {
	res.sendFile(__dirname + "/data/dane_nauka.json")
})

app.get('/nauka/gra', (req,   res) => {
	res.sendFile(__dirname + "/public/html/nauka_gra.html")
})

app.listen(PORT, () => {
	console.log(`Serwer działa na http://localhost:${PORT}`);
  });

let showElement = true;

app.get('/backend-status', (req, res) => {
	res.json({ showElement })
});

app.post('/api/data', (req, res) => {
    // Odczytanie wartości z JSON-a
    const showElement = req.body.key;

    // Sprawdzenie typu danych i przypisanie
    if (typeof booleanValue === 'boolean') {
        console.log(`Otrzymano wartość bool: ${booleanValue}`);
        res.status(200).send({ success: true, receivedValue: booleanValue });
    } else {
        console.log('Nieprawidłowy typ danych!');
        res.status(400).send({ success: false, message: 'Oczekiwano wartości boolean!' });
    }
});