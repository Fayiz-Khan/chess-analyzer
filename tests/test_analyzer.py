import chess

from analyzer import classify_move
from models import MoveClassification

def test_classify_move_returns_best_when_player_move_matches_best_move():
    move = chess.Move.from_uci("e2e4")

    assert classify_move(5.0, move, move) == MoveClassification.BEST


def test_classify_move_blunder_at_2_point_0():
    player_move = chess.Move.from_uci("e2e4")
    best_move = chess.Move.from_uci("d2d4")

    assert classify_move(2.0, player_move, best_move) == MoveClassification.BLUNDER


def test_classify_move_mistake_below_blunder_threshold():
    player_move = chess.Move.from_uci("e2e4")
    best_move = chess.Move.from_uci("d2d4")

    assert classify_move(1.99, player_move, best_move) == MoveClassification.MISTAKE


def test_classify_move_mistake_at_1_point_0():
    player_move = chess.Move.from_uci("e2e4")
    best_move = chess.Move.from_uci("d2d4")

    assert classify_move(1.0, player_move, best_move) == MoveClassification.MISTAKE


def test_classify_move_inaccuracy_below_mistake_threshold():
    player_move = chess.Move.from_uci("e2e4")
    best_move = chess.Move.from_uci("d2d4")

    assert classify_move(0.99, player_move, best_move) == MoveClassification.INACCURACY


def test_classify_move_inaccuracy_at_0_point_3():
    player_move = chess.Move.from_uci("e2e4")
    best_move = chess.Move.from_uci("d2d4")

    assert classify_move(0.3, player_move, best_move) == MoveClassification.INACCURACY


def test_classify_move_good_below_inaccuracy_threshold():
    player_move = chess.Move.from_uci("e2e4")
    best_move = chess.Move.from_uci("d2d4")

    assert classify_move(0.29, player_move, best_move) == MoveClassification.GOOD


def test_classify_move_works_when_best_move_is_none():
    player_move = chess.Move.from_uci("e2e4")

    assert classify_move(2.0, player_move, None) == MoveClassification.BLUNDER
