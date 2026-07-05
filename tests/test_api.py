from fastapi.testclient import TestClient
from unittest.mock import patch
from api.app import app
from models.models import (
    EnrichedMoveAnalysis,
    MasterPositionStats,
    OnlinePositionStats,
)

client = TestClient(app)


def make_enriched_move(move):
    return EnrichedMoveAnalysis(
        move_analysis=move,
        master_position_stats=MasterPositionStats(0, 0, 0, []),
        played_master_move=None,
        online_position_stats=OnlinePositionStats(0, 0, 0, []),
        played_online_player_move=None,
    )

def test_health_check_returns_ok(): 
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_analyze_returns_analysis():
    pgn_data = {"pgn": "[Event \"Test\"]\n[White \"Noob\"]\n[Black \"Fayiz\"]\n[Result \"0-1\"]\n\n1. f4 e5 2. g4 Qh4# 0-1"}

    response = client.post("/analyze", json=pgn_data)

    data = response.json()

    assert response.status_code == 200
    assert "game" in data
    assert "moves" in data
    assert "summary" in data

        
def test_analyze_rejects_invalid_request():
    response = client.post("/analyze", json={})

    assert response.status_code == 422

def test_analyze_defaults_to_no_human_stats():
    pgn_data = {
        "pgn": "[Event \"Test\"]\n[White \"Noob\"]\n[Black \"Fayiz\"]\n[Result \"0-1\"]\n\n1. f4 e5 2. g4 Qh4# 0-1"
    }

    response = client.post("/analyze", json=pgn_data)
    data = response.json()

    assert response.status_code == 200
    assert "move_san" in data["moves"][0]
    assert "move_analysis" not in data["moves"][0]

@patch("analyzer.analysis_service.enrich_move_analysis")
def test_analyze_includes_human_stats_when_requested(mock_enrich):
    mock_enrich.side_effect = lambda move: {
        "engine": move.to_dict(),
        "masters": {"position": None, "played_move": None},
        "online_players": {"position": None, "played_move": None},
        "explanation": None,
    }

    pgn_data = {
        "pgn": "[Event \"Test\"]\n[White \"Noob\"]\n[Black \"Fayiz\"]\n[Result \"0-1\"]\n\n1. f4 e5 2. g4 Qh4# 0-1",
        "include_human_stats": True,
    }

    response = client.post("/analyze", json=pgn_data)
    data = response.json()

    assert response.status_code == 200
    assert mock_enrich.call_count == len(data["moves"])
    assert "engine" in data["moves"][0]
    
@patch("analyzer.analysis_service.explain_enriched_move")
@patch("analyzer.analysis_service.enrich_move_analysis")
def test_analyze_includes_explanations_when_requested(mock_enrich, mock_explain):
    mock_enrich.side_effect = lambda move: make_enriched_move(move)
    mock_explain.return_value = "This move is bad because it ignores the center."

    pgn_data = {
        "pgn": "[Event \"Test\"]\n[White \"Noob\"]\n[Black \"Fayiz\"]\n[Result \"0-1\"]\n\n1. f4 e5 2. g4 Qh4# 0-1",
        "include_human_stats": True,
        "include_explanations": True,
    }

    response = client.post("/analyze", json=pgn_data)

    assert response.status_code == 200
    assert mock_explain.called


@patch("analyzer.analysis_service.load_similar_positions")
@patch("analyzer.analysis_service.enrich_move_analysis")
def test_analyze_includes_similar_positions_when_requested(mock_enrich, mock_similar):
    mock_enrich.side_effect = lambda move: make_enriched_move(move)
    mock_similar.return_value = []

    pgn_data = {
        "pgn": "[Event \"Test\"]\n[White \"Noob\"]\n[Black \"Fayiz\"]\n[Result \"0-1\"]\n\n1. f4 e5 2. g4 Qh4# 0-1",
        "include_human_stats": True,
        "include_similar_positions": True,
    }

    response = client.post("/analyze", json=pgn_data)

    assert response.status_code == 200
    assert mock_similar.called