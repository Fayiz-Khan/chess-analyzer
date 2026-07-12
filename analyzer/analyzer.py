import io

import chess
import chess.pgn

from analyzer.engine import call_engine, start_engine
from models.models import MoveAnalysis, MoveClassification, MoveColour, Evaluation


def classify_move(
    eval_drop: float | None,
    player_move: chess.Move,
    best_move: chess.Move | None,
    eval_after: Evaluation,
    move_colour: MoveColour
) -> MoveClassification:
    
    if best_move and player_move == best_move:
        return MoveClassification.BEST

    if eval_after.mate_in is not None:
        if move_colour == MoveColour.WHITE and eval_after.mate_in < 0:
            return MoveClassification.BLUNDER
        if move_colour == MoveColour.BLACK and eval_after.mate_in > 0:
            return MoveClassification.BLUNDER

    if eval_drop is None:
        return MoveClassification.GOOD

    if eval_drop >= 2.0:
        return MoveClassification.BLUNDER

    if eval_drop >= 1.0:
        return MoveClassification.MISTAKE

    if eval_drop >= 0.3:
        return MoveClassification.INACCURACY

    return MoveClassification.GOOD
    
def score_to_evaluation(score: chess.engine.PovScore) -> Evaluation:
    pov = score.pov(chess.WHITE) # normalize scores so + can be in favour of white and - be in favour of black as it normally is

    if pov.is_mate():
        return Evaluation(
            centipawns=None,
            mate_in=pov.mate(),
        )
    
    return Evaluation(
        centipawns=pov.score() / 100.0,
        mate_in=None,
    )

def analyze_pgn_text(pgn_text: str) -> tuple[dict[str, str], list[MoveAnalysis]]:
    return analyze_game_stream(io.StringIO(pgn_text))


def analyze_game(pgn_path: str) -> tuple[dict[str, str], list[MoveAnalysis]]:
    with open(pgn_path, encoding="utf-8") as pgn:
        return analyze_game_stream(pgn)


def analyze_game_stream(pgn: io.TextIOBase) -> tuple[dict[str, str], list[MoveAnalysis]]:
    analysis = []

    game = chess.pgn.read_game(pgn)

    if game is None:
        return {}, []

    metadata = dict(game.headers)

    board = game.board()
    engine = start_engine()

    try:
        for move in game.mainline_moves():
            info_before = call_engine(engine, board)
            eval_before = score_to_evaluation(info_before["score"])

            move_san = board.san(move)
            best_line = info_before.get("pv")
            best_move = best_line[0] if best_line else None
            best_move_san = board.san(best_move) if best_move else "None"

            move_number = board.fullmove_number
            move_colour = MoveColour.WHITE if board.turn == chess.WHITE else MoveColour.BLACK

            fen_state_before = board.fen()  # storing the fen for flexibility when working with APIs compared to storing board string which we can output as anyways
            board.push(move)
            fen_state_after = board.fen()

            info_after = call_engine(engine, board)
            eval_after = score_to_evaluation(info_after["score"])

            is_checkmate = board.is_checkmate()

            delta = None

            if (eval_after.centipawns is not None and eval_before.centipawns is not None):
                delta=(
                    eval_before.centipawns - eval_after.centipawns
                    if move_colour == MoveColour.WHITE
                    else eval_after.centipawns - eval_before.centipawns
                )

            classification = classify_move(delta, move, best_move, eval_after, move_colour)

            move_analysis = MoveAnalysis(
                    move_number=move_number,
                    move_colour=move_colour,
                    move_san=move_san,
                    best_move_san=best_move_san,
                    fen_state_before=fen_state_before,
                    fen_state_after=fen_state_after,
                    eval_before=eval_before,
                    eval_after=eval_after,
                    delta=delta,
                    classification=classification,
                    is_checkmate=is_checkmate,
                )

            analysis.append(move_analysis)

            if is_checkmate:
                break

    finally:
        engine.quit()

    return  metadata, analysis
