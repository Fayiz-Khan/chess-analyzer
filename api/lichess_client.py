import requests
import os
from dotenv import load_dotenv

load_dotenv()

MASTERS_DATABASE_URL = "https://explorer.lichess.org/masters"
LICHESS_PLAYERS_URL = "https://explorer.lichess.org/lichess"

token = os.getenv("MY_SECRET_LICHESS_TOKEN")
headers = {"Authorization": f"Bearer {token}"} if token else {}

def call_masters_database(fen: str) -> dict:
    response = requests.get(
        MASTERS_DATABASE_URL,
        params={"fen": fen},
        headers=headers
    )
    response.raise_for_status()
    
    return response.json()

def call_online_players_database(fen: str) -> dict:
    response = requests.get(
        LICHESS_PLAYERS_URL,
        params={"fen": fen},
        headers=headers
    )
    response.raise_for_status()

    return response.json()
