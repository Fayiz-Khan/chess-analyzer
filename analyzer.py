import chess

from models import MoveClassification


def classify_move(eval_drop, player_move, best_move):
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
    
def score_to_cp(score):
    pov = score.pov(chess.WHITE) # normalize scores so + can be in favour of white and - be in favour of black as it normally is
    if pov.is_mate():
        return 10000 if pov.mate() > 0 else -10000
    return pov.score() / 100.0

def format_score(score): 
    pov = score.pov(chess.WHITE)

    if pov.is_mate():
        mate_moves = pov.mate()
        if mate_moves > 0:
            return f"Mate in {mate_moves}"
        return f"-Mate in {abs(mate_moves)}"

    return f"{pov.score() / 100.0:.2f}"
