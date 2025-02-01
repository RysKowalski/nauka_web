from fastapi import APIRouter
from fastapi.responses import FileResponse

import os
import json

from typing import Dict, Union, List

from nauka_web_api.backend import gra
from nauka_web_api.backend.new_module_validation import validate_dict_structure
from nauka_web_api.backend.save_new_module import save_new_module

router: APIRouter = APIRouter()

@router.get("/api/nauka/data")
def get_info():
	# Zwrot pliku JSON
	return FileResponse(os.path.join('nauka_web_api', 'backend', 'data', 'nauka_questions.json'))

@router.post("/api/nauka/user_exist")
def user_exist(user: dict):
    print(user)
    with open(os.path.join('nauka_web_api', "backend", "data", "nauka_user_data.json"), "r") as plik:
        user_exists = user["user"] in json.load(plik)
        return {"exists": user_exists}  # Zwróć obiekt JSON

@router.post('/api/nauka/init')
def nauka_init(data: Dict[str, List[str]]):
	user: str = data["user"][0]
	chances: list[str] = data["chances"]

	print(data)
	instancje_gry.new_instance(user, chances)
	
	updated_dict: dict = instancje_gry.instances[user].get_data()
	return updated_dict

@router.post('/api/nauka/move')
def nauka_move(data: dict) -> dict:
	user: str = data['user']
	answer_time: float = float(data['time'])
	answer: bool = data["answer"]

	print(data)

	instancje_gry.instances[user].move(answer, answer_time)

	updated_dict: dict = instancje_gry.instances[user].get_data()
	return updated_dict

@router.post('/api/nauka/submit')
def submit_new_module(data: dict):
	print(data)
	validated_data: dict = validate_dict_structure(data)
	if validated_data['error']:
		return validated_data
	
	save_new_module(data)
	
	return {'error': False, 'error_message': ''}
	

	
	

instancje_gry: gra.Instances = gra.Instances()

if __name__ == "__main__":
	PORT: int = 3001
	import uvicorn


	uvicorn.run(router, host="127.0.0.1", port=PORT)