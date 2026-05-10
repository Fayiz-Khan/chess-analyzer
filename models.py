import json
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
    fen_state_before: str
    fen_state_after: str
    eval_before: float
    eval_after: float
    delta: float
    classification: MoveClassification
    is_checkmate: bool = False

    def to_dict(self) -> dict[str, object]:
        return {
            "move_number": self.move_number,
            "move_colour": self.move_colour.value,
            "move_san": self.move_san,
            "best_move_san": self.best_move_san,
            "fen_state_before": self.fen_state_before,
            "fen_state_after": self.fen_state_after,
            "eval_before": round(self.eval_before, 2),
            "eval_after": round(self.eval_after, 2),
            "delta": round(self.delta, 2),
            "classification": self.classification.value,
            "is_checkmate": self.is_checkmate,
        }
    
@dataclass
class PlayerSummary:
    total_moves: int
    best_moves: int
    good_moves: int
    inaccuracies: int
    mistakes: int
    blunders: int
    average_eval_loss: float

    def to_dict(self) -> dict[str, object]:
        return {
            "total_moves": self.total_moves,
            "best_moves": self.best_moves,
            "good_moves": self.good_moves,
            "inaccuracies": self.inaccuracies,
            "mistakes": self.mistakes,
            "blunders": self.blunders,
            "average_eval_loss": self.average_eval_loss,
        }

@dataclass
class AnalysisSummary:
    white: PlayerSummary
    black: PlayerSummary

    def to_dict(self) -> dict[str, object]:
        return {
            "white": self.white.to_dict(),
            "black": self.black.to_dict(),
        }

class AnalysisEncoder(json.JSONEncoder):
    def default(self, obj: object) -> object:
        if isinstance(obj, (MoveAnalysis, AnalysisSummary)):
            return obj.to_dict()
        return super().default(obj)
