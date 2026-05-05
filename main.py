import chess
from analyzer import analyze_game
from models import MoveColour

analysis = analyze_game("game.pgn")

for move in analysis:
    board = chess.Board(move.board_state)

    if move.move_colour == MoveColour.WHITE:
        print(f"{move.move_number}. {move.move_san}")
    else:
        print(f"{move.move_number}... {move.move_san}")

    print(board)
    print()
    if move.best_move_san != "None":
        print(f"Best move: {move.best_move_san}")

    print(f"Eval: {move.eval_before:.2f} → {move.eval_after:.2f}")
    print(f"Δ {move.delta:.2f}")
    print(move.classification.value)

    if move.is_checkmate:
        print("Checkmate")

    print("--------------------")
