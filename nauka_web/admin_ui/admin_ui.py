import requests
import os
from dotenv import load_dotenv
load_dotenv()

keys: dict = {'main': os.environ.get('MAIN-SITE'), 'local': 'api-key'}

website_mode: str = 'local'

websites: dict[str, str] = {'main': 'https://stronadlabogatych.website/', 'local': 'http://localhost:8000/'}

ADD_USER_URL: str = 'api/nauka/add_user'
REMOVE_USER_URL: str = 'api/nauka/remove_user'
REMOVE_MODULE_URL: str = 'api/nauka/remove_module'

USER_LIST_URL: str = 'api/nauka/user_list'
MODULE_LIST_URL: str = 'api/nauka/modules'

HELP: str = """exit -> exit program
usradd <username> -> adds user to website and prints request json
rmusr <username> -> removes user from website and prints request json
rmm <module_name> -> removes module from website and prints requests json
setmode <mode> -> sets website. local = 'http://localhost:8000/' main = 'https://stronadlabogatych.website/'
lsm -> prints list of modules from website
lsu -> prints list of users from website
clear -> clears console
help -> provides help"""

def add_user(username: str):
	response = requests.post(websites[website_mode] + ADD_USER_URL, headers={'X-API-Key': keys[website_mode]}, json={'username': username})
	return response.json()

def remove_user(username: str):
	response = requests.delete(websites[website_mode] + REMOVE_USER_URL, headers={'X-API-Key': keys[website_mode]}, json={'username': username})
	return response.json()

def remove_module(module_name: str):
	response = requests.delete(websites[website_mode] + REMOVE_MODULE_URL, headers={'X-API-Key': keys[website_mode]}, json={'module_name': module_name})
	return response.json()

def get_user_list() -> list[str]:
	response = requests.get(websites[website_mode] + USER_LIST_URL, headers={'X-API-Key': keys[website_mode]})
	user_list: list[str] = response.json()['user_list']
	return user_list

def get_module_list() -> list[dict[str, str]]:
	response = requests.get(websites[website_mode] + MODULE_LIST_URL, headers={'X-API-Key': keys[website_mode]})
	module_list: list[dict[str, str]] = response.json()
	return module_list

def set_website_mode(mode: str):
	global website_mode
	website_mode = mode

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
			# Łączenie wszystkich tokenów po pierwszym jako nazwę użytkownika
			username = ' '.join(command_tokens[1:])
			print(remove_user(username))
			return
		else:
			print('you must specify username')
			return
	
	elif command_tokens[0] == 'rmm':
		if len(command_tokens) >= 2:
			module_name: str = ' '.join(command_tokens[1:])
			modules: list[str] = module_name.split(', ')
			for module in modules:
				print(f'{module = }', remove_module(module))
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
	
	elif command_tokens[0] == 'setmode':
		if len(command_tokens) >= 2:
			set_website_mode(command_tokens[1])
			return
		else:
			print('you must specify mode')
			return

if __name__ == '__main__':
	while True:
		user_command(input('# '))