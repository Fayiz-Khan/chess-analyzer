from models import MoveClassification, MoveColour, PlayerSummary, AnalysisSummary, MoveAnalysis

def build_player_summary(analysis: list[MoveAnalysis]) -> PlayerSummary:
    best_moves = 0
    good_moves = 0
    inaccuracies = 0
    mistakes = 0
    blunders = 0

    total_eval_loss = 0
    eval_loss_count = 0

    for move in analysis:
        if move.classification == MoveClassification.BEST:
            best_moves += 1
        elif move.classification == MoveClassification.GOOD:
            good_moves += 1
        elif move.classification == MoveClassification.INACCURACY:
            inaccuracies += 1
        elif move.classification == MoveClassification.MISTAKE:
            mistakes += 1
        elif move.classification == MoveClassification.BLUNDER:
            blunders += 1

        if move.delta is not None:
            total_eval_loss += max(0, move.delta)
            eval_loss_count += 1

    average_eval_loss = total_eval_loss / eval_loss_count if eval_loss_count else 0

    return PlayerSummary(
        total_moves=len(analysis),
        best_moves=best_moves,
        good_moves=good_moves,
        inaccuracies=inaccuracies,
        mistakes=mistakes,
        blunders=blunders,
        average_eval_loss=round(average_eval_loss, 2),
    )

def build_summary(analysis: list[MoveAnalysis]) -> AnalysisSummary:
    white_moves = [
        move for move in analysis
        if move.move_colour == MoveColour.WHITE
    ]

    black_moves = [
        move for move in analysis
        if move.move_colour == MoveColour.BLACK
    ]

    return AnalysisSummary(
        white=build_player_summary(white_moves),
        black=build_player_summary(black_moves),
    )