import json
import os
from typing import TypedDict, cast

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from fastapi.responses import FileResponse

from nauka_web_api.backend import admin, gra, login_stuff
from nauka_web_api.backend.login_stuff import UserStatus
from nauka_web_api.backend.new_module_validation import validate_dict_structure
from nauka_web_api.backend.save_new_module import (
    ModuleData,
    ModuleDataFromAPI,
    save_new_module,
)

router: APIRouter = APIRouter()


@router.get("/auth/callback")
async def auth_callback(code: str, response: Response):
    return await login_stuff.auth_callback(code, response)


@router.get("/api/nauka/data")
def get_info():
    file_path = os.path.join("nauka_web_api", "backend", "data", "nauka_questions.json")
    response = FileResponse(file_path)
    response.headers["Cache-Control"] = (
        "no-store, no-cache, must-revalidate, proxy-revalidate"
    )

    return response


class User(TypedDict):
    user: str


class UserExistsReturn(TypedDict):
    exists: bool


@router.post("/api/nauka/user_exist")
def user_exist(user: User) -> UserExistsReturn:
    with open(
        os.path.join("nauka_web_api", "backend", "data", "nauka_user_data.json"), "r"
    ) as plik:
        user_exists: bool = user["user"] in json.load(plik)
        return {"exists": user_exists}


class InitData(TypedDict):
    chances: list[str]


@router.post("/api/nauka/init")
def start_new_game_session(
    data: InitData, api_key: str = Cookie(None)
) -> gra.GameStateReturnData:
    user: str = login_stuff.get_username(api_key)
    chances: list[str] = data["chances"]

    gameInstances.new_instance(user, chances)

    updated_dict: gra.GameStateReturnData = gameInstances.instances[user].get_data()
    return updated_dict


class MoveData(TypedDict):
    time: str
    answer: bool


@router.post("/api/nauka/move")
def nauka_move(data: MoveData, api_key: str = Cookie(None)) -> gra.GameStateReturnData:
    user: str = login_stuff.get_username(api_key)
    answer_time: float = float(data["time"])
    answer: bool = data["answer"]

    gameInstances.instances[user].move(answer, answer_time)

    updated_dict: gra.GameStateReturnData = gameInstances.instances[user].get_data()
    return updated_dict


@router.post("/api/nauka/submit")
def submit_new_module(dataFromAPI: ModuleDataFromAPI, api_key: str = Cookie(None)):
    validated_data: dict = validate_dict_structure(dataFromAPI, api_key)
    if validated_data["error"]:
        return validated_data

    temporary_data: dict = cast(dict, dataFromAPI)
    temporary_data["username"] = login_stuff.get_user_status(api_key)["global_name"]
    data: ModuleData = cast(ModuleData, temporary_data)
    save_new_module(data)

    return {"error": False, "error_message": "Udało się zapisać nowy moduł"}


class RemoveUserData(TypedDict):
    username: str


@router.delete("/api/nauka/remove_user")
def remove_user(
    data: RemoveUserData, api_key: str = Depends(admin.authenticate)
) -> admin.ReturnMessage:
    username = data.get("username")
    if not username:
        raise HTTPException(status_code=400, detail="Username is required")

    return admin.remove_user(username)


class RemoveModuleData(TypedDict):
    module_name: str


@router.delete("/api/nauka/remove_module")
def remove_module(
    data: RemoveModuleData, api_key: str = Depends(admin.authenticate)
) -> admin.ReturnMessage:
    module_name = data.get("module_name")
    if not module_name:
        raise HTTPException(status_code=400, detail="Username is required")

    return admin.remove_module(module_name)


@router.get("/api/nauka/modules")
def get_modules(api_key: str = Depends(admin.authenticate)) -> list[dict[str, str]]:
    return admin.get_module_list()


@router.get("/api/get_user_status")
def get_user_status(api_key: str = Cookie(None)) -> UserStatus:
    logged: UserStatus = login_stuff.get_user_status(api_key)
    return logged


gameInstances: gra.Instances = gra.Instances()

if __name__ == "__main__":
    PORT: int = 3001
    import uvicorn

    uvicorn.run(router, host="127.0.0.1", port=PORT)
