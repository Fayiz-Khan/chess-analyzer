import { useState } from "react";
import { analyzePgn } from "./api";
import { MoveTable } from "./components/MoveTable";
import { PgnInput } from "./components/PgnInput";
import { SummaryPanel } from "./components/SummaryPanel";
import type { AnalyzeResponse } from "./types";
import "./App.css";

const SAMPLE_PGN = `[Event "Demo"]
[White "Alice"]
[Black "Bob"]
[Result "0-1"]

1. f4 e5 2. g4 Qh4# 0-1`;

function App() {
  const [pgn, setPgn] = useState(SAMPLE_PGN);
  const [includeHumanStats, setIncludeHumanStats] = useState(true);
  const [includeSimilarPositions, setIncludeSimilarPositions] = useState(true);
  const [includeExplanations, setIncludeExplanations] = useState(false);
  const [analysis, setAnalysis] = useState<AnalyzeResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleAnalyze() {
    setLoading(true);
    setError(null);

    try {
      const result = await analyzePgn(pgn, {
        includeHumanStats,
        includeSimilarPositions,
        includeExplanations,
      });
      setAnalysis(result);
    } catch (caughtError) {
      setAnalysis(null);
      setError(
        caughtError instanceof Error ? caughtError.message : "Analysis failed",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <div>
          <h1>Chess Analyzer</h1>
          <p>Paste or upload a PGN to analyze moves, evaluations, and human stats.</p>
        </div>
      </header>

      <main className="app-main">
        <PgnInput
          pgn={pgn}
          onPgnChange={setPgn}
          includeHumanStats={includeHumanStats}
          onIncludeHumanStatsChange={setIncludeHumanStats}
          includeSimilarPositions={includeSimilarPositions}
          onIncludeSimilarPositionsChange={setIncludeSimilarPositions}
          includeExplanations={includeExplanations}
          onIncludeExplanationsChange={setIncludeExplanations}
          onAnalyze={handleAnalyze}
          loading={loading}
        />

        {error ? <div className="error-banner">{error}</div> : null}

        {analysis ? (
          <section className="results">
            <div className="game-meta">
              <h2>
                {analysis.game.White ?? "White"} vs {analysis.game.Black ?? "Black"}
              </h2>
              <p>
                {analysis.game.Event ?? "Unknown event"} · Result{" "}
                {analysis.game.Result ?? "?"}
              </p>
            </div>

            <SummaryPanel summary={analysis.summary} />

            <MoveTable moves={analysis.moves} />
          </section>
        ) : null}
      </main>
    </div>
  );
}

export default App;
