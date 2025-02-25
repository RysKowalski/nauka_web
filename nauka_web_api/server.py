from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from fastapi.responses import FileResponse

import os
import json
import httpx

from typing import Dict, Union, List

from nauka_web_api.backend import gra
from nauka_web_api.backend.new_module_validation import validate_dict_structure
from nauka_web_api.backend.save_new_module import save_new_module
from nauka_web_api.backend import admin, login_stuff

router: APIRouter = APIRouter()

@router.get("/auth/callback")
async def auth_callback(code: str, response: Response):
	return await login_stuff.auth_callback(code, response)

@router.get("/api/nauka/data")
def get_info():
    # Ścieżka do pliku
    file_path = os.path.join('nauka_web_api', 'backend', 'data', 'nauka_questions.json')
    
    # Tworzymy odpowiedź FileResponse
    response = FileResponse(file_path)
    
    # Dodajemy nagłówek Cache-Control
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, proxy-revalidate"
    
    return response

@router.post("/api/nauka/user_exist")
def user_exist(user: dict):
	print(user)
	with open(os.path.join('nauka_web_api', "backend", "data", "nauka_user_data.json"), "r") as plik:
		user_exists = user["user"] in json.load(plik)
		return {"exists": user_exists}  # Zwróć obiekt JSON

@router.post('/api/nauka/init')
def nauka_init(data: Dict[str, List[str]], api_key: str = Cookie(None)):
	user: str = login_stuff.get_username(api_key)
	chances: list[str] = data["chances"]

	print(data)
	instancje_gry.new_instance(user, chances)
	
	updated_dict: dict = instancje_gry.instances[user].get_data()
	return updated_dict

@router.post('/api/nauka/move')
def nauka_move(data: dict, api_key: str = Cookie(None)) -> dict:
	user: str = login_stuff.get_username(api_key)
	answer_time: float = float(data['time'])
	answer: bool = data["answer"]

	print(data)

	instancje_gry.instances[user].move(answer, answer_time)

	updated_dict: dict = instancje_gry.instances[user].get_data()
	return updated_dict

@router.post('/api/nauka/submit')
def submit_new_module(data: dict, api_key: str = Cookie(None)):
	print(data)
	validated_data: dict = validate_dict_structure(data, api_key)
	if validated_data['error']:
		return validated_data
	
	data['username'] = login_stuff.get_user_status(api_key)['global_name']
	save_new_module(data)
	
	return {'error': False, 'error_message': 'Udało się zapisać nowy moduł'}

@router.post('/api/nauka/add_user')
def add_user(data: Dict[str, str], api_key: str = Depends(admin.authenticate)):
	username = data.get('username')
	if not username:
		raise HTTPException(status_code=400, detail="Username is required")

	return admin.add_user(username)

@router.delete('/api/nauka/remove_user')
def remove_user(data: Dict[str, str], api_key: str = Depends(admin.authenticate)):
	username = data.get('username')
	if not username:
		raise HTTPException(status_code=400, detail="Username is required")

	return admin.remove_user(username)

@router.delete('/api/nauka/remove_module')
def remove_module(data: Dict[str, str], api_key: str = Depends(admin.authenticate)):
	module_name = data.get('module_name')
	if not module_name:
		raise HTTPException(status_code=400, detail="Username is required")

	return admin.remove_module(module_name)

@router.get('/api/get_user_status')
def is_logged(api_key: str = Cookie(None)):
	logged: dict = login_stuff.get_user_status(api_key)
	return logged

instancje_gry: gra.Instances = gra.Instances()

if __name__ == "__main__":
	PORT: int = 3001
	import uvicorn

	uvicorn.run(router, host="127.0.0.1", port=PORT)