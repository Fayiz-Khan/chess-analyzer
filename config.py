from pathlib import Path
import os

PROJECT_ROOT = Path(__file__).resolve().parent

TEMP_PGN_PATH = PROJECT_ROOT / "temp.pgn"
POSITION_DATASET_PATH = PROJECT_ROOT / "data" / "positions.jsonl"

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

ENGINE_PATH = os.getenv("ENGINE_PATH", "/opt/homebrew/bin/stockfish")
ENGINE_DEPTH = int(os.getenv("ENGINE_DEPTH", "10"))

SIMILAR_POSITION_COUNT = int(os.getenv("SIMILAR_POSITION_COUNT", "5"))

_max_similarity_records = os.getenv("MAX_SIMILARITY_RECORDS")
MAX_SIMILARITY_RECORDS = int(_max_similarity_records) if _max_similarity_records else None
