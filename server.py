from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from typing import Dict
import json

import os

import backend
import backend.gra

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

@app.get("/nauka/api/data")
def get_info():
	# Zwrot pliku JSON
	return FileResponse(os.path.join('backend', 'data', 'nauka_questions.json'))
	
@app.get("/nauka/gra")
def nauka_gra():
	location = get_path('nauka_gra.html')
	return FileResponse(location)

@app.post("/nauka/user_exist")
def user_exist(user: dict):
	print(user)
	with open(os.path.join("backend", "data", "nauka_user_data.json"), "r") as plik:
		return user["user"] in json.load(plik)

@app.post('/nauka/api/gra')
def kolejny_test(data: dict):
	print(data)

	updated_dict: Dict[str, dict | int | str | bool] = {'element_list': {
										'example_name':2137,
										'example_name2':7312
									   },
						'points': 666,
						'max_points': 1234,
						'question': 'ile to 5Σdi=3(i+1)',
						'answer': 'skibiditoilet jest zawsze odpowiedzią',
						'time':10,
						'show_done': True,
						'show_answer': True,
						'show_user_answer': True
						}
	return updated_dict

@app.post('/nauka/init')
def nauka_init(chances: list[str]):
	print(chances)
	updated_dict: dict = {'element_list': {
										'example_name':213774872334,
										'example_name2':7312
									   },
						'max_points': 1234,
						'question': 'ile to 5Σi=3(i+1)',
						'answer': 'skibiditoilet nie jest zawsze odpowiedzią',
						'show_done': True,
						'show_answer': True,
						'show_user_answer': True
						}
	return updated_dict

if __name__ == "__main__":
	import uvicorn

	PORT: int = 3000

	uvicorn.run(app, host="127.0.0.1", port=PORT)
