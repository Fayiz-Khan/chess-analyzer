import requests
import os
from config import LICHESS_TOKEN

MASTERS_DATABASE_URL = "https://explorer.lichess.org/masters"
LICHESS_PLAYERS_URL = "https://explorer.lichess.org/lichess"

headers = {"Authorization": f"Bearer {LICHESS_TOKEN}"} if LICHESS_TOKEN else {}

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
