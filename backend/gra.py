from typing import Self

class Game:
	def __init__(self: Self, elements: list[str]) -> None:
		...
	
	def action(self: Self, endtime: int, odpowiedz: bool) -> dict:
		return {}

class Instances:
	def __init__(self: Self) -> None:
		self.instances: dict[int, Game] = {}
	
	def new_instance(self: Self, id: int, elements: list[str]) -> None:
		new_instance: Game = Game(elements)
		self.instances[id] = new_instance

	def update_instance(self: Self, id: int, endtime: int, odpowiedz: bool) -> dict:
		
		new_data: dict = self.instances[id].action(endtime, odpowiedz)
		return new_data

def add_user(name: str) -> None:
	...

if __name__ == '__main__':
	instances: Instances = Instances()
	
	instances.new_instance(4, ['test1', 'test2'])
	
	data: dict = instances.update_instance(4, 30000, True)

	print(instances.instances, '\n\n\n\n', data)
