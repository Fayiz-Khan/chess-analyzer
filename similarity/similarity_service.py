from dataclasses import dataclass
from pathlib import Path

from similarity.dataset_builder import load_position_records
from similarity.feature_extractor import extract_features_from_fen
from similarity.position_record import PositionRecord


@dataclass
class SimilarPosition:
    record: PositionRecord
    distance: float


def find_similar_positions(
    query_fen: str,
    records: list[PositionRecord],
    k: int = 5,
) -> list[SimilarPosition]:
    query_vector = extract_features_from_fen(query_fen)

    scored_positions: list[SimilarPosition] = []

    for record in records:
        record_vector = extract_features_from_fen(record.fen)
        distance = euclidean_distance(query_vector, record_vector)

        scored_positions.append(
            SimilarPosition(
                record=record,
                distance=distance,
            )
        )

    return sorted(scored_positions, key=lambda item: item.distance)[:k]


def find_similar_positions_from_dataset(
    query_fen: str,
    dataset_path: Path,
    k: int = 5,
    max_records: int | None = None,
) -> list[SimilarPosition]:
    records = load_position_records(dataset_path, max_records=max_records)
    return find_similar_positions(query_fen, records, k=k)


def euclidean_distance(vector_a: list[float], vector_b: list[float]) -> float:
    if len(vector_a) != len(vector_b):
        raise ValueError("Vectors must have the same length")

    return sum((a - b) ** 2 for a, b in zip(vector_a, vector_b)) ** 0.5
