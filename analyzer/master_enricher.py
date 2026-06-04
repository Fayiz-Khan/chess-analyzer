from api.lichess_client import call_masters_database, call_online_players_database
from models.models import MasterPositionStats, MoveAnalysis, EnrichedMoveAnalysis, OnlinePositionStats

def enrich_move_analysis(move_analysis: MoveAnalysis) -> EnrichedMoveAnalysis:
    played_master_move = None
    played_online_game_move = None

    master_data = call_masters_database(move_analysis.fen_state_before)

    master_stats = MasterPositionStats.from_json(master_data)

    online_player_data = call_online_players_database(move_analysis.fen_state_before)

    online_player_stats = OnlinePositionStats.from_json(online_player_data)

    for move in master_stats.master_moves:
        if move.san == move_analysis.move_san:
            played_master_move = move
            break

    for move in online_player_stats.online_player_moves:
        if move.san == move_analysis.move_san:
            played_online_game_move = move
            break
        
    return EnrichedMoveAnalysis(
        move_analysis=move_analysis,
        master_position_stats=master_stats,
        played_master_move=played_master_move,
        online_position_stats=online_player_stats,
        played_online_player_move=played_online_game_move,
    )
