import chess

from similarity.feature_extractor import extract_features_from_fen
from similarity.position_record import PositionRecord
from similarity.similarity_service import euclidean_distance, find_similar_positions


def test_extract_features_from_fen_returns_vector():
    vector = extract_features_from_fen(chess.STARTING_FEN)

    assert isinstance(vector, list)
    assert len(vector) > 0


def test_euclidean_distance_returns_zero_for_same_vector():
    assert euclidean_distance([1, 2, 3], [1, 2, 3]) == 0


def test_find_similar_positions_returns_closest_record():
    query_fen = chess.STARTING_FEN

    records = [
        PositionRecord(
            fen=chess.STARTING_FEN,
            move_san="e4",
            next_moves=["e5", "Nf3"],
        ),
        PositionRecord(
            fen="8/8/8/8/8/8/8/4K3 w - - 0 1",
            move_san="Kd2",
            next_moves=[],
        ),
    ]

    results = find_similar_positions(query_fen, records, k=1)

    assert len(results) == 1
    assert results[0].record.fen == chess.STARTING_FEN
