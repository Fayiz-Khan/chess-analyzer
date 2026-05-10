import chess.engine
import os

ENGINE_PATH = os.getenv("ENGINE_PATH", "/opt/homebrew/bin/stockfish")
ENGINE_DEPTH = int(os.getenv("ENGINE_DEPTH", "10"))

def call_engine(
    engine: chess.engine.SimpleEngine,
    board: chess.Board,
) -> chess.engine.InfoDict:
    return engine.analyse(board, chess.engine.Limit(depth=ENGINE_DEPTH))

def start_engine() -> chess.engine.SimpleEngine: 
    return chess.engine.SimpleEngine.popen_uci(ENGINE_PATH)
