from unittest.mock import patch

from analyzer.master_enricher import enrich_move_analysis
from models.models import (
    EnrichedMoveAnalysis,
    Evaluation,
    MoveAnalysis,
    MoveClassification,
    MoveColour,
)


def make_move_analysis(move_san: str) -> MoveAnalysis:
    return MoveAnalysis(
        move_number=1,
        move_colour=MoveColour.WHITE,
        move_san=move_san,
        best_move_san="e4",
        fen_state_before="fake fen before",
        fen_state_after="fake fen after",
        eval_before=Evaluation(centipawns=0.2, mate_in=None),
        eval_after=Evaluation(centipawns=0.3, mate_in=None),
        delta=0.1,
        classification=MoveClassification.GOOD,
        is_checkmate=False,
    )


@patch("analyzer.master_enricher.call_masters_database")
def test_enrich_move_analysis_returns_matching_master_move(mock_call_masters_database):
    mock_call_masters_database.return_value = {
        "white": 10,
        "black": 5,
        "draws": 5,
        "moves": [
            {
                "san": "e4",
                "averageRating": 2400,
                "white": 5,
                "black": 2,
                "draws": 3,
            }
        ],
    }

    move_analysis = make_move_analysis("e4")

    enriched = enrich_move_analysis(move_analysis)

    mock_call_masters_database.assert_called_once_with("fake fen before")

    assert isinstance(enriched, EnrichedMoveAnalysis)
    assert enriched.move_analysis == move_analysis
    assert enriched.master_position_stats.total_games == 20

    assert enriched.played_master_move is not None
    assert enriched.played_master_move.san == "e4"
    assert enriched.played_master_move.average_rating == 2400
    assert enriched.played_master_move.total_games == 10


@patch("analyzer.master_enricher.call_masters_database")
def test_enrich_move_analysis_returns_none_when_move_not_found(mock_call_masters_database):
    mock_call_masters_database.return_value = {
        "white": 10,
        "black": 5,
        "draws": 5,
        "moves": [
            {
                "san": "e4",
                "averageRating": 2400,
                "white": 5,
                "black": 2,
                "draws": 3,
            }
        ],
    }

    move_analysis = make_move_analysis("h4")

    enriched = enrich_move_analysis(move_analysis)

    mock_call_masters_database.assert_called_once_with("fake fen before")

    assert isinstance(enriched, EnrichedMoveAnalysis)
    assert enriched.move_analysis == move_analysis
    assert enriched.master_position_stats.total_games == 20
    assert enriched.played_master_move is None
    