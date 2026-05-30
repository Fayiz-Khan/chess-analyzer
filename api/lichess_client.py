import requests
import os
from dotenv import load_dotenv

load_dotenv()

MASTERS_DATABASE_URL = "https://explorer.lichess.org/masters"
token = os.getenv("MY_SECRET_TOKEN")

headers = {
    "Authorization": f"Bearer {token}"
}

def call_masters_database(fen: str):
    response = requests.get(
        MASTERS_DATABASE_URL,
        params={"fen": fen},
        headers=headers
    )
    response.raise_for_status()

    return response.json()
