from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from typing import Dict
import json

import os

def get_path(name: str) -> str:
	# Upewniamy się, że ścieżka do katalogu "public/html" jest poprawna
	return os.path.join('public', 'html', name)

app: FastAPI = FastAPI()

# Montujemy katalog public, żeby obsługiwać statyczne pliki (JS, CSS)
app.mount("/static", StaticFiles(directory="public"), name="public")

@app.get("/")
def home():
	# Zwrot głównego pliku HTML
	location = get_path('index.html')
	return FileResponse(location)

@app.get("/nauka/wybieranie")
def nauka_wybieranie():
	# Zwrot pliku HTML dla nauka/wybieranie
	location = get_path('nauka_wybieranie.html')
	return FileResponse(location)
	
@app.get("/nauka/gra")
def nauka_gra():
	location = get_path('nauka_gra.html')
	return FileResponse(location)

if __name__ == "__main__":
	import uvicorn

	PORT: int = 3000

	uvicorn.run(app, host="127.0.0.1", port=PORT)
