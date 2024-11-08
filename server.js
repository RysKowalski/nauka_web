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

app.get('/nauka/api/list', (req,   res) => {
	res.sendFile(__dirname + "/data/dane_nauka.json")
})

app.get('/nauka/gra', (req,   res) => {
	res.sendFile(__dirname + "/public/html/nauka_gra.html")
})

app.listen(PORT, () => {
	console.log(`Serwer działa na http://localhost:${PORT}`);
  });