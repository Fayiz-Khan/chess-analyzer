import os

from dotenv import load_dotenv
from openai import OpenAI

from config import OPENAI_MODEL
from models.models import EnrichedMoveAnalysis
from similarity.similarity_service import SimilarPosition

load_dotenv()


def format_similar_positions(similar_positions: list[SimilarPosition] | None) -> str:
    if not similar_positions:
        return "No similar positions were provided."

    lines = [
        "Retrieved similar examples:",
        "These positions were retrieved because they are structurally similar, not identical. Use them only as supporting evidence.",
    ]

    for index, similar in enumerate(similar_positions, start=1):
        record = similar.record
        lines.append(
            f"""
Example {index}
Opening: {record.opening}
Move played: {record.move_san}
Typical continuation: {", ".join(record.next_moves)}
White Elo: {record.white_elo}
Black Elo: {record.black_elo}
Result: {record.result}
""".strip()
        )

    return "\n\n".join(lines)


def build_explanation_prompt(
    move: EnrichedMoveAnalysis,
    similar_positions: list[SimilarPosition] | None = None,
) -> str:
    engine = move.move_analysis
    similar_position_text = format_similar_positions(similar_positions)

    return f"""
You are a chess coach explaining one move clearly and accurately.

Current move evidence:
Move number: {engine.move_number}
Side to move: {engine.move_colour.value}
Move played: {engine.move_san}
Best engine move for {engine.move_colour.value}: {engine.best_move_san}
Position before the move: {engine.fen_state_before}
Classification: {engine.classification.value}
Eval before: {engine.eval_before}
Eval after: {engine.eval_after}
Eval loss: {engine.delta}

Master database evidence:
{move.played_master_move}

Online database evidence:
{move.played_online_player_move}

Similar-position evidence:
{similar_position_text}

Write 2-4 sentences.

Rules:
1. Explain why the played move was good or bad using the engine evaluation.
2. Explain why the engine preferred the best move for {engine.move_colour.value}.
3. Use master, online, or similar-position evidence only when it supports the explanation.
4. Do not claim the retrieved positions are identical to the current position.
5. If retrieved examples conflict with the engine, prioritize the engine evaluation.
6. Do not invent tactics, plans, or strategic ideas that are not supported by the provided evidence.
7. Treat the best engine move as a legal move for the same side that played the current move. Do not describe it as the opponent's move or as a move that challenges that same side's own center.
""".strip()


def explain_enriched_move(
    move: EnrichedMoveAnalysis,
    similar_positions: list[SimilarPosition] | None = None,
) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.responses.create(
        model=OPENAI_MODEL,
        input=build_explanation_prompt(move, similar_positions),
    )

    return response.output_text
