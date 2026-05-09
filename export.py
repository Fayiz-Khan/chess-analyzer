from models import AnalysisEncoder
import json

def export_analysis(metadata, analysis, summary, output_path = "analysis.json"):
    output = {
        "game": metadata,
        "moves": analysis,
        "summary": summary,
    }

    with open(output_path, "w") as f:
        json.dump(output, f, indent=4, cls=AnalysisEncoder)