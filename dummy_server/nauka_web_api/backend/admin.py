import json
import os
from typing import Optional, TypedDict

from fastapi import Header, HTTPException

ADMIN_API_KEY = os.getenv("ADMIN_API_KEY")


class Modules(TypedDict):
    data: list[str]
    questions: list[str]
    username: str


class ReturnMessage(TypedDict):
    message: str


def authenticate(x_api_key: Optional[str] = Header(None)):
    if x_api_key != ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key


def add_user(username: str) -> ReturnMessage:
    file_path = os.path.join("nauka_web_api", "backend", "data", "nauka_user_data.json")

    try:
        # Odczyt danych z pliku
        if os.path.exists(file_path):
            with open(file_path, "r") as plik:
                user_data = json.load(plik)
        else:
            user_data = {}

        # Sprawdzanie, czy użytkownik już istnieje
        if username in user_data:
            raise HTTPException(status_code=400, detail="User already exists")

        # Dodanie użytkownika do danych
        user_data[username] = {}

        # Zapisanie zmodyfikowanych danych
        with open(file_path, "w") as plik:
            json.dump(user_data, plik)

        return {"message": "User added successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def remove_user(username: str) -> ReturnMessage:
    file_path = os.path.join("nauka_web_api", "backend", "data", "nauka_user_data.json")
    try:
        # Odczyt danych z pliku
        if os.path.exists(file_path):
            with open(file_path, "r") as plik:
                user_data = json.load(plik)
        else:
            user_data = {}

        # Sprawdzanie, czy użytkownik już istnieje
        if username not in user_data:
            raise HTTPException(status_code=400, detail="User don't exists")

        user_data.pop(username)

        # Zapisanie zmodyfikowanych danych
        with open(file_path, "w") as plik:
            json.dump(user_data, plik)

        return {"message": "User removed successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def remove_module(module_name: str) -> ReturnMessage:
    file_path = os.path.join("nauka_web_api", "backend", "data", "nauka_questions.json")
    try:
        # Odczyt danych z pliku
        if os.path.exists(file_path):
            with open(file_path, "r") as plik:
                questions_data = json.load(plik)
        else:
            questions_data = {}

        # Sprawdzanie, czy użytkownik już istnieje
        if module_name not in questions_data:
            raise HTTPException(status_code=400, detail="User don't exists")

        questions_data.pop(module_name)

        # Zapisanie zmodyfikowanych danych
        with open(file_path, "w") as plik:
            json.dump(questions_data, plik)

        return {"message": "module removed successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_user_list() -> dict[str, list[str]]:
    file_path = os.path.join("nauka_web_api", "backend", "data", "nauka_user_data.json")
    try:
        # Odczyt danych z pliku
        if os.path.exists(file_path):
            with open(file_path, "r") as plik:
                user_list: list[str] = list(json.load(plik).keys())
        else:
            user_list = []

        return {"user_list": user_list}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class ModuleData(TypedDict):
    data: list[str]
    questions: list[str]
    username: str


# def get_module_list() -> list[ModuleData]:
#     print("\nDOES THIS EVEN WORK???\n")
#     print("\nDOES THIS EVEN WORK???\n")
#     print("\nDOES THIS EVEN WORK???\n")
#     file_path = os.path.join("nauka_web_api", "backend", "data", "nauka_questions.json")
#
#     try:
#         with open(file_path, "r") as plik:
#             modules: dict[str, ModuleData] = json.load(plik)
#
#         return_data: list[ModuleData] = []
#         for module in modules.keys():
#             return_data.append({module: modules[module]["username"]})
#         return return_data
#
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
