from fastapi.testclient import TestClient
from unittest.mock import patch
from api.app import app

client = TestClient(app)

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

@patch("api.app.enrich_move_analysis")
def test_analyze_includes_human_stats_when_requested(mock_enrich):
    mock_enrich.side_effect = lambda move: {
        "move_analysis": move,
        "master_position_stats": None,
        "played_master_move": None,
        "online_position_stats": None,
        "played_online_player_move": None,
    }

    pgn_data = {
        "pgn": "[Event \"Test\"]\n[White \"Noob\"]\n[Black \"Fayiz\"]\n[Result \"0-1\"]\n\n1. f4 e5 2. g4 Qh4# 0-1",
        "include_human_stats": True,
    }

    response = client.post("/analyze", json=pgn_data)
    data = response.json()

    assert response.status_code == 200
    assert mock_enrich.call_count == len(data["moves"])
    assert "move_analysis" in data["moves"][0]
    