from models.models import (
    EnrichedMoveAnalysis,
    Evaluation,
    MasterMove,
    MasterPositionStats,
    MoveAnalysis,
    MoveClassification,
    MoveColour,
    OnlinePlayerMove,
    OnlinePositionStats,
)
from analyzer.response_builder import serialize_analyze_response, serialize_enriched_move
from similarity.position_record import PositionRecord
from similarity.similarity_service import SimilarPosition


def build_enriched_move() -> EnrichedMoveAnalysis:
    move_analysis = MoveAnalysis(
        move_number=1,
        move_colour=MoveColour.WHITE,
        move_san="e4",
        best_move_san="e4",
        fen_state_before="before",
        fen_state_after="after",
        eval_before=Evaluation(centipawns=0.1, mate_in=None),
        eval_after=Evaluation(centipawns=0.2, mate_in=None),
        delta=0.1,
        classification=MoveClassification.GOOD,
        is_checkmate=False,
    )

    master_move = MasterMove(
        san="e4",
        average_rating=2400,
        white_wins=5,
        black_wins=2,
        draws=3,
    )

    online_move = OnlinePlayerMove(
        san="e4",
        average_rating=1605,
        white_wins=10,
        black_wins=5,
        draws=5,
    )

    return EnrichedMoveAnalysis(
        move_analysis=move_analysis,
        master_position_stats=MasterPositionStats(
            white_wins=10,
            black_wins=5,
            draws=5,
            master_moves=[master_move],
        ),
        played_master_move=master_move,
        online_position_stats=OnlinePositionStats(
            white_wins=20,
            black_wins=10,
            draws=10,
            online_player_moves=[online_move],
        ),
        played_online_player_move=online_move,
    )


def test_serialize_enriched_move_returns_nested_dicts():
    enriched = build_enriched_move()

    result = serialize_enriched_move(enriched)

    assert result["engine"]["move_san"] == "e4"
    assert result["masters"]["played_move"]["san"] == "e4"
    assert result["online_players"]["position"]["online_player_moves"][0]["san"] == "e4"


def test_serialize_enriched_move_includes_similar_positions():
    enriched = build_enriched_move()
    similar_positions = [
        SimilarPosition(
            record=PositionRecord(
                fen="fen",
                move_san="d4",
                next_moves=["d5"],
                opening="Queen's Pawn Game",
            ),
            distance=1.25,
        )
    ]

    result = serialize_enriched_move(enriched, similar_positions=similar_positions)

    assert result["similar_positions"][0]["move_san"] == "d4"
    assert result["similar_positions"][0]["opening"] == "Queen's Pawn Game"
