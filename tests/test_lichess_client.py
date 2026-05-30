from unittest.mock import Mock, patch
from api.lichess_client import call_masters_database


@patch("api.lichess_client.requests.get")
def test_call_masters_database_returns_json(mock_get):
    fake_response = Mock()

    fake_response.json.return_value = {
        "moves": [
            {"san": "d5"}
        ]
    }

    mock_get.return_value = fake_response

    result = call_masters_database("some random mocked fen")

    assert result["moves"][0]["san"] == "d5"

@patch("api.lichess_client.requests.get")
def test_call_masters_database_passes_fen_as_query_param(mock_get):
    fake_response = Mock()
    fake_response.json.return_value = {"moves": []}
    mock_get.return_value = fake_response

    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    call_masters_database(fen)

    mock_get.assert_called()

    _, kwargs = mock_get.call_args

    assert kwargs["params"] == {"fen": fen}