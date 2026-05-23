from fastapi import FastAPI
from pydantic import BaseModel

from analyzer.analyzer import analyze_game
from analyzer.summarizer import build_summary

app = FastAPI()

class AnalyzeRequest(BaseModel):
    pgn: str

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/analyze")
def analyze(request: AnalyzeRequest): 
    with open("temp.pgn", "w") as f:
        f.write(request.pgn)

    metadata, analysis = analyze_game("temp.pgn")
    summary = build_summary(analysis)

    return {
        "game": metadata,
        "moves": analysis,
        "summary": summary,
    }