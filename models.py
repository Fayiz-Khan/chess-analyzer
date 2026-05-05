from enum import Enum
from dataclasses import dataclass
import json

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
    fen_state_before: str
    fen_state_after: str
    eval_before: float
    eval_after: float
    delta: float
    classification: MoveClassification
    is_checkmate: bool = False

    def to_dict(self):
        return {
            "move_number": self.move_number,
            "move_colour": self.move_colour.value,
            "move_san": self.move_san,
            "best_move_san": self.best_move_san,
            "fen_state_before": self.fen_state_before,
            "fen_state_after": self.fen_state_after,
            "eval_before": self.eval_before,
            "eval_after": self.eval_after,
            "delta": self.delta,
            "classification": self.classification.value,
            "is_checkmate": self.is_checkmate, 
        }

class MoveEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, MoveAnalysis):
            return obj.to_dict()
        return super().default(obj)