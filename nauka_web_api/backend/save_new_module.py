import json
import os

def save_new_module(data: dict):
	with open(os.path.join("nauka_web_api", "backend", "data", "nauka_questions.json"), 'r') as plik:
		modules: dict = json.load(plik)
	
	new_module: dict = {}

	name: str = data['name']

	module_names: list[str] = []
	module_datas: list[str] = []
	module_questions: list[str] = []

	for i, element in enumerate(data['elements']):
		module_names.append(element['name'])
		module_datas.append(element['answer'])
		module_questions.append(element['question'])
	
	modules[name] = {'data': module_datas, 'names': module_names, 'questions': module_questions}
	print(modules)
	
	with open(os.path.join("nauka_web_api", "backend", "data", "nauka_questions.json"), 'w') as plik:
		json.dump(modules, plik)