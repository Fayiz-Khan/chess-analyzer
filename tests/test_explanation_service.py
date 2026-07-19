from analyzer.explanation_service import build_explanation_prompt
from models.models import (
    EnrichedMoveAnalysis,
    Evaluation,
    MasterPositionStats,
    MoveAnalysis,
    MoveClassification,
    MoveColour,
    OnlinePositionStats,
)


def test_build_explanation_prompt_identifies_best_move_as_same_side():
    move = EnrichedMoveAnalysis(
        move_analysis=MoveAnalysis(
            move_number=17,
            move_colour=MoveColour.WHITE,
            move_san="Kh1",
            best_move_san="c5",
            fen_state_before="r1q2rk1/pppb1pb1/2np2np/4p1p1/2PP4/2N1B1P1/PP1QBPKP/R4RN1 w - - 4 17",
            fen_state_after="r1q2rk1/pppb1pb1/2np2np/4p1p1/2PP4/2N1B1P1/PP1QBPKP/R4RNK b - - 5 17",
            eval_before=Evaluation(centipawns=1.01, mate_in=None),
            eval_after=Evaluation(centipawns=0.70, mate_in=None),
            delta=0.31,
            classification=MoveClassification.INACCURACY,
        ),
        master_position_stats=MasterPositionStats(
            white_wins=0,
            black_wins=0,
            draws=0,
            master_moves=[],
        ),
        played_master_move=None,
        online_position_stats=OnlinePositionStats(
            white_wins=0,
            black_wins=0,
            draws=0,
            online_player_moves=[],
        ),
        played_online_player_move=None,
    )

    prompt = build_explanation_prompt(move)

    assert "Side to move: White" in prompt
    assert "Best engine move for White: c5" in prompt
    assert "Position before the move:" in prompt
    assert "Treat the best engine move as a legal move for the same side" in prompt
    assert "Do not describe it as the opponent's move" in prompt
