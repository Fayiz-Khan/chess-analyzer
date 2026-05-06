from models import MoveEncoder
import json

def export_analysis(metadata, analysis, output_path = "analysis.json"):
    output = {
        "game": metadata,
        "moves": analysis
    }

    with open(output_path, "w") as f:
        json.dump(output, f, indent=4, cls=MoveEncoder)