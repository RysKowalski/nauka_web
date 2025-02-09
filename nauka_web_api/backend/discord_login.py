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
DB_PATH = ""

def init_db():
    """Tworzy tabelę w bazie danych, jeśli nie istnieje."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            discord_id TEXT UNIQUE,
            username TEXT,
            api_key TEXT UNIQUE
        )
    """)
    conn.commit()
    conn.close()

init_db()

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
            cursor.execute("INSERT INTO users (discord_id, username, api_key) VALUES (?, ?, ?)",
                           (discord_id, username, api_key))
            conn.commit()

        conn.close()

        # Zapisanie klucza API w ciasteczku
        response = RedirectResponse(url="/nauka/wybieranie", headers={"Cache-Control": "no-cache, no-store, must-revalidate"})
        response.set_cookie(key="api_key", value=api_key, httponly=True, secure=True, samesite="lax")

        return response
