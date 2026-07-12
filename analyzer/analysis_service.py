from analyzer.analyzer import analyze_pgn_text
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
)
from similarity.similarity_service import SimilarPosition, find_similar_positions_from_dataset


def normalize_pgn_text(pgn: str) -> str:
    lines = pgn.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    normalized: list[str] = []
    in_header_block = True
    saw_header = False
    saw_blank_after_header = False

    for line in lines:
        stripped = line.strip()

        if in_header_block:
            if stripped.startswith("["):
                normalized.append(line)
                saw_header = True
                saw_blank_after_header = False
                continue

            if saw_header and not stripped:
                saw_blank_after_header = True
                continue

            if saw_blank_after_header:
                normalized.append("")

            normalized.append(line)
            in_header_block = False
            continue

        normalized.append(line)

    return "\n".join(normalized)


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
    metadata, analysis = analyze_pgn_text(normalize_pgn_text(pgn))

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
