from typing import Self
import os
import json

import numpy as np
from math import log2

class Game:
	def __init__(self: Self, elements: list[str], name: str) -> None:
		self.modules: list[str] = elements
		self.elements: list[dict] = []
		self.max_points: int = 0
		self.points: int = 0
		self.current_element: int = 0
		self.username: str = name

		chances: list[float] = []
		questions: list[str] = []
		answers: list[str] = []
		names: list[str] = []

		self.max_points, chances = self.load_user_data(name, self.modules)

		with open(os.path.join('./nauka_web_api', 'backend', 'data', 'nauka_questions.json')) as plik:
			questions_from_file: dict = json.load(plik)

			for element in elements:
				questions.extend(questions_from_file[element]['questions'])
				answers.extend(questions_from_file[element]['data'])
				names.extend(questions_from_file[element]['names'])

		for i, element in enumerate(names):
			self.elements.append({
				'name': element,
				'chance': chances[i],
				'question': questions[i],
				'answer': answers[i]
			})
			
	
	def get_data(self: Self) -> dict:
		data: dict = {
			'element_list': dict(zip([item['name'] for item in self.elements], [item['chance'] for item in self.elements])),
			'max_points': self.max_points,
			'question': self.elements[self.current_element]['question'],
			'answer': self.elements[self.current_element]['answer'],
			'points': self.points
		}


		return data
	
	def move(self: Self, answer: bool, answer_time: float) -> None:

		if answer_time / 10 > 1:
			self.elements[self.current_element]['chance'] *= log2(answer_time) - 2.7

		if answer:
			self.points += 1
			if self.points > self.max_points:
				self.max_points = self.points

			self.elements[self.current_element]['chance'] /= 1.2
		else:
			self.elements[self.current_element]['chance'] *= 1.7
			self.points = 0
			self.save_user_data()
		
		weights = np.array([item['chance'] for item in self.elements]) / np.sum([item['chance'] for item in self.elements])
		self.current_element = np.random.choice(range(0, len(weights)), p=weights)

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
				with open(os.path.join('nauka_web_api', 'backend', 'data', 'nauka_questions.json'), 'r') as plik:
					questions_data: dict = json.load(plik)
					questions: list = []
					for module in elements:
						questions.extend(questions_data[module]['questions'])
				
				max_points = 0
				chances = [100 for _ in range(len(questions))]
					

		except FileNotFoundError:
			# Handle file not found
			max_points = 0
			chances = [100 for _ in elements]

		return max_points, chances

	def save_user_data(self: Self) -> None:
		with open(os.path.join('nauka_web_api', 'backend', 'data', 'nauka_user_data.json'), 'r') as plik:
			data: dict = json.load(plik)
		
		data[self.username]['|'.join(self.modules)] = {'max_points': self.max_points, 'chances': [item['chance'] for item in self.elements]}

		with open(os.path.join('nauka_web_api', 'backend', 'data', 'nauka_user_data.json'), 'w') as plik:
			json.dump(data, plik)

class Instances:
	def __init__(self: Self) -> None:
		self.instances: dict[str, Game] = {}
	
	def new_instance(self: Self, name: str, elements: list[str]) -> None:
		new_instance: Game = Game(elements, name)
		self.instances[name] = new_instance


if __name__ == '__main__':
	instances: Instances = Instances()
	
	instances.new_instance('rysiek', ['example'])
	
	print(instances.instances['rysiek'].get_data())

	instances.instances['rysiek'].move(True, 1)

	print()	
	print(instances.instances['rysiek'].get_data())
	