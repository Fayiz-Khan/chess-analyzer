import chess.engine

ENGINE_NAME = "/opt/homebrew/bin/stockfish"
ENGINE_DEPTH = 10

def call_engine(engine, board):
    return engine.analyse(board, chess.engine.Limit(depth=ENGINE_DEPTH))

def start_engine(): 
    return chess.engine.SimpleEngine.popen_uci(ENGINE_NAME)
