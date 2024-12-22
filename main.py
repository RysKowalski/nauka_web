from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import os
import sys
import requests
import subprocess
import uvicorn
from typing import Any, Dict, List

from server import router

app = FastAPI()
app.include_router(router)

PORT: int = 3000

# Konfiguracja
AUTHORIZED_IP: str = "127.0.0.1"  # Adres IP, który może uzyskać dostęp do endpointu
VERSION_URL: str = "https://raw.githubusercontent.com/RysKowalski/updates/refs/heads/main/version.txt"  # URL pliku z wersją
UPDATE_URL: str = "https://raw.githubusercontent.com/RysKowalski/updates/refs/heads/main/update.json"  # URL pliku JSON z instrukcjami aktualizacji
LOCAL_VERSION_FILE: str = "local_version.txt"  # Lokalny plik z wersją

@app.middleware("http")
async def verify_ip(request, call_next: Any) -> JSONResponse:
    client_ip: str = request.client.host
    if client_ip != AUTHORIZED_IP:
        return JSONResponse(status_code=403, content={"detail": "Access forbidden"})
    return await call_next(request)

@app.get("/update")
async def update_endpoint() -> Dict[str, Any]:
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
        update_instructions: Dict[str, list[dict[str, str]]] = requests.get(UPDATE_URL).json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch update instructions: {e}")

    # Przetwarzanie instrukcji aktualizacji
    for instruction in update_instructions.get("instructions", []):
        action: str = instruction.get("action", "") # instrukcja do wykonania
        target: str = instruction.get("target", "") # plik do wykonania instrukcji
        source: str = instruction.get("source", "") # link do pobrania pliku
        destination: str = instruction.get("destination",  "") # ścieżka do zapisania pliku / nazwa pliku

        try:
            if action == "delete": # instrukcja usuwająca plik target
                if os.path.exists(target):
                    os.remove(target)
                    
            elif action == "download": # instrukcja pobierająca plik source, zapisując go do pliku destination
                file_content: bytes = requests.get(source).content
                with open(destination, "wb") as f:
                    f.write(file_content)
                    
            elif action == "rename": # instrukcja zmieniająca nazwę pliku target na destination
                if os.path.exists(target):
                    os.rename(target, destination)
                    
            elif action == "move": # porusza plik target do destination
                if os.path.exists(target):
                    os.replace(target, destination)
                    
            elif action == "execute": # włącza plik target przez python
                if os.path.exists(target):
                    os.system(f'python ./{target}')

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error during update action '{action}': {e}")

    # Restart aplikacji
    restart_application()
    return {"detail": "Update completed, restarting..."}

def restart_application() -> None:
    """Funkcja restartująca aplikację."""
    python: str = sys.executable
    os.execl(python, python, *sys.argv)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=PORT)
