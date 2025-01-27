from typing import Self
import os
import json

class Game:
	def __init__(self: Self, elements: list[str], name: str) -> None:
		self.max_points: int = 0
		self.chances: list[float] = []

		self.max_points, self.chances = self.load_user_data(name, elements)
			
		self.points: int = 0
		
		self.questions: list[str] = []
		self.answers: list[str] = []
		self.elements: list[str] = elements
		self.current_element: int = 0

		with open(os.path.join('./nauka_web_api', 'backend', 'data', 'nauka_questions.json')) as plik:
			questions: dict = json.load(plik)
			for element in elements:
				self.questions.extend(questions[element]['names'])
				self.answers.extend(questions[element]['data'])
	
	def get_data(self: Self) -> dict:
		data: dict = {
			"element_list": dict(zip(self.elements, self.chances)),
			"max_points": self.max_points,
			"question": self.questions[self.current_element],
			"answer": self.answers[self.current_element],
		}
		return data
	
	def move(self: Self, answer: bool, answer_time: float) -> dict:

		
		return {'skibidi': 'skibidi'}
	
	def load_user_data(self: Self, name: str, elements: list[str]):
		"""
		Loads user data from the 'nauka_user_data.json' file.

		Args:
			name: The name of the user.
			elements: A list of elements.

		Returns:
			A tuple containing the maximum points and a list of chances.
		"""

		file_path = os.path.join('./nauka_web_api', 'backend', 'data', 'nauka_user_data.json')

		try:
			with open(file_path, 'r') as file:
				user_data = json.load(file)
				user_data = user_data.get(name, {})  # Get user data or an empty dict
				points_data = user_data.get('points', {})

				if '|'.join(elements) in points_data:
					max_points = points_data['|'.join(elements)]['max_points']
					chances = points_data['|'.join(elements)]['chances']
				else:
					max_points = 0
					chances = [100 for _ in elements]

		except FileNotFoundError:
			# Handle file not found
			max_points = 0
			chances = [100 for _ in elements]

		# Update user data if necessary
		if not max_points:
			with open(file_path, 'r') as file:
				data = json.load(file)
				data.setdefault(name, {})
				data[name].setdefault('points', {})
				data[name]['points']['|'.join(elements)] = {'max_points': max_points, 'chances': chances}

			with open(file_path, 'w') as file:
				json.dump(data, file)

		return max_points, chances

class Instances:
	def __init__(self: Self) -> None:
		self.instances: dict[str, Game] = {}
	
	def new_instance(self: Self, name: str, elements: list[str]) -> None:
		new_instance: Game = Game(elements, name)
		self.instances[name] = new_instance


if __name__ == '__main__':
	instances: Instances = Instances()
	
	instances.new_instance('example_user', ['example', 'question'])
	
	print(instances.instances)
	
