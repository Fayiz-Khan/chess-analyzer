from models.models import (
    MoveAnalysis,
    MoveClassification,
    MoveColour,
    PlayerSummary,
    AnalysisSummary,
    Evaluation, 
    MasterPositionStats, 
    MasterMove,
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

def test_master_move_total_games():
    move = MasterMove(
        san = "c5",
        average_rating = 2375,
        white_wins = 235,
        black_wins = 253,
        draws = 237,
    )

    assert(move.total_games == 725)

def test_master_position_stats_from_json():
    data = {
        "white": 1872,
        "black": 2288,
        "draws": 2537,
        "moves": [
            {
                "san": "c5",
                "averageRating": 2375,
                "white": 235,
                "black": 253,
                "draws": 237,
            }
        ],
    }

    stats = MasterPositionStats.from_json(data)

    assert stats.white_wins == 1872
    assert stats.black_wins == 2288
    assert stats.draws == 2537

    assert len(stats.master_moves) == 1
    assert stats.master_moves[0].san == "c5"
    assert stats.master_moves[0].average_rating == 2375
    assert stats.master_moves[0].white_wins == 235
    assert stats.master_moves[0].black_wins == 253
    assert stats.master_moves[0].draws == 237
    assert stats.master_moves[0].total_games == 725

def test_master_position_total_games():
    stats = MasterPositionStats(
        white_wins=1872,
        black_wins=2288,
        draws=2537,
        master_moves=[],
    )

    assert stats.total_games == 6697
