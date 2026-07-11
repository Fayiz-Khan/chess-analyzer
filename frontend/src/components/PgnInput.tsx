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
    if (!file) return;

    const reader = new FileReader();
    reader.onload = () => {
      if (typeof reader.result === "string") onPgnChange(reader.result);
    };
    reader.readAsText(file);
  }

  return (
    <section className="panel input-panel">
      <div className="panel-heading-row">
        <div>
          <p className="section-label">PGN input</p>
          <h2>Paste a game or upload notation</h2>
        </div>
        <label className="file-upload">
          Upload PGN
          <input type="file" accept=".pgn,text/plain" onChange={handleFileUpload} />
        </label>
      </div>

      <textarea
        value={pgn}
        onChange={(event) => onPgnChange(event.target.value)}
        rows={9}
        spellCheck={false}
      />

      <div className="input-actions">
        <button type="button" className="primary-button" onClick={onAnalyze} disabled={loading || !pgn.trim()}>
          {loading ? "Analyzing…" : "Analyze game →"}
        </button>

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
              onChange={(event) => onIncludeSimilarPositionsChange(event.target.checked)}
            />
            Similar positions
          </label>
          <label>
            <input
              type="checkbox"
              checked={includeExplanations}
              disabled={!includeHumanStats}
              onChange={(event) => onIncludeExplanationsChange(event.target.checked)}
            />
            AI explanations
          </label>
        </div>
      </div>
    </section>
  );
}
