from fastapi.testclient import TestClient
from api.app import app

client = TestClient(app)

def test_health_check_returns_ok(): 
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"
}

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