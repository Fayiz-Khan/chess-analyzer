from models import (
    MoveAnalysis,
    MoveClassification,
    MoveColour,
    PlayerSummary,
    AnalysisSummary,
)

def test_move_analysis_to_dict_serializes_enums_and_rounds_values():
    move = MoveAnalysis(
        move_number=1,
        move_colour=MoveColour.WHITE,
        move_san="e4",
        best_move_san="e4",
        fen_state_before="before",
        fen_state_after="after",
        eval_before=0.126,
        eval_after=-0.987,
        delta=1.113,
        classification=MoveClassification.GOOD,
        is_checkmate=False,
    )

    result = move.to_dict()

    assert result["move_colour"] == "White"
    assert result["classification"] == "Good"
    assert result["eval_before"] == 0.13
    assert result["eval_after"] == -0.99
    assert result["delta"] == 1.11
    assert result["is_checkmate"] is False


def test_player_summary_to_dict_returns_all_fields():
    summary = PlayerSummary(
        total_moves=10,
        best_moves=2,
        good_moves=3,
        inaccuracies=2,
        mistakes=1,
        blunders=2,
        average_eval_loss=0.75,
    )

    result = summary.to_dict()

    assert result == {
        "total_moves": 10,
        "best_moves": 2,
        "good_moves": 3,
        "inaccuracies": 2,
        "mistakes": 1,
        "blunders": 2,
        "average_eval_loss": 0.75,
    }


def test_analysis_summary_to_dict_nests_white_and_black_summaries():
    white = PlayerSummary(1, 1, 0, 0, 0, 0, 0.0)
    black = PlayerSummary(1, 0, 1, 0, 0, 0, 0.2)

    summary = AnalysisSummary(white=white, black=black)

    result = summary.to_dict()

    assert result["white"]["best_moves"] == 1
    assert result["black"]["good_moves"] == 1