import chess
import chess.pgn

from engine import call_engine, start_engine
from models import MoveAnalysis, MoveClassification, MoveColour


def classify_move(
    eval_drop: float,
    player_move: chess.Move,
    best_move: chess.Move | None,
) -> MoveClassification:
    
    if best_move and player_move == best_move:
        return MoveClassification.BEST
    if eval_drop >= 2.0:
        return MoveClassification.BLUNDER
    elif eval_drop >= 1.0:
        return MoveClassification.MISTAKE
    elif eval_drop >= 0.3:
        return MoveClassification.INACCURACY
    else:
        return MoveClassification.GOOD
    
def score_to_cp(score: chess.engine.PovScore) -> float:
    pov = score.pov(chess.WHITE) # normalize scores so + can be in favour of white and - be in favour of black as it normally is
    if pov.is_mate():
        return 10000 if pov.mate() > 0 else -10000
    return pov.score() / 100.0

def analyze_game(pgn_path: str) -> tuple[dict[str, str], list[MoveAnalysis]]:
    analysis = []

    with open(pgn_path) as pgn:
        game = chess.pgn.read_game(pgn)

    metadata = dict(game.headers)

    board = game.board()
    engine = start_engine()

    try:
        for move in game.mainline_moves():
            info_before = call_engine(engine, board)
            eval_before = score_to_cp(info_before["score"])

            move_san = board.san(move)
            best_line = info_before.get("pv")
            best_move = best_line[0] if best_line else None
            best_move_san = board.san(best_move) if best_move else "None"

            move_number = board.fullmove_number
            move_colour = MoveColour.WHITE if board.turn == chess.WHITE else MoveColour.BLACK

            fen_state_before = board.fen()  # storing the fen for flexibility when working with APIs compared to storing board string which we can output as anyways
            board.push(move)
            fen_state_after = board.fen()

            if board.is_checkmate():
                classification = MoveClassification.BEST
                eval_after = -10000 if board.turn == chess.WHITE else 10000

                analysis.append(
                    MoveAnalysis(
                        move_number=move_number,
                        move_colour=move_colour,
                        move_san=move_san,
                        best_move_san=best_move_san,
                        fen_state_before=fen_state_before,
                        fen_state_after=fen_state_after,
                        eval_before=eval_before,
                        eval_after=eval_after,
                        delta=999,
                        classification=classification,
                        is_checkmate=True,
                    )
                )
                break

            info_after = call_engine(engine, board)
            eval_after = score_to_cp(info_after["score"])

            delta = eval_before - eval_after if move_colour == MoveColour.WHITE else eval_after - eval_before 

            classification = classify_move(delta, move, best_move)

            analysis.append(
                MoveAnalysis(
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
                )
            )

    finally:
        engine.quit()

    return  metadata, analysis
