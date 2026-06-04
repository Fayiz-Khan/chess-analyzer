from api.lichess_client import call_masters_database
from models.models import MasterPositionStats, MoveAnalysis, EnrichedMoveAnalysis

def enrich_move_analysis(move_analysis: MoveAnalysis) -> EnrichedMoveAnalysis:
    played_master_move = None

    data = call_masters_database(move_analysis.fen_state_before)

    stats = MasterPositionStats.from_json(data)

    for move in stats.master_moves:
        if move.san == move_analysis.move_san:
            played_master_move = move
            break
        
    return EnrichedMoveAnalysis(
        move_analysis=move_analysis,
        master_position_stats=stats,
        played_master_move=played_master_move,
    )
