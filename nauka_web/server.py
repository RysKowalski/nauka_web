from fastapi import APIRouter
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from typing import Dict
import json

import os

def get_path(name: str) -> str:
	# Upewniamy się, że ścieżka do katalogu "public/html" jest poprawna
	return os.path.join('public', 'html', name)

router: APIRouter = APIRouter()

@router.get("/")
def home():
	# Zwrot głównego pliku HTML
	location = get_path('index.html')
	return FileResponse(location)

@router.get("/nauka/wybieranie")
def nauka_wybieranie():
	# Zwrot pliku HTML dla nauka/wybieranie
	location = get_path('nauka_wybieranie.html')
	return FileResponse(location)
	
@router.get("/nauka/gra")
def nauka_gra():
	location = get_path('nauka_gra.html')
	return FileResponse(location)

if __name__ == "__main__":
	import uvicorn

	PORT: int = 3000

	uvicorn.run(router, host="127.0.0.1", port=PORT)
