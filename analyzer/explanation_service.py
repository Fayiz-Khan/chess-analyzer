from dotenv import load_dotenv
from openai import OpenAI
from models.models import EnrichedMoveAnalysis
import os

load_dotenv()

def build_explanation_prompt(move: EnrichedMoveAnalysis) -> str:
    engine = move.move_analysis

    return f"""
You are a chess coach explaining one move clearly.

Move played: {engine.move_san}
Best engine move: {engine.best_move_san}
Classification: {engine.classification}
Eval before: {engine.eval_before}
Eval after: {engine.eval_after}
Eval loss: {engine.delta}

Master database played move:
{move.played_master_move}

Online database played move:
{move.played_online_player_move}

Explain in 2-4 sentences:
1. why the played move was good or bad
2. why the engine preferred the best move
3. use human database evidence if available
Do not hallucinate specific plans if the data does not support it.
"""


def explain_enriched_move(move: EnrichedMoveAnalysis) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = build_explanation_prompt(move)

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )

    return response.output_text
