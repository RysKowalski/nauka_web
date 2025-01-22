from fastapi import APIRouter
from fastapi.responses import FileResponse

import os
import json

from typing import Dict, Union, List

from nauka_web_api.backend import gra

router: APIRouter = APIRouter()

@router.get("/api/nauka/data")
def get_info():
	# Zwrot pliku JSON
	return FileResponse(os.path.join('nauka_web_api', 'backend', 'data', 'nauka_questions.json'))

@router.post("/api/nauka/user_exist")
def user_exist(user: dict):
	print(user)
	with open(os.path.join('nauka_web_api', "backend", "data", "nauka_user_data.json"), "r") as plik:
		return user["user"] in json.load(plik)

@router.post('/api/nauka/gra')
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

@router.post('/api/nauka/init')
def nauka_init(data: Dict[str, List[str]]):
	user: str = data["user"][0]
	chances: list[str] = data["chances"]

	print(data)
	instancje_gry.new_instance(user, chances)

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
	
	updated_dict = instancje_gry.instances[user].get_data()
	return updated_dict

instancje_gry: gra.Instances = gra.Instances()

if __name__ == "__main__":
	import uvicorn

	PORT: int = 3001

	uvicorn.run(router, host="127.0.0.1", port=PORT)
#