import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from similarity.dataset_builder import build_dataset


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a position dataset from a PGN file."
    )

    parser.add_argument("input", help="Path to a PGN file")
    parser.add_argument("--output", default="data/positions.jsonl")
    parser.add_argument("--max-games", type=int, default=1000)
    parser.add_argument("--next-moves", type=int, default=5)

    args = parser.parse_args()
    input_path = Path(args.input)

    if not input_path.exists():
        parser.error(
            f"Input PGN not found: {input_path}. Download/extract a Lichess Elite PGN or pass another PGN path."
        )

    build_dataset(
        input_path=input_path,
        output_path=Path(args.output),
        max_games=args.max_games,
        next_move_count=args.next_moves,
    )


if __name__ == "__main__":
    main()
