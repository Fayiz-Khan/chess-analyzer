from analyzer.analyzer import analyze_game
from analyzer.summarizer import build_summary
from analyzer.master_enricher import enrich_move_analysis
from analyzer.explanation_service import explain_enriched_move
from config import POSITION_DATASET_PATH, TEMP_PGN_PATH
from similarity.similarity_service import find_similar_positions_from_dataset

from config import (
    MAX_SIMILARITY_RECORDS,
    POSITION_DATASET_PATH,
    SIMILAR_POSITION_COUNT,
    TEMP_PGN_PATH,
)

def analyze_pgn_request(
    pgn: str,
    include_human_stats: bool = False,
    include_explanations: bool = False,
    include_similar_positions: bool = False,
) -> dict[str, object]:
    TEMP_PGN_PATH.write_text(pgn, encoding="utf-8")

    metadata, analysis = analyze_game(str(TEMP_PGN_PATH))
    summary = build_summary(analysis)

    if not include_human_stats:
        return {
            "game": metadata,
            "moves": analysis,
            "summary": summary,
        }

    moves = [enrich_move_analysis(move) for move in analysis]

    if include_explanations:
        for move in moves:
            similar_positions = []

            if include_similar_positions and POSITION_DATASET_PATH.exists():
                similar_positions = find_similar_positions_from_dataset(
                    query_fen=move.move_analysis.fen_state_before,
                    dataset_path=POSITION_DATASET_PATH,
                    k=SIMILAR_POSITION_COUNT,
                    max_records=MAX_SIMILARITY_RECORDS,
                )

            move.explanation = explain_enriched_move(
                move,
                similar_positions=similar_positions,
            )

    return {
        "game": metadata,
        "moves": moves,
        "summary": summary,
    }
