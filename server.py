from fastapi import FastAPI

from nauka_web.server import router as router_main
from nauka_web_api.server import router as router_api

app: FastAPI = FastAPI()
app.include_router(router_main)
app.include_router(router_api)

if __name__ == "__main__":
	import uvicorn

	PORT: int = 3000

	uvicorn.run(app, host="127.0.0.1", port=PORT)
