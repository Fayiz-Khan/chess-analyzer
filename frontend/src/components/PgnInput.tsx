interface PgnInputProps {
  pgn: string;
  onPgnChange: (value: string) => void;
  includeHumanStats: boolean;
  onIncludeHumanStatsChange: (value: boolean) => void;
  includeSimilarPositions: boolean;
  onIncludeSimilarPositionsChange: (value: boolean) => void;
  includeExplanations: boolean;
  onIncludeExplanationsChange: (value: boolean) => void;
  onAnalyze: () => void;
  loading: boolean;
}

export function PgnInput({
  pgn,
  onPgnChange,
  includeHumanStats,
  onIncludeHumanStatsChange,
  includeSimilarPositions,
  onIncludeSimilarPositionsChange,
  includeExplanations,
  onIncludeExplanationsChange,
  onAnalyze,
  loading,
}: PgnInputProps) {
  function handleFileUpload(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file) {
      return;
    }

    const reader = new FileReader();
    reader.onload = () => {
      if (typeof reader.result === "string") {
        onPgnChange(reader.result);
      }
    };
    reader.readAsText(file);
  }

  return (
    <section className="panel input-panel">
      <div className="panel-header">
        <h2>PGN Input</h2>
        <label className="file-upload">
          Upload PGN
          <input type="file" accept=".pgn,text/plain" onChange={handleFileUpload} />
        </label>
      </div>

      <textarea
        value={pgn}
        onChange={(event) => onPgnChange(event.target.value)}
        rows={12}
        spellCheck={false}
      />

      <div className="option-row">
        <label>
          <input
            type="checkbox"
            checked={includeHumanStats}
            onChange={(event) => onIncludeHumanStatsChange(event.target.checked)}
          />
          Human stats
        </label>
        <label>
          <input
            type="checkbox"
            checked={includeSimilarPositions}
            disabled={!includeHumanStats}
            onChange={(event) =>
              onIncludeSimilarPositionsChange(event.target.checked)
            }
          />
          Similar positions
        </label>
        <label>
          <input
            type="checkbox"
            checked={includeExplanations}
            disabled={!includeHumanStats}
            onChange={(event) =>
              onIncludeExplanationsChange(event.target.checked)
            }
          />
          AI explanations
        </label>
      </div>

      <button type="button" onClick={onAnalyze} disabled={loading || !pgn.trim()}>
        {loading ? "Analyzing..." : "Analyze Game"}
      </button>
    </section>
  );
}
