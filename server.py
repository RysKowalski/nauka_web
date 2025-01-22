import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from nauka_web.server import router as router_main
from nauka_web_api.server import router as router_api

app: FastAPI = FastAPI()
app.include_router(router_main)
app.include_router(router_api)

app.mount("/nauka_web", StaticFiles(directory=os.path.join(os.getcwd(), "nauka_web/public")), name="nauka_web")

if __name__ == "__main__":
	import uvicorn

	PORT: int = 3000

	uvicorn.run(app, host="0.0.0.0", port=PORT)
