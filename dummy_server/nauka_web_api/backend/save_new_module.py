import json
import os
from typing import Optional, TypedDict


class ModuleElementData(TypedDict):
    question: str
    answer: str


class ModuleData(TypedDict):
    name: str
    elements: list[ModuleElementData]
    username: str


class ModuleDataFromAPI(TypedDict):
    name: str
    elements: list[ModuleElementData]


def save_new_module(data: ModuleData):
    with open(
        os.path.join("nauka_web_api", "backend", "data", "nauka_questions.json"), "r"
    ) as plik:
        modules: dict = json.load(plik)

    name: str = data["name"]

    module_datas: list[str] = []
    module_questions: list[str] = []

    username: str = data["username"]

    for element in data["elements"]:
        module_datas.append(element["answer"])
        module_questions.append(element["question"])

    modules[name] = {
        "data": module_datas,
        "questions": module_questions,
        "username": username,
    }
    print(modules)

    with open(
        os.path.join("nauka_web_api", "backend", "data", "nauka_questions.json"), "w"
    ) as plik:
        json.dump(modules, plik)
