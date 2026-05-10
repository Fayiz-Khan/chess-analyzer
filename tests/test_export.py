import json
from export import export_analysis
from models import MoveAnalysis, MoveClassification, MoveColour, PlayerSummary, AnalysisSummary

def test_export_analysis_writes_expected_json_shape(tmp_path):
    output_path = tmp_path / "analysis.json"

    metadata = {
        "Event": "Test Game",
        "White": "Alice",
        "Black": "Bob",
        "Result": "1-0",
    }

    analysis = [
        MoveAnalysis(
            move_number=1,
            move_colour=MoveColour.WHITE,
            move_san="e4",
            best_move_san="e4",
            fen_state_before="before",
            fen_state_after="after",
            eval_before=0.0,
            eval_after=0.3,
            delta=-0.3,
            classification=MoveClassification.BEST,
        )
    ]

    summary = AnalysisSummary(
        white=PlayerSummary(1, 1, 0, 0, 0, 0, 0.0),
        black=PlayerSummary(0, 0, 0, 0, 0, 0, 0.0),
    )

    export_analysis(metadata, analysis, summary, output_path)

    with open(output_path) as f:
        data = json.load(f)

    assert data["game"] == metadata
    assert "moves" in data
    assert "summary" in data
    assert data["moves"][0]["move_colour"] == "White"
    assert data["moves"][0]["classification"] == "Best"
    assert data["summary"]["white"]["best_moves"] == 1