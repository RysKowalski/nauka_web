import requests

API_KEY: str = 'api-key'
HEADER: dict[str, str] = {'X-API-Key': API_KEY}

WEBSITE: str = 'http://localhost:8000/'

ADD_USER_URL: str = WEBSITE + 'api/nauka/add_user'
REMOVE_USER_URL: str = WEBSITE + 'api/nauka/remove_user'
REMOVE_MODULE_URL: str = WEBSITE + 'api/nauka/remove_module'

USER_LIST_URL: str = WEBSITE + 'api/nauka/user_list'
MODULE_LIST_URL: str = WEBSITE + 'api/nauka/data'

HELP: str = """exit -> exit program
usradd <username> -> adds user to website and prints request json
rmusr <username> -> removes user from website and prints request json
rmm <module_name> -> removes module from website and prints requests json
lsm -> prints list of modules from website
lsu -> prints list of users from website
clear -> clears console
help -> provides help"""

def add_user(username: str):
	response = requests.post(ADD_USER_URL, headers=HEADER, json={'username': username})
	return response.json()

def remove_user(username: str):
	response = requests.delete(REMOVE_USER_URL, headers=HEADER, json={'username': username})
	return response.json()

def remove_module(module_name: str):
	response = requests.delete(REMOVE_MODULE_URL, headers=HEADER, json={'module_name': module_name})
	return response.json()

def get_user_list() -> list[str]:
	response = requests.get(USER_LIST_URL, headers=HEADER)
	user_list: list[str] = response.json()['user_list']
	return user_list

def get_module_list() -> list[str]:
	response = requests.get(MODULE_LIST_URL)
	module_list: list[str] = list(response.json().keys())
	return module_list

def user_command(command: str):
	command_tokens: list[str] = command.split()

	if command_tokens == []:
		return
	elif command_tokens[0] == 'exit':
		exit()
	
	elif command_tokens[0] == 'usradd':
		if len(command_tokens) >= 2:
			print(add_user(command_tokens[1]))
			return
		else:
			print('you must specify username')
			return
	
	elif command_tokens[0] == 'rmusr':
		if len(command_tokens) >= 2:
			print(remove_user(command_tokens[1]))
			return
		else:
			print('you must specify username')
			return
	
	elif command_tokens[0] == 'rmm':
		if len(command_tokens) >= 2:
			print(remove_module(command_tokens[1]))
			return
		else:
			print('you must specify module name')
			return
	
	elif command_tokens[0] == 'lsm':
		print(get_module_list())
		return
	
	elif command_tokens[0] == 'lsu':
		print(get_user_list())
		return
	
	elif command_tokens[0] == 'help':
		print(HELP)
		return
	
	elif command_tokens[0] == 'clear':
		print('\n' * 20)
		return
	

if __name__ == '__main__':
	while True:
		user_command(input('# '))