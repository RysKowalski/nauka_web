import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from dotenv import load_dotenv
import httpx

# Wczytanie konfiguracji z pliku .env
load_dotenv()

DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
DISCORD_REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI")
DISCORD_TOKEN_URL = "https://discord.com/api/oauth2/token"
DISCORD_USER_URL = "https://discord.com/api/users/@me"

app = FastAPI()

@app.get("/auth/login")
async def login():
    """Generuje URL do autoryzacji użytkownika przez Discord."""
    return {
        "url": f"https://discord.com/api/oauth2/authorize"
               f"?client_id={DISCORD_CLIENT_ID}"
               f"&redirect_uri={DISCORD_REDIRECT_URI}"
               f"&response_type=code"
               f"&scope=identify+email"
    }

@app.get("/auth/callback")
async def auth_callback(code: str):
    """Obsługuje callback po autoryzacji na Discordzie."""
    async with httpx.AsyncClient() as client:
        # Wymiana kodu na token dostępu
        response = await client.post(
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
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Błąd autoryzacji")

        token_data = response.json()
        access_token = token_data["access_token"]

        # Pobranie danych użytkownika
        user_response = await client.get(
            DISCORD_USER_URL,
            headers={"Authorization": f"Bearer {access_token}"},
        )

        if user_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Błąd pobierania użytkownika")

        user_data = user_response.json()
        print(user_data)
        return {
            "id": user_data["id"],
            "username": user_data["username"],
            "discriminator": user_data["discriminator"],
            "email": user_data.get("email"),
            "avatar": f"https://cdn.discordapp.com/avatars/{user_data['id']}/{user_data['avatar']}.png"
        }
