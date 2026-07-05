from dataclasses import dataclass
from pathlib import Path

from similarity.faiss_index import PositionVectorIndex
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


def find_similar_positions_from_index(
    query_fen: str,
    index: PositionVectorIndex,
    k: int = 5,
) -> list[SimilarPosition]:
    return [
        SimilarPosition(record=record, distance=distance)
        for record, distance in index.search(query_fen, k=k)
    ]


def find_similar_positions_from_dataset(
    query_fen: str,
    dataset_path: Path,
    k: int = 5,
    max_records: int | None = None,
    index_path: Path | None = None,
    metadata_path: Path | None = None,
) -> list[SimilarPosition]:
    if index_path is not None and metadata_path is not None and index_path.exists() and metadata_path.exists():
        index = PositionVectorIndex.load(index_path, metadata_path)
        return find_similar_positions_from_index(query_fen, index, k=k)

    index = PositionVectorIndex.from_dataset(dataset_path, max_records=max_records)
    return find_similar_positions_from_index(query_fen, index, k=k)


def euclidean_distance(vector_a: list[float], vector_b: list[float]) -> float:
    if len(vector_a) != len(vector_b):
        raise ValueError("Vectors must have the same length")

    return sum((a - b) ** 2 for a, b in zip(vector_a, vector_b)) ** 0.5
