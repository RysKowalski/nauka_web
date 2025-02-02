import json
import os
from fastapi import HTTPException, Header

from typing import Optional

ADMIN_API_KEY = os.getenv("ADMIN_API_KEY")

def authenticate(x_api_key: Optional[str] = Header(None)):
    print(f"Received API Key: {x_api_key}")  # Debugging
    if x_api_key != ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key

def add_user_to_file(username: str):
    file_path = os.path.join('nauka_web_api', 'backend', 'data', 'nauka_user_data.json')
    
    try:
        # Odczyt danych z pliku
        if os.path.exists(file_path):
            with open(file_path, 'r') as plik:
                user_data = json.load(plik)
        else:
            user_data = {}

        # Sprawdzanie, czy użytkownik już istnieje
        if username in user_data:
            raise HTTPException(status_code=400, detail="User already exists")

        # Dodanie użytkownika do danych
        user_data[username] = {}

        # Zapisanie zmodyfikowanych danych
        with open(file_path, 'w') as plik:
            json.dump(user_data, plik)

        return {"message": "User added successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))