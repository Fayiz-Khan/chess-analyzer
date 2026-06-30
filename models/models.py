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
class Evaluation:
    centipawns: float | None
    mate_in: int | None

    def to_dict(self) -> dict[str, object]:
        return {
            "centipawns": self.centipawns,
            "mate_in": self.mate_in,
        }

@dataclass
class MoveAnalysis:
    move_number: int
    move_colour: MoveColour
    move_san: str
    best_move_san: str
    fen_state_before: str
    fen_state_after: str
    eval_before: Evaluation
    eval_after: Evaluation
    delta: float | None
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
            "eval_before": self.eval_before.to_dict(),
            "eval_after": self.eval_after.to_dict(),
            "delta": round(self.delta, 2) if self.delta is not None else None,
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
    
@dataclass
class MasterMove:
    san: str
    average_rating: int
    white_wins: int
    black_wins: int
    draws: int

    @property
    def total_games(self) -> int:
        return self.white_wins + self.black_wins + self.draws
    
    @classmethod
    def from_json(cls, data: dict) -> "MasterMove":
        return cls(
            san = data["san"],
            average_rating = data["averageRating"],
            white_wins = data["white"],
            black_wins = data["black"],
            draws = data["draws"],
        )
    
    def to_dict(self) -> dict[str,object]:
        return{
            "san": self.san,
            "average_rating": self.average_rating,
            "white_wins": self.white_wins,
            "black_wins": self.black_wins,
            "draws": self.draws,
            "total_games": self.total_games,
        }

@dataclass
class MasterPositionStats: 
    white_wins: int
    black_wins: int
    draws: int
    master_moves: list[MasterMove]

    @property
    def total_games(self) -> int:
        return self.white_wins + self.black_wins + self.draws
    
    @classmethod
    def from_json(cls, data: dict) -> "MasterPositionStats":
        return cls(
            white_wins = data["white"],
            black_wins = data["black"],
            draws = data["draws"],
            master_moves =[
                MasterMove.from_json(move) for move in data["moves"]
            ],
        )
    
    def to_dict(self) -> dict[str,object]:
        return{
            "white_wins": self.white_wins,
            "black_wins": self.black_wins,
            "draws": self.draws,
            "master_moves": self.master_moves,
            "total_games": self.total_games,
        }
    
@dataclass
class OnlinePlayerMove:
    san: str
    average_rating: int
    white_wins: int
    black_wins: int
    draws: int

    @property
    def total_games(self) -> int:
        return self.white_wins + self.black_wins + self.draws
    
    @classmethod
    def from_json(cls, data: dict) -> "OnlinePlayerMove":
        return cls(
            san = data["san"],
            average_rating = data["averageRating"],
            white_wins = data["white"],
            black_wins = data["black"],
            draws = data["draws"],
        )
    
    def to_dict(self) -> dict[str,object]:
        return{
            "san": self.san,
            "average_rating": self.average_rating,
            "white_wins": self.white_wins,
            "black_wins": self.black_wins,
            "draws": self.draws,
            "total_games": self.total_games,
        }
    
@dataclass
class OnlinePositionStats:
    white_wins: int
    black_wins: int
    draws: int
    online_player_moves: list[OnlinePlayerMove]

    @property
    def total_games(self) -> int:
        return self.white_wins + self.black_wins + self.draws
    
    @classmethod
    def from_json(cls, data: dict) -> "OnlinePositionStats":
        return cls(
            white_wins = data["white"],
            black_wins = data["black"],
            draws = data["draws"],
            online_player_moves =[
                OnlinePlayerMove.from_json(move) for move in data["moves"]
            ],
        )
    
    def to_dict(self) -> dict[str,object]:
        return{
            "white_wins": self.white_wins,
            "black_wins": self.black_wins,
            "draws": self.draws,
            "online_player_moves": self.online_player_moves,
            "total_games": self.total_games,
        }
    
@dataclass
class EnrichedMoveAnalysis:
    move_analysis: MoveAnalysis
    master_position_stats: MasterPositionStats
    played_master_move: MasterMove | None
    online_position_stats: OnlinePositionStats
    played_online_player_move: OnlinePlayerMove | None
    explanation: str | None = None


    def to_dict(self) -> dict[str, object]:
        return{
            "engine": self.move_analysis,
            "masters": {
                "position": self.master_position_stats,
                "played_move": self.played_master_move,
            },
            "online_players": {
                "position": self.online_position_stats,
                "played_move": self.played_online_player_move, 
            }
        }
        
class AnalysisEncoder(json.JSONEncoder):
    def default(self, obj: object) -> object:
        if isinstance(obj, (MoveAnalysis, AnalysisSummary, PlayerSummary, Evaluation, EnrichedMoveAnalysis, MasterPositionStats, MasterMove, OnlinePositionStats, OnlinePlayerMove)):
            return obj.to_dict()
        return super().default(obj)
