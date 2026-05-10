from models import MoveAnalysis, MoveClassification, MoveColour, AnalysisSummary
from summarizer import build_player_summary, build_summary

def make_move(
    classification: MoveClassification,
    delta: float,
    move_colour: MoveColour = MoveColour.WHITE,
    is_checkmate: bool = False,
) -> MoveAnalysis:
    return MoveAnalysis(
        move_number=1,
        move_colour=move_colour,
        move_san="e4",
        best_move_san="e4",
        fen_state_before="before",
        fen_state_after="after",
        eval_before=0.0,
        eval_after=0.0,
        delta=delta,
        classification=classification,
        is_checkmate=is_checkmate,
    )


def test_build_player_summary_empty_list_returns_zero_summary():
    summary = build_player_summary([])

    assert summary.total_moves == 0
    assert summary.best_moves == 0
    assert summary.good_moves == 0
    assert summary.inaccuracies == 0
    assert summary.mistakes == 0
    assert summary.blunders == 0
    assert summary.average_eval_loss == 0


def test_build_player_summary_counts_all_classifications():
    moves = [
        make_move(MoveClassification.BEST, 0.0),
        make_move(MoveClassification.GOOD, 0.1),
        make_move(MoveClassification.INACCURACY, 0.3),
        make_move(MoveClassification.MISTAKE, 1.0),
        make_move(MoveClassification.BLUNDER, 2.0),
    ]

    summary = build_player_summary(moves)

    assert summary.total_moves == 5
    assert summary.best_moves == 1
    assert summary.good_moves == 1
    assert summary.inaccuracies == 1
    assert summary.mistakes == 1
    assert summary.blunders == 1


def test_build_player_summary_average_eval_loss_uses_positive_deltas_only():
    moves = [
        make_move(MoveClassification.GOOD, 0.5),
        make_move(MoveClassification.GOOD, -1.0),
        make_move(MoveClassification.GOOD, 1.0),
    ]

    summary = build_player_summary(moves)

    assert summary.average_eval_loss == 0.5


def test_build_player_summary_excludes_checkmate_from_average_loss():
    moves = [
        make_move(MoveClassification.GOOD, 1.0),
        make_move(MoveClassification.BEST, 999, is_checkmate=True),
    ]

    summary = build_player_summary(moves)

    assert summary.total_moves == 2
    assert summary.average_eval_loss == 1.0


def test_build_player_summary_excludes_large_sentinel_deltas():
    moves = [
        make_move(MoveClassification.GOOD, 1.0),
        make_move(MoveClassification.BLUNDER, 999),
    ]

    summary = build_player_summary(moves)

    assert summary.average_eval_loss == 1.0


def test_build_player_summary_rounds_average_eval_loss_to_two_decimals():
    moves = [
        make_move(MoveClassification.GOOD, 0.333),
        make_move(MoveClassification.GOOD, 0.333),
    ]

    summary = build_player_summary(moves)

    assert summary.average_eval_loss == 0.33


def test_build_summary_splits_white_and_black_moves():
    moves = [
        make_move(MoveClassification.BLUNDER, 2.0, MoveColour.WHITE),
        make_move(MoveClassification.BEST, 0.0, MoveColour.BLACK),
    ]

    summary = build_summary(moves)

    assert isinstance(summary, AnalysisSummary)
    assert summary.white.total_moves == 1
    assert summary.white.blunders == 1
    assert summary.black.total_moves == 1
    assert summary.black.best_moves == 1
    