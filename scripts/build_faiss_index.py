import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from config import FAISS_INDEX_PATH, FAISS_METADATA_PATH, POSITION_DATASET_PATH
from similarity.faiss_index import PositionVectorIndex


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a FAISS index from a position dataset."
    )

    parser.add_argument(
        "--dataset",
        default=str(POSITION_DATASET_PATH),
        help="Path to positions.jsonl",
    )
    parser.add_argument(
        "--index",
        default=str(FAISS_INDEX_PATH),
        help="Path to write the FAISS index",
    )
    parser.add_argument(
        "--metadata",
        default=str(FAISS_METADATA_PATH),
        help="Path to write position metadata",
    )
    parser.add_argument(
        "--max-records",
        type=int,
        default=None,
        help="Maximum number of records to index",
    )

    args = parser.parse_args()

    index = PositionVectorIndex.from_dataset(
        dataset_path=Path(args.dataset),
        max_records=args.max_records,
    )
    index.save(Path(args.index), Path(args.metadata))

    print(f"Indexed {len(index.records)} positions")
    print(f"Wrote index to {args.index}")
    print(f"Wrote metadata to {args.metadata}")


if __name__ == "__main__":
    main()
