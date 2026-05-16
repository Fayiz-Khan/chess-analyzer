from models import (
    MoveAnalysis,
    MoveClassification,
    MoveColour,
    PlayerSummary,
    AnalysisSummary,
    Evaluation
)

def test_move_analysis_to_dict_serializes_enums_and_rounds_values():
    move = MoveAnalysis(
        move_number=1,
        move_colour=MoveColour.WHITE,
        move_san="e4",
        best_move_san="e4",
        fen_state_before="before",
        fen_state_after="after",
        eval_before=Evaluation(centipawns=0.126, mate_in=None),
        eval_after=Evaluation(centipawns=-0.987, mate_in=None),        
        delta=1.113,
        classification=MoveClassification.GOOD,
        is_checkmate=False,
    )

    result = move.to_dict()

    assert result["move_colour"] == "White"
    assert result["classification"] == "Good"

    assert result["delta"] == 1.11
    assert result["is_checkmate"] is False

    assert result["eval_before"] == {
        "centipawns": 0.126,
        "mate_in": None,
    }
    assert result["eval_after"] == {
        "centipawns": -0.987,
        "mate_in": None,
    }

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

def test_evaluation_serializes_mate_scores():
    evaluation = Evaluation(
        centipawns=None,
        mate_in=-1,
    )
    result = evaluation.to_dict()

    assert result == {
        "centipawns": None,
        "mate_in": -1,
    }

def test_move_analysis_to_dict_handles_none_delta():
    move = MoveAnalysis(
        move_number=1,
        move_colour=MoveColour.WHITE,
        move_san="Qh4#",
        best_move_san="Qh4#",
        fen_state_before="before",
        fen_state_after="after",
        eval_before=Evaluation(None, -1),
        eval_after=Evaluation(None, 0),
        delta=None,
        classification=MoveClassification.BEST,
        is_checkmate=True,
    )

    result = move.to_dict()

    assert result["delta"] is None
    assert result["is_checkmate"] is True
