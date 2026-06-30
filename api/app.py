from fastapi import FastAPI
from pydantic import BaseModel

from analyzer.analyzer import analyze_game
from analyzer.summarizer import build_summary
from analyzer.master_enricher import enrich_move_analysis

app = FastAPI()

class AnalyzeRequest(BaseModel):
    pgn: str
    include_human_stats: bool = False

## to test: uvicorn api.app:app --reload and then http://127.0.0.1:8000/docs
@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/analyze")
def analyze(request: AnalyzeRequest) -> dict[str, object]:
    with open("temp.pgn", "w") as f:
        f.write(request.pgn)

    metadata, analysis = analyze_game("temp.pgn")
    summary = build_summary(analysis)

    if request.include_human_stats:
        moves = [
            enrich_move_analysis(move)
            for move in analysis
        ]
    else:
        moves = analysis

    return {
        "game": metadata,
        "moves": moves,
        "summary": summary,
    }
