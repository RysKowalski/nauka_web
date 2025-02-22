from fastapi import APIRouter
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from typing import Dict
import json

import os

def get_path(name: str) -> str:
	return os.path.join("nauka_web", "public", name, name + ".html")

router: APIRouter = APIRouter()

@router.get("/")
def home():
	# Zwrot głównego pliku HTML
	# location = get_path('index')
	# return FileResponse(location)
	return RedirectResponse(url="/nauka/wybieranie", headers={"Cache-Control": "no-cache, no-store, must-revalidate"})

@router.get("/nauka/add_module")
def nauka_add_modules():
	location = get_path('nauka_add_modules')
	return FileResponse(location)

@router.get("/nauka/wybieranie")
def nauka_wybieranie():
	# Zwrot pliku HTML dla nauka/wybieranie
	location = get_path('nauka_wybieranie')

	response = FileResponse(location)
	response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, proxy-revalidate"

	return response
	
@router.get("/nauka/gra")
def nauka_gra():
	location = get_path('nauka_gra')
	return FileResponse(location)

if __name__ == "__main__":
	import uvicorn

	PORT: int = 3000

	uvicorn.run(router, host="127.0.0.1", port=PORT)
