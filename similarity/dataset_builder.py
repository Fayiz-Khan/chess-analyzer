import io
import json
from pathlib import Path

import chess.pgn
from similarity.position_record import PositionRecord


def safe_int(value: str | None) -> int | None:
    try:
        return int(value) if value is not None else None
    except ValueError:
        return None


def get_next_moves(board, moves, start_index: int, count: int) -> list[str]:
    temp_board = board.copy()

    # Advance to the position AFTER the current move
    temp_board.push(moves[start_index])

    next_moves = []

    for next_move in moves[start_index + 1 : start_index + 1 + count]:
        next_moves.append(temp_board.san(next_move))
        temp_board.push(next_move)

    return next_moves


def record_from_move(game, board, moves, index: int, next_move_count: int) -> PositionRecord:
    move = moves[index]

    return PositionRecord(
        fen=board.fen(),
        move_san=board.san(move),
        next_moves=get_next_moves(board, moves, index, next_move_count),
        result=game.headers.get("Result"),
        white_elo=safe_int(game.headers.get("WhiteElo")),
        black_elo=safe_int(game.headers.get("BlackElo")),
        eco=game.headers.get("ECO"),
        opening=game.headers.get("Opening"),
    )


def iter_games_from_pgn(path: Path):
    with open(path, "r", encoding="utf-8") as pgn_file:
        while True:
            game = chess.pgn.read_game(pgn_file)
            if game is None:
                break
            yield game


def position_record_to_dict(record: PositionRecord) -> dict[str, object]:
    return {
        "fen": record.fen,
        "move_san": record.move_san,
        "next_moves": record.next_moves,
        "result": record.result,
        "white_elo": record.white_elo,
        "black_elo": record.black_elo,
        "eco": record.eco,
        "opening": record.opening,
    }


def position_record_from_dict(data: dict[str, object]) -> PositionRecord:
    return PositionRecord(
        fen=str(data["fen"]),
        move_san=str(data["move_san"]),
        next_moves=list(data.get("next_moves", [])),
        result=data.get("result"),
        white_elo=data.get("white_elo"),
        black_elo=data.get("black_elo"),
        eco=data.get("eco"),
        opening=data.get("opening"),
    )


def build_dataset(
    input_path: Path,
    output_path: Path,
    max_games: int = 1000,
    next_move_count: int = 5,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    games_processed = 0
    positions_written = 0

    with open(output_path, "w", encoding="utf-8") as output_file:
        for game in iter_games_from_pgn(input_path):
            if games_processed >= max_games:
                break

            board = game.board()
            moves = list(game.mainline_moves())

            for index, _ in enumerate(moves):
                record = record_from_move(game, board, moves, index, next_move_count)
                output_file.write(json.dumps(position_record_to_dict(record)) + "\n")
                positions_written += 1
                board.push(moves[index])

            games_processed += 1

            if games_processed % 100 == 0:
                print(f"Processed {games_processed} games, wrote {positions_written} positions")

    print(f"Done. Processed {games_processed} games, wrote {positions_written} positions")


def load_position_records(path: Path, max_records: int | None = None) -> list[PositionRecord]:
    records: list[PositionRecord] = []

    with open(path, encoding="utf-8") as input_file:
        for line in input_file:
            if max_records is not None and len(records) >= max_records:
                break

            records.append(position_record_from_dict(json.loads(line)))

    return records
