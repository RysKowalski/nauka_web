import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def save_new_module(data: dict):
	with open(os.path.join(BASE_DIR, "data", "nauka_questions.json"), 'r') as plik:
		modules: dict = json.load(plik)

	name: str = data['name']

	module_datas: list[str] = []
	module_questions: list[str] = []

	username: str = data['username']

	for i, element in enumerate(data['elements']):
		module_datas.append(element['answer'])
		module_questions.append(element['question'])
	
	modules[name] = {'data': module_datas, 'questions': module_questions, 'username': username}
	print(modules)
	
	with open(os.path.join(BASE_DIR, "data", "nauka_questions.json"), 'w') as plik:
		json.dump(modules, plik)