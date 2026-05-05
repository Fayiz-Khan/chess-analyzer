from enum import Enum
from dataclasses import dataclass

class MoveClassification(Enum):
    BEST = "Best"
    GOOD = "Good"
    INACCURACY = "Inaccuracy"
    MISTAKE = "Mistake"
    BLUNDER = "Blunder"

class MoveColour(Enum):
    WHITE = "White"
    BLACK = "Black"

@dataclass
class MoveAnalysis:
    move_number: int
    move_colour: MoveColour
    move_san: str
    best_move_san: str
    board_state: str 
    eval_before: float
    eval_after: float
    delta: float
    classification: MoveClassification
    is_checkmate: bool = False
    