import json
from models.models import AnalysisEncoder, MoveAnalysis, AnalysisSummary

def export_analysis(
    metadata: dict[str, str],
    analysis: list[MoveAnalysis],
    summary: AnalysisSummary,
    output_path: str = "analysis.json",
) -> None:
    output = {
        "game": metadata,
        "moves": analysis,
        "summary": summary,
    }

    with open(output_path, "w") as f:
        json.dump(output, f, indent=4, cls=AnalysisEncoder)