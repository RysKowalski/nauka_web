from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security.api_key import APIKeyHeader
import os
import sys
import requests
import shutil
from dotenv import load_dotenv
from typing import Any

#from server import router

app = FastAPI()
#app.include_router(router)

PORT: int = 3000

load_dotenv()

# Konfiguracja
AUTHORIZED_API_KEY = os.getenv("AUTHORIZED_API_KEY")  # Klucz API, który umożliwia dostęp
VERSION_URL: str = "https://raw.githubusercontent.com/RysKowalski/updates/refs/heads/main/version.txt"  # URL pliku z wersją
UPDATE_URL: str = "https://raw.githubusercontent.com/RysKowalski/updates/refs/heads/main/update.json"  # URL pliku JSON z instrukcjami aktualizacji
LOCAL_VERSION_FILE: str = "local_version.txt"  # Lokalny plik z wersją

# Nagłówek API Key
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

# Funkcja do weryfikacji API Key
def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != AUTHORIZED_API_KEY:
        raise HTTPException(status_code=403, detail="Access forbidden: Invalid API Key")
    return api_key

def restart_application() -> None:
    """Funkcja restartująca aplikację."""
    python: str = sys.executable
    os.execl(python, python, *sys.argv)

@app.get("/update")
async def update_endpoint(api_key: str = Depends(verify_api_key)) -> dict[str, Any]:
    # Pobierz najnowszą wersję z pliku online
    try:
        latest_version: str = requests.get(VERSION_URL).text.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch version file: {e}")

    # Odczytaj lokalną wersję
    local_version: str = "0"  # Domyślna wersja, jeśli plik nie istnieje
    if os.path.exists(LOCAL_VERSION_FILE):
        with open(LOCAL_VERSION_FILE, "r") as f:
            local_version = f.read().strip()

    if local_version >= latest_version:
        return {"detail": "No update required", "current_version": local_version, "latest_version": latest_version}

    # Aktualizacja wersji lokalnej
    with open(LOCAL_VERSION_FILE, "w") as f:
        f.write(latest_version)

    # Pobierz plik JSON z instrukcjami
    try:
        update_instructions: dict[str, list[dict[str, str]]] = requests.get(UPDATE_URL).json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch update instructions: {e}")

    # Przetwarzanie instrukcji aktualizacji
    for instruction in update_instructions.get("instructions", []):
        print(instruction)
        action: str = instruction.get("action", "")  # instrukcja do wykonania
        target: str = instruction.get("target", "")  # plik do wykonania instrukcji
        source: str = instruction.get("source", "")  # link do pobrania pliku
        destination: str = instruction.get("destination", "")  # ścieżka do zapisania pliku / nazwa pliku

        try:
            if action == "delete":  # instrukcja usuwająca plik lub folder target
                if os.path.exists(target):
                    if os.path.isfile(target):  # Jeśli target jest plikiem
                        os.remove(target)
                    elif os.path.isdir(target):  # Jeśli target jest katalogiem
                        shutil.rmtree(target)  # Usuwa katalog wraz z zawartością

            elif action == "download":  # instrukcja pobierająca plik source, zapisując go do pliku destination
                file_content: bytes = requests.get(source).content
                with open(destination, "wb") as f:
                    f.write(file_content)

            elif action == "move":  # porusza plik target do destination
                if os.path.exists(target):
                    os.rename(target, destination)

            elif action == "execute":  # włącza plik target przez python
                if os.path.exists(target):
                    os.system(f'python ./{target}')

            elif action == "create_folder":  # tworzy folder o ścieżce destination
                if not os.path.exists(destination):
                    os.makedirs(destination)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error during update action '{action}': {e}")

    # Restart aplikacji
    restart_application()
    return {"detail": "Update completed, restarting..."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=PORT)
