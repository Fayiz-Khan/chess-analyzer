from models.models import EnrichedMoveAnalysis, MoveAnalysis, AnalysisSummary
from similarity.similarity_service import SimilarPosition


def serialize_similar_positions(
    similar_positions: list[SimilarPosition],
) -> list[dict[str, object]]:
    return [
        {
            "distance": round(similar.distance, 4),
            "fen": similar.record.fen,
            "move_san": similar.record.move_san,
            "next_moves": similar.record.next_moves,
            "result": similar.record.result,
            "white_elo": similar.record.white_elo,
            "black_elo": similar.record.black_elo,
            "eco": similar.record.eco,
            "opening": similar.record.opening,
        }
        for similar in similar_positions
    ]


def serialize_enriched_move(
    move: EnrichedMoveAnalysis,
    similar_positions: list[SimilarPosition] | None = None,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "engine": move.move_analysis.to_dict(),
        "masters": {
            "position": {
                **move.master_position_stats.to_dict(),
                "master_moves": [
                    master_move.to_dict()
                    for master_move in move.master_position_stats.master_moves
                ],
            },
            "played_move": (
                move.played_master_move.to_dict()
                if move.played_master_move is not None
                else None
            ),
        },
        "online_players": {
            "position": {
                **move.online_position_stats.to_dict(),
                "online_player_moves": [
                    online_move.to_dict()
                    for online_move in move.online_position_stats.online_player_moves
                ],
            },
            "played_move": (
                move.played_online_player_move.to_dict()
                if move.played_online_player_move is not None
                else None
            ),
        },
        "explanation": move.explanation,
    }

    if similar_positions is not None:
        payload["similar_positions"] = serialize_similar_positions(similar_positions)

    return payload


def serialize_analyze_response(
    metadata: dict[str, str],
    moves: list[MoveAnalysis] | list[EnrichedMoveAnalysis] | list[dict[str, object]],
    summary: AnalysisSummary,
) -> dict[str, object]:
    serialized_moves: list[dict[str, object]] = []

    for move in moves:
        if isinstance(move, MoveAnalysis):
            serialized_moves.append(move.to_dict())
            continue

        if isinstance(move, EnrichedMoveAnalysis):
            serialized_moves.append(serialize_enriched_move(move))
            continue

        serialized_moves.append(move)

    return {
        "game": metadata,
        "moves": serialized_moves,
        "summary": summary.to_dict(),
    }
