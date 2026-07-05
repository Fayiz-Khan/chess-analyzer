import json
from pathlib import Path

import faiss
import numpy as np

from similarity.dataset_builder import (
    load_position_records,
    position_record_from_dict,
    position_record_to_dict,
)
from similarity.feature_extractor import extract_features_from_fen
from similarity.position_record import PositionRecord


class PositionVectorIndex:
    def __init__(self, records: list[PositionRecord], index: faiss.Index) -> None:
        self.records = records
        self.index = index

    @classmethod
    def from_records(cls, records: list[PositionRecord]) -> "PositionVectorIndex":
        if not records:
            raise ValueError("Cannot build index from empty records")

        vectors = vectors_from_records(records)
        dimension = vectors.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(vectors)
        return cls(records, index)

    @classmethod
    def from_dataset(
        cls,
        dataset_path: Path,
        max_records: int | None = None,
    ) -> "PositionVectorIndex":
        records = load_position_records(dataset_path, max_records=max_records)
        return cls.from_records(records)

    def search(self, query_fen: str, k: int) -> list[tuple[PositionRecord, float]]:
        if not self.records:
            return []

        query = np.array([extract_features_from_fen(query_fen)], dtype=np.float32)
        k = min(k, len(self.records))
        squared_distances, indices = self.index.search(query, k)

        results: list[tuple[PositionRecord, float]] = []

        for index, squared_distance in zip(indices[0], squared_distances[0]):
            if index < 0:
                continue

            distance = float(squared_distance) ** 0.5
            results.append((self.records[int(index)], distance))

        return results

    def save(self, index_path: Path, metadata_path: Path) -> None:
        index_path.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(index_path))

        with open(metadata_path, "w", encoding="utf-8") as metadata_file:
            for record in self.records:
                metadata_file.write(
                    json.dumps(position_record_to_dict(record)) + "\n"
                )

    @classmethod
    def load(cls, index_path: Path, metadata_path: Path) -> "PositionVectorIndex":
        index = faiss.read_index(str(index_path))
        records: list[PositionRecord] = []

        with open(metadata_path, encoding="utf-8") as metadata_file:
            for line in metadata_file:
                records.append(position_record_from_dict(json.loads(line)))

        return cls(records, index)


def vectors_from_records(records: list[PositionRecord]) -> np.ndarray:
    return np.array(
        [extract_features_from_fen(record.fen) for record in records],
        dtype=np.float32,
    )
