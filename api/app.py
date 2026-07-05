from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from analyzer.analysis_service import analyze_pgn_request

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    pgn: str
    include_human_stats: bool = False
    include_explanations: bool = False
    include_similar_positions: bool = False

## to test: uvicorn api.app:app --reload and then http://127.0.0.1:8000/docs
@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/analyze")
def analyze(request: AnalyzeRequest) -> dict[str, object]:
    return analyze_pgn_request(
        pgn=request.pgn,
        include_human_stats=request.include_human_stats,
        include_explanations=request.include_explanations,
        include_similar_positions=request.include_similar_positions,
    )
