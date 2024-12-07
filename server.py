from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import os

def get_path(name: str) -> str:
	# Upewniamy się, że ścieżka do katalogu "public/html" jest poprawna
	return os.path.join('public', 'html', name)

PORT: int = 3000

app: FastAPI = FastAPI()

# Montujemy katalog public, żeby obsługiwać statyczne pliki (JS, CSS)
app.mount("/static", StaticFiles(directory="public"), name="public")


global game
game: dict = {'element_list': {
								'example_name':2137,
								'example_name2':7312
							   },
			'points': 666,
			'max_points': 1234,
			'question': 'ile to 5Σi=3(i+1)',
			'answer': 'skibiditoilet jest zawsze odpowiedzią',
			'time':10,
			'show_done': True,
			'show_answer': True,
			'show_user_answer': True
			}

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
	
@app.post('/nauka/api/gra')
def kolejny_test(data: dict):
	print(data)

	updated_dict: dict = {'element_list': {
										'example_name':2137,
										'example_name2':7312
									   },
						'points': 666,
						'max_points': 1234,
						'question': 'ile to 5Σi=3(i+1)',
						'answer': 'skibiditoilet jest zawsze odpowiedzią',
						'time':10,
						'show_done': True,
						'show_answer': True,
						'show_user_answer': True
						}
	return updated_dict

#@app.get('/nauka/api/get_data')


if __name__ == "__main__":
	import uvicorn
	uvicorn.run(app, host="127.0.0.1", port=PORT)
