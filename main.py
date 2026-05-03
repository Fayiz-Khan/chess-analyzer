import chess
import chess.pgn
import chess.engine

with open("game.pgn") as pgn: 
    game = chess.pgn.read_game(pgn)

print(game, "\n")

board = game.board()

engine = chess.engine.SimpleEngine.popen_uci("stockfish")

for move in game.mainline_moves():
    standard_algebraic_move = board.san(move) # converts move to SAN (standard algebraic notation). If we didn't, it would say 1. e2e4 instead of the standard 1. e4 as an example

    move_number = board.fullmove_number

    if board.turn == chess.WHITE:
        print(f"{move_number}. {standard_algebraic_move}")
    else:
        print(f"{move_number}... {standard_algebraic_move}")
    
    board.push(move)

    print(board)

    info = engine.analyse(board, chess.engine.Limit(depth=10))

    score = info["score"]
    best_line = info.get("pv")
    best_move = best_line[0] if best_line else None

    if best_move:    
        standard_algebraic_best_move = board.san(best_move)
    else: 
        standard_algebraic_best_move = "None"

    print("Score:", score)
    print("Best move:", standard_algebraic_best_move)
    print("--------------------")

engine.quit()
