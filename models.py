from enum import Enum

class MoveClassification(Enum):
    BEST = "Best"
    GOOD = "Good"
    INACCURACY = "Inaccuracy"
    MISTAKE = "Mistake"
    BLUNDER = "Blunder"

@dataclass
class MoveAnalysis:
    move_san: str
    eval_before: float
    eval_after: float
    delta: float
    classification: MoveClassification
    