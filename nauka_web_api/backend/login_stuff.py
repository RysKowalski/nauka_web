import os
import sqlite3
import secrets
import httpx
from fastapi import HTTPException, Response
from fastapi.responses import RedirectResponse

# Konfiguracja Discord OAuth
DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
DISCORD_REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI")
DISCORD_TOKEN_URL = "https://discord.com/api/oauth2/token"
DISCORD_USER_URL = "https://discord.com/api/users/@me"

# Inicjalizacja bazy danych
DB_PATH = os.path.join('nauka_web_api', "backend", "data", "users.db")

def init_db():
    """Tworzy tabelę w bazie danych, jeśli nie istnieje."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            discord_id TEXT UNIQUE,
            username TEXT,
            global_name TEXT,
            avatar TEXT,
            api_key TEXT UNIQUE
        )
    """)
    conn.commit()
    conn.close()

async def auth_callback(code: str, response: Response):
    """Obsługuje callback po autoryzacji na Discordzie."""
    async with httpx.AsyncClient() as client:
        # Wymiana kodu na token dostępu
        token_response = await client.post(
            DISCORD_TOKEN_URL,
            data={
                "client_id": DISCORD_CLIENT_ID,
                "client_secret": DISCORD_CLIENT_SECRET,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": DISCORD_REDIRECT_URI,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        if token_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Błąd autoryzacji")

        token_data = token_response.json()
        access_token = token_data["access_token"]

        # Pobranie danych użytkownika
        user_response = await client.get(
            DISCORD_USER_URL,
            headers={"Authorization": f"Bearer {access_token}"},
        )

        if user_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Błąd pobierania użytkownika")

        user_data = user_response.json()
        discord_id = user_data["id"]
        username = user_data["username"]
        global_name = user_data.get("global_name", "")
        avatar = user_data.get("avatar", "")
        
        print(f'{user_data = }')

        # Sprawdzenie, czy użytkownik już istnieje
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT api_key FROM users WHERE discord_id = ?", (discord_id,))
        user = cursor.fetchone()

        if user:
            api_key = user[0]  # Pobranie istniejącego klucza API
        else:
            # Generowanie nowego klucza API
            api_key = secrets.token_hex(32)
            cursor.execute("INSERT INTO users (discord_id, username, global_name, avatar, api_key) VALUES (?, ?, ?, ?, ?)",
                           (discord_id, username, global_name, avatar, api_key))
            conn.commit()

        conn.close()

        # Zapisanie klucza API w ciasteczku
        response = RedirectResponse(url="/nauka/wybieranie", headers={"Cache-Control": "no-cache, no-store, must-revalidate"})
        response.set_cookie(key="api_key", value=api_key, httponly=True, secure=True, samesite="lax")

        return response

def get_user_status(api_key: str) -> dict:
    """
    Sprawdza, czy podany api_key istnieje w bazie danych i zwraca informacje o użytkowniku.

    :param api_key: Klucz API do sprawdzenia
    :return: Słownik zawierający klucze 'username', 'global_name', 'discord_id', 'avatar' i 'is_logged'
    """
    try:
        # Połączenie z bazą danych
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        # Zapytanie SQL sprawdzające api_key i pobierające dane użytkownika
        query = "SELECT username, global_name, discord_id, avatar FROM users WHERE api_key = ?"
        cursor.execute(query, (api_key,))

        # Pobranie wyniku
        result = cursor.fetchone()

        if result:
            # Użytkownik istnieje, zwracamy jego dane i status zalogowania
            return {
                "username": result[0],
                "global_name": result[1],
                "discord_id": result[2],
                "avatar": result[3],
                "is_logged": True
            }
        else:
            # Brak użytkownika z takim api_key
            return {"username": None, "global_name": None, "discord_id": None, "avatar": None, "is_logged": False}

    except sqlite3.Error as e:
        print(f"Błąd bazy danych: {e}")
        return {"username": None, "global_name": None, "discord_id": None, "avatar": None, "is_logged": False}
    finally:
        if connection:
            connection.close()

def get_username(api_key: str) -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT global_name FROM users WHERE api_key = ?", (api_key,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 'guest'

init_db()

# Przykład użycia
if __name__ == "__main__":
    api_key_to_check = "4608ae37baed103bd3cf334d573c344dfac64c17099f52be8ac40b4e0e0b4b4f"
    
    print(get_username(api_key_to_check))
