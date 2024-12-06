from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import os

def get_path(name: str) -> str:
	# Upewniamy się, że ścieżka do katalogu "public/html" jest poprawna
	return os.path.join('public', 'html', name)

PORT: int = 3000

app = FastAPI()

# Montujemy katalog public, żeby obsługiwać statyczne pliki (JS, CSS)
app.mount("/static", StaticFiles(directory="public"), name="public")


global show
show = False
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

@app.get("/nauka/api/data")
def get_info():
	# Zwrot pliku JSON
	return FileResponse(os.path.join('data', 'dane_nauka.json'))
	
@app.get("/nauka/gra")
def nauka_gra():
	location = get_path('nauka_gra.html')
	return FileResponse(location)

@app.get('/backend-status')
def testowy_status():
	global show
	show = not show
	return show
	
@app.post('/api/data')
def kolejny_test():
	return
	

if __name__ == "__main__":
	import uvicorn
	uvicorn.run(app, host="127.0.0.1", port=PORT)
