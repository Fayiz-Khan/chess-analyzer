import chess
import json
from pathlib import Path

import numpy as np
import pytest

from similarity.dataset_builder import position_record_to_dict
from similarity.faiss_index import PositionVectorIndex, vectors_from_records
from similarity.position_record import PositionRecord
from similarity.similarity_service import (
    find_similar_positions,
    find_similar_positions_from_dataset,
    find_similar_positions_from_index,
)


def sample_records() -> list[PositionRecord]:
    return [
        PositionRecord(
            fen=chess.STARTING_FEN,
            move_san="e4",
            next_moves=["e5", "Nf3"],
            opening="King's Pawn Game",
        ),
        PositionRecord(
            fen="rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1",
            move_san="e5",
            next_moves=["Nf3", "Nc6"],
            opening="King's Pawn Game",
        ),
        PositionRecord(
            fen="8/8/8/8/8/8/8/4K3 w - - 0 1",
            move_san="Kd2",
            next_moves=[],
        ),
    ]


def test_vectors_from_records_returns_float32_matrix():
    vectors = vectors_from_records(sample_records())

    assert vectors.dtype == np.float32
    assert vectors.shape == (3, len(vectors[0]))


def test_position_vector_index_search_returns_closest_record():
    index = PositionVectorIndex.from_records(sample_records())
    results = index.search(chess.STARTING_FEN, k=1)

    assert len(results) == 1
    assert results[0][0].fen == chess.STARTING_FEN
    assert results[0][1] == pytest.approx(0.0)


def test_position_vector_index_save_and_load(tmp_path: Path):
    index_path = tmp_path / "positions.faiss"
    metadata_path = tmp_path / "positions_metadata.jsonl"
    records = sample_records()

    original = PositionVectorIndex.from_records(records)
    original.save(index_path, metadata_path)

    loaded = PositionVectorIndex.load(index_path, metadata_path)
    results = loaded.search(chess.STARTING_FEN, k=2)

    assert len(results) == 2
    assert results[0][0].fen == chess.STARTING_FEN


def test_find_similar_positions_from_index_matches_brute_force():
    records = sample_records()
    index = PositionVectorIndex.from_records(records)
    query_fen = chess.STARTING_FEN

    faiss_results = find_similar_positions_from_index(query_fen, index, k=2)
    brute_force_results = find_similar_positions(query_fen, records, k=2)

    assert [item.record.fen for item in faiss_results] == [
        item.record.fen for item in brute_force_results
    ]


def test_find_similar_positions_from_dataset_uses_saved_index(tmp_path: Path):
    dataset_path = tmp_path / "positions.jsonl"
    index_path = tmp_path / "positions.faiss"
    metadata_path = tmp_path / "positions_metadata.jsonl"
    records = sample_records()

    with open(dataset_path, "w", encoding="utf-8") as dataset_file:
        for record in records:
            dataset_file.write(json.dumps(position_record_to_dict(record)) + "\n")

    PositionVectorIndex.from_records(records).save(index_path, metadata_path)

    results = find_similar_positions_from_dataset(
        query_fen=chess.STARTING_FEN,
        dataset_path=dataset_path,
        k=1,
        index_path=index_path,
        metadata_path=metadata_path,
    )

    assert len(results) == 1
    assert results[0].record.fen == chess.STARTING_FEN


def test_find_similar_positions_from_dataset_builds_index_from_jsonl(tmp_path: Path):
    dataset_path = tmp_path / "positions.jsonl"
    records = sample_records()

    with open(dataset_path, "w", encoding="utf-8") as dataset_file:
        for record in records:
            dataset_file.write(json.dumps(position_record_to_dict(record)) + "\n")

    results = find_similar_positions_from_dataset(
        query_fen=chess.STARTING_FEN,
        dataset_path=dataset_path,
        k=1,
    )

    assert len(results) == 1
    assert results[0].record.fen == chess.STARTING_FEN


def test_position_vector_index_from_empty_records_raises():
    with pytest.raises(ValueError, match="empty records"):
        PositionVectorIndex.from_records([])
