import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
load_dotenv()

from api.routes import router as api_router

app = FastAPI()

# CORS - zezwolenie na zapytania z frontendu
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adres frontendu
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

with open(os.path.join('version.txt'), 'r') as plik:
	VERSION: str = plik.read()

@app.get('/version')
def get_version():
	return {'version': VERSION}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
