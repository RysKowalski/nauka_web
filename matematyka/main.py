from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import random
from typing import TypedDict, Literal

import os

from game import Game

app: FastAPI = FastAPI()

app.mount("/public", StaticFiles(directory="public"), name="public")

@app.get('/')
def index():
    return FileResponse(os.path.join('index.html'))

game: Game = Game(20)

@app.get('/start')
def start():
    game = Game(20)

@app.get('/generate')
def generate():
    game.generate_question()

    return {'question': f'{game.question['number1']} {game.question['operation']} {game.question['number2']}'}

@app.post('/move')
def move(answer: dict):
    return game.move(int(answer['answer']))

@app.get('/end')
def is_end():
    return game.end

@app.get('/moves')
def get_moves():
    return {'moves': f'\n{game.correct_answers} / {game.moves}\n{str(game.correct_answers / game.moves)[:4]}'}
