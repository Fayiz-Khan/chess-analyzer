import chess.engine

from config import ENGINE_DEPTH, ENGINE_PATH

def call_engine(
    engine: chess.engine.SimpleEngine,
    board: chess.Board,
) -> chess.engine.InfoDict:
    return engine.analyse(board, chess.engine.Limit(depth=ENGINE_DEPTH))

def start_engine() -> chess.engine.SimpleEngine:
    return chess.engine.SimpleEngine.popen_uci(ENGINE_PATH)
