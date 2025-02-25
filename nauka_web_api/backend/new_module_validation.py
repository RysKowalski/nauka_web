from nauka_web_api.backend.login_stuff import get_user_status

def validate_dict_structure(data, api_key: str):

	if not get_user_status(api_key)['is_logged']:
		return {'error': True, 'error_message': 'Żeby dodać nowy modół, musisz się zalogować.'}
	
	if not isinstance(data, dict):
		return {'error': True, 'error_message': 'Dane muszą być typu dict'}
	
	if set(data.keys()) != {"name", "elements"}:
		return {'error': True, 'error_message': 'Dane muszą zawierać klucze "name" oraz "elements"'}
	
	if not isinstance(data["name"], str):
		return {'error': True, 'error_message': 'Wartość klucza "name" musi być typu string.'}
	
	if not isinstance(data["elements"], list):
		return {'error': True, 'error_message': 'Wartość klucza "elements" musi być listą.'}
	
	if data['name'] == '':
		return {'error': True, 'error_message': 'Nazwa nowego modułu nie może być pusta'}

	for index, element in enumerate(data["elements"]):
		if not isinstance(element, dict):
			return {'error': True, 'error_message': f'Element na pozycji {index + 1} musi być typu dict'}
		
		if set(element.keys()) != {"question", "answer"}:
			return {'error': True, 'error_message': f'Element na pozycji {index + 1} musi zawierać dokładnie klucze: "question" i "answer".'}
		
		for key in ["question", "answer"]:
			if not isinstance(element[key], str):
				return {'error': True, 'error_message': f'Wartość klucza "{key}" w elemencie na pozycji {index + 1} musi być typu string.'}
			elif element[key] == '':
				error_message: str = ''
				if key == 'question':
					error_message = f'Pytanie elementu {index + 1} nie może być puste'
				elif key == 'answer':
					error_message = f'Odpowiedź elementu {index + 1} nie może być puste'
				return {'error': True, 'error_message': error_message}
	
	return {'error': False, 'error_message': ''}
