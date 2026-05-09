import chess
from analyzer import analyze_game
from models import MoveColour
from export import export_analysis
from summarizer import build_summary

DEFAULT_PGN_PATH = "game.pgn"

metadata, analysis = analyze_game(DEFAULT_PGN_PATH)

summary = build_summary(analysis)

export_analysis(metadata, analysis, summary)

for move in analysis:
    board = chess.Board(move.fen_state_after)

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
