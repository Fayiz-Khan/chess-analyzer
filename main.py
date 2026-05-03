import chess
import chess.pgn
import chess.engine

from analyzer import classify_move, score_to_cp, format_score
from models import MoveAnalysis, MoveClassification

def call_engine(engine, board):
    return engine.analyse(board, chess.engine.Limit(depth=10))

with open("game.pgn") as pgn: 
    game = chess.pgn.read_game(pgn)

print(game, "\n")

board = game.board()

analysis = []

engine = chess.engine.SimpleEngine.popen_uci("stockfish")

for move in game.mainline_moves():

    info_before = call_engine(engine, board)
    eval_before = score_to_cp(info_before["score"])

    standard_algebraic_move = board.san(move) # converts move to SAN (standard algebraic notation). If we didn't, it would say 1. e2e4 instead of the standard 1. e4 as an example

    move_number = board.fullmove_number

    if board.turn == chess.WHITE:
        print(f"{move_number}. {standard_algebraic_move}")
    else:
        print(f"{move_number}... {standard_algebraic_move}")

    best_line = info_before.get("pv")
    best_move = best_line[0] if best_line else None
    best_move_san = board.san(best_move) if best_move else "None"
    
    board.push(move)

    if board.is_checkmate():
        classification = MoveClassification.BEST

        eval_after = -100000 if board.turn == chess.WHITE else 100000
        
        analysis.append(
            MoveAnalysis(
                move_san=standard_algebraic_move,
                eval_before=eval_before,
                eval_after=-10000,
                delta=999,
                classification=classification
            )
        )

        print(classification.value)
        print("Checkmate")
        print("--------------------")
        break

    print(board)

    info_after = call_engine(engine, board)
    eval_after = score_to_cp(info_after["score"])

    delta = eval_before - eval_after

    if best_move:    
        print(f"Best move: {best_move_san}")

    classification = classify_move(delta, move, best_move)

    analysis.append(
        MoveAnalysis(
            move_san=standard_algebraic_move,
            eval_before=eval_before,
            eval_after=eval_after,
            delta=delta,
            classification=classification
        )
    )

    print(f"Eval: {format_score(info_before['score'])} → {format_score(info_after['score'])}")
    print(f"Δ {delta:.2f}")
    print(f"{classification.value}")
    print("--------------------")

engine.quit()
