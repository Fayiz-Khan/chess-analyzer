from dataclasses import dataclass


@dataclass
class PositionRecord:
    fen: str
    move_san: str
    next_moves: list[str]
    result: str | None = None
    white_elo: int | None = None
    black_elo: int | None = None
    eco: str | None = None
    opening: str | None = None
