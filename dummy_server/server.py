import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from nauka_web.server import router as router_main
from nauka_web_api.server import router as router_api

with open(os.path.join("version.txt"), "r") as plik:
    VERSION: str = plik.read()

app: FastAPI = FastAPI()
app.include_router(router_main)
app.include_router(router_api)

app.mount(
    "/nauka_web",
    StaticFiles(directory=os.path.join(os.getcwd(), "nauka_web/public")),
    name="nauka_web",
)


@app.get("/favicon.ico")
def favicon():
    return FileResponse(os.path.join("favicon.ico"))


@app.get("/version")
def get_version():
    """get version string like "1.3.1" """
    return {"version": VERSION}


def run():
    import uvicorn
    from uvicorn.config import LOGGING_CONFIG

    LOGGING_CONFIG["formatters"]["default"]["fmt"] = (
        "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
    )
    PORT: int = 3000
    uvicorn.run(app, log_config=LOGGING_CONFIG, port=PORT)


if __name__ == "__main__":
    run()
