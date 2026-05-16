import chess
from analyzer.analyzer import analyze_game
from models.models import MoveColour, Evaluation
from analyzer.export import export_analysis
from analyzer.summarizer import build_summary

def format_evaluation(evaluation: Evaluation) -> str:
    if evaluation.mate_in is not None:
        return f"M{evaluation.mate_in}"

    return f"{evaluation.centipawns:.2f}"

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

    print(
    f"Eval: "
    f"{format_evaluation(move.eval_before)} "
    f"→ "
    f"{format_evaluation(move.eval_after)}"
)
    if move.delta is not None:
        print(f"Δ {move.delta:.2f}")
    else:
        print("Δ N/A")
    print(move.classification.value)

    if move.is_checkmate:
        print("Checkmate")

    print("--------------------")
