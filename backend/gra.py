from typing import Self

class Game:
	def __init__(self: Self, elements: list[str]) -> None:
		...

class Instances:
	def __init__(self: Self) -> None:
		self.instances: dict[int, Game] = {}
	
	def new_instance(self: Self, id: int, elements: list[str]) -> None:
		new_instance: Game = Game(elements)
		self.instances[id] = new_instance


if __name__ == '__main__':
	instances: Instances = Instances()
	
	instances.new_instance(4, ['test1', 'test2'])
	
	print(instances.instances)