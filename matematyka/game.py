import random

from typing import TypedDict, Literal


class Answer(TypedDict):
    number1: int
    number2: int
    operation: Literal['+', '*']
    user_answer: int
    correct_answer: int
    correct: bool

class Question(TypedDict):
    number1: int
    number2: int
    operation: Literal['+', '*']

class Game:
    def __init__(self, all_moves: int):
        self.end: bool = False
        self.moves: int = 0
        self.answers: list[Answer] = []
        self.question: Question = {"number1": 1, "number2": 1, "operation": '+'}
        self.correct_answers: int = 0
        self.all_moves: int = all_moves
        self.last_correct_answer: int = 0

    def generate_question(self):
        if random.randint(0, 1) == 0:
            operator: Literal['+', '*'] = '+'
        else:
            operator: Literal['+', '*'] = '*'

        if operator == '+':
            number1: int = random.randint(0, 100)
            number2: int = random.randint(0, 100)
        else:
            number1: int = random.randint(0, 20)
            number2: int = random.randint(0, 20)

        self.question = {'number1': number1, 'number2': number2, 'operation': operator}

    def move(self, answer: int) -> bool:
        if self.question['operation'] == '+':
            correct_answer: int = self.question['number1'] + self.question['number2']
        else:
            correct_answer: int = self.question['number1'] * self.question['number2']

        self.last_correct_answer = correct_answer
        
        correct: bool = answer == correct_answer

        self.answers.append({'number1': self.question['number1'],
                            'number2': self.question['number2'],
                            'operation': self.question['operation'],
                            'user_answer': answer,
                            'correct_answer': correct_answer,
                            'correct': correct
                            })
        self.moves += 1
        if correct:
            self.correct_answers += 1\

        if self.moves == self.all_moves:
            self.end = True

        print(correct)
        return {'answer': f'\n{correct} {self.last_correct_answer}'}
