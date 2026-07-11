from analyzer.analyzer import analyze_game
from analyzer.response_builder import serialize_analyze_response, serialize_enriched_move
from analyzer.summarizer import build_summary
from analyzer.master_enricher import enrich_move_analysis
from analyzer.explanation_service import explain_enriched_move
from config import (
    FAISS_INDEX_PATH,
    FAISS_METADATA_PATH,
    MAX_SIMILARITY_RECORDS,
    POSITION_DATASET_PATH,
    SIMILAR_POSITION_COUNT,
    TEMP_PGN_PATH,
)
from similarity.similarity_service import SimilarPosition, find_similar_positions_from_dataset


def load_similar_positions(query_fen: str) -> list[SimilarPosition]:
    if not POSITION_DATASET_PATH.exists():
        return []

    return find_similar_positions_from_dataset(
        query_fen=query_fen,
        dataset_path=POSITION_DATASET_PATH,
        k=SIMILAR_POSITION_COUNT,
        max_records=MAX_SIMILARITY_RECORDS,
        index_path=FAISS_INDEX_PATH,
        metadata_path=FAISS_METADATA_PATH,
    )


def analyze_pgn_request(
    pgn: str,
    include_human_stats: bool = False,
    include_explanations: bool = False,
    include_similar_positions: bool = False,
) -> dict[str, object]:
    TEMP_PGN_PATH.write_text(pgn, encoding="utf-8")

    metadata, analysis = analyze_game(str(TEMP_PGN_PATH))

    if not analysis:
        raise ValueError("PGN must contain at least one move.")

    summary = build_summary(analysis)

    if not include_human_stats:
        return serialize_analyze_response(metadata, analysis, summary)

    enriched_moves = []

    for move in analysis:
        enriched = enrich_move_analysis(move)

        if isinstance(enriched, dict):
            enriched_moves.append(enriched)
            continue

        similar_positions: list[SimilarPosition] = []

        if include_similar_positions:
            similar_positions = load_similar_positions(enriched.move_analysis.fen_state_before)

        if include_explanations:
            enriched.explanation = explain_enriched_move(
                enriched,
                similar_positions=similar_positions,
            )

        enriched_moves.append(
            serialize_enriched_move(
                enriched,
                similar_positions=similar_positions if include_similar_positions else None,
            )
        )

    return serialize_analyze_response(metadata, enriched_moves, summary)
