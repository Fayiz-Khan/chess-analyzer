import chess

from analyzer.analyzer import classify_move
from models.models import MoveClassification, Evaluation, MoveColour

NORMAL_EVAL = Evaluation(centipawns=0.0, mate_in=None)

def test_classify_move_returns_best_when_player_move_matches_best_move():
    move = chess.Move.from_uci("e2e4")

    assert classify_move(5.0, move, move, NORMAL_EVAL, MoveColour.WHITE) == MoveClassification.BEST


def test_classify_move_blunder_at_2_point_0():
    player_move = chess.Move.from_uci("e2e4")
    best_move = chess.Move.from_uci("d2d4")

    assert classify_move(2.0, player_move, best_move, NORMAL_EVAL, MoveColour.WHITE) == MoveClassification.BLUNDER


def test_classify_move_mistake_below_blunder_threshold():
    player_move = chess.Move.from_uci("e2e4")
    best_move = chess.Move.from_uci("d2d4")

    assert classify_move(1.99, player_move, best_move, NORMAL_EVAL, MoveColour.WHITE) == MoveClassification.MISTAKE


def test_classify_move_mistake_at_1_point_0():
    player_move = chess.Move.from_uci("e2e4")
    best_move = chess.Move.from_uci("d2d4")

    assert classify_move(1.0, player_move, best_move, NORMAL_EVAL, MoveColour.WHITE) == MoveClassification.MISTAKE


def test_classify_move_inaccuracy_below_mistake_threshold():
    player_move = chess.Move.from_uci("e2e4")
    best_move = chess.Move.from_uci("d2d4")

    assert classify_move(0.99, player_move, best_move, NORMAL_EVAL, MoveColour.WHITE) == MoveClassification.INACCURACY


def test_classify_move_inaccuracy_at_0_point_3():
    player_move = chess.Move.from_uci("e2e4")
    best_move = chess.Move.from_uci("d2d4")

    assert classify_move(0.3, player_move, best_move, NORMAL_EVAL, MoveColour.WHITE) == MoveClassification.INACCURACY


def test_classify_move_good_below_inaccuracy_threshold():
    player_move = chess.Move.from_uci("e2e4")
    best_move = chess.Move.from_uci("d2d4")

    assert classify_move(0.29, player_move, best_move, NORMAL_EVAL, MoveColour.WHITE) == MoveClassification.GOOD


def test_classify_move_works_when_best_move_is_none():
    player_move = chess.Move.from_uci("e2e4")

    assert classify_move(2.0, player_move, None, NORMAL_EVAL, MoveColour.WHITE) == MoveClassification.BLUNDER

def test_classify_move_blunder_when_white_allows_mate():
    player_move = chess.Move.from_uci("g2g4")
    best_move = chess.Move.from_uci("f4e5")
    eval_after = Evaluation(centipawns=None, mate_in=-1)

    assert classify_move(
        None,
        player_move,
        best_move,
        eval_after,
        MoveColour.WHITE,
    ) == MoveClassification.BLUNDER

def test_classify_move_blunder_when_black_allows_mate():
    player_move = chess.Move.from_uci("g7g5")
    best_move = chess.Move.from_uci("e7e5")
    eval_after = Evaluation(centipawns=None, mate_in=1)

    assert classify_move(
        None,
        player_move,
        best_move,
        eval_after,
        MoveColour.BLACK,
    ) == MoveClassification.BLUNDER
