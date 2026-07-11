import { useMemo, useState } from "react";
import { Chessboard, type ChessboardOptions } from "react-chessboard";
import { analyzePgn } from "./api";
import { MoveTable } from "./components/MoveTable";
import { PgnInput } from "./components/PgnInput";
import { SummaryPanel } from "./components/SummaryPanel";
import {
  formatEvaluation,
  isEnrichedMove,
  type AnalyzeResponse,
  type MoveResult,
} from "./types";
import "./App.css";

const SAMPLE_PGN = `[Event "Demo"]
[White "Alice"]
[Black "Bob"]
[Result "0-1"]

1. f4 e5 2. g4 Qh4# 0-1`;
const STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR";

function getEngineMove(move: MoveResult) {
  return "engine" in move ? move.engine : move;
}

function getEvalValue(move: MoveResult): number {
  const engine = getEngineMove(move);

  if (engine.eval_after?.mate_in !== null && engine.eval_after?.mate_in !== undefined) {
    return engine.eval_after.mate_in > 0 ? 5 : -5;
  }

  return Math.max(-5, Math.min(5, engine.eval_after?.centipawns ?? 0));
}

function getClassificationClass(classification: string): string {
  return classification.toLowerCase().replace(/\s+/g, "-");
}

function EvaluationGraph({
  moves,
  selectedMoveIndex,
  onSelectMove,
}: {
  moves: MoveResult[];
  selectedMoveIndex: number;
  onSelectMove: (index: number) => void;
}) {
  const chart = useMemo(() => {
    const values = moves.length ? [0, ...moves.map(getEvalValue)] : [0, 0.15, -0.2, 0.35, -0.1];
    const width = 720;
    const height = 220;
    const padX = 20;
    const padY = 26;
    const usableW = width - padX * 2;
    const usableH = height - padY * 2;

    const points = values.map((value, index) => {
      const x = padX + (index / Math.max(values.length - 1, 1)) * usableW;
      const y = padY + ((5 - value) / 10) * usableH;
      return { x, y, value };
    });

    const line = points.map((point) => `${point.x},${point.y}`).join(" ");
    const fill = `${padX},${height - padY} ${line} ${width - padX},${height - padY}`;

    return { width, height, points, line, fill, zeroY: padY + usableH / 2 };
  }, [moves]);

  const marker = chart.points[Math.min(selectedMoveIndex + 1, chart.points.length - 1)];

  return (
    <section className="panel graph-panel">
      <div className="panel-heading-row">
        <div>
          <p className="section-label">Engine evaluation</p>
          <h2>Momentum map</h2>
        </div>
        <span className="muted-text">Centipawns · positive = White</span>
      </div>

      <svg viewBox={`0 0 ${chart.width} ${chart.height}`} className="eval-chart" role="img">
        <defs>
          <linearGradient id="evalGoldFill" x1="0" x2="0" y1="0" y2="1">
            <stop offset="0%" stopColor="#d7b24d" stopOpacity="0.42" />
            <stop offset="100%" stopColor="#d7b24d" stopOpacity="0.02" />
          </linearGradient>
        </defs>

        <line x1="20" x2="700" y1={chart.zeroY} y2={chart.zeroY} className="graph-zero" />
        <polygon points={chart.fill} className="graph-fill" />
        <polyline points={chart.line} className="graph-line" />

        {moves.map((_, index) => {
          const point = chart.points[index + 1];

          return (
            <circle
              aria-label={`Select move ${index + 1}`}
              className="chart-hit"
              key={index}
              cx={point.x}
              cy={point.y}
              r="9"
              onClick={() => onSelectMove(index)}
            />
          );
        })}

        {marker ? <circle className="graph-marker" cx={marker.x} cy={marker.y} r="5" /> : null}
      </svg>
    </section>
  );
}

function BoardPanel({
  analysis,
  selectedMove,
  selectedMoveIndex,
  onSelectMove,
}: {
  analysis: AnalyzeResponse | null;
  selectedMove?: MoveResult;
  selectedMoveIndex: number;
  onSelectMove: (index: number) => void;
}) {
  const engine = selectedMove ? getEngineMove(selectedMove) : undefined;
  const boardFen = engine?.fen_state_after || engine?.fen_state_before || STARTING_FEN;
  const chessboardOptions = useMemo<ChessboardOptions>(
    () => ({
      position: boardFen,
      allowDragging: false,
      boardOrientation: "white",
      animationDurationInMs: 300,
      darkSquareStyle: { backgroundColor: "#9b643c" },
      lightSquareStyle: { backgroundColor: "#e2bf86" },
      boardStyle: {
        borderRadius: "4px",
        boxShadow: "none",
      },
    }),
    [boardFen],
  );
  const moveCount = analysis?.moves.length ?? 0;

  return (
    <section className="board-column">
      <div className="player-strip top-player">
        <span className="player-dot black-dot" />
        <div>
          <strong>{analysis?.game.Black ?? "Black"}</strong>
          <span>Black</span>
        </div>
      </div>

      <div className="board-frame">
        <Chessboard options={chessboardOptions} />
      </div>

      <div className="board-controls">
        <button type="button" onClick={() => onSelectMove(0)} disabled={!moveCount || selectedMoveIndex === 0}>
          First
        </button>
        <button
          type="button"
          onClick={() => onSelectMove(Math.max(0, selectedMoveIndex - 1))}
          disabled={!moveCount || selectedMoveIndex === 0}
        >
          Prev
        </button>
        <span>{moveCount ? `${selectedMoveIndex + 1} / ${moveCount}` : "No game"}</span>
        <button
          type="button"
          onClick={() => onSelectMove(Math.min(moveCount - 1, selectedMoveIndex + 1))}
          disabled={!moveCount || selectedMoveIndex >= moveCount - 1}
        >
          Next
        </button>
      </div>

      <div className="player-strip bottom-player">
        <span className="player-dot white-dot" />
        <div>
          <strong>{analysis?.game.White ?? "White"}</strong>
          <span>White</span>
        </div>
      </div>
    </section>
  );
}

function SelectedMovePanel({ selectedMove }: { selectedMove?: MoveResult }) {
  if (!selectedMove) {
    return (
      <section className="panel selected-panel empty-state">
        <p className="section-label">Selected move</p>
        <h2>No move selected</h2>
        <p>Analyze a PGN, then click a move to inspect the position.</p>
      </section>
    );
  }

  const engine = getEngineMove(selectedMove);
  const enriched = isEnrichedMove(selectedMove) ? selectedMove : null;
  const deltaText = engine.delta === null || engine.delta === undefined ? "N/A" : engine.delta.toFixed(2);

  return (
    <section className="panel selected-panel">
      <div className="selected-topline">
        <span className={`classification ${getClassificationClass(engine.classification)}`}>
          {engine.classification}
        </span>
        <span>{formatEvaluation(engine.eval_after)}</span>
      </div>

      <p className="section-label">Selected move</p>
      <h2>
        {engine.move_number}. {engine.move_san}
      </h2>

      <dl className="move-facts">
        <div>
          <dt>Side</dt>
          <dd>{engine.move_colour}</dd>
        </div>
        <div>
          <dt>Best</dt>
          <dd>{engine.best_move_san}</dd>
        </div>
        <div>
          <dt>Before</dt>
          <dd>{formatEvaluation(engine.eval_before)}</dd>
        </div>
        <div>
          <dt>Δ</dt>
          <dd>{deltaText}</dd>
        </div>
      </dl>

      <div className="explanation-card">
        <span>AI explanation</span>
        <p>{enriched?.explanation || "No AI explanation generated for this move."}</p>
      </div>
    </section>
  );
}

function DatabasePanels({ selectedMove }: { selectedMove?: MoveResult }) {
  const enriched = selectedMove && isEnrichedMove(selectedMove) ? selectedMove : null;
  const similarPositions = enriched?.similar_positions ?? [];

  return (
    <section className="data-grid">
      <article className="panel data-card">
        <p className="section-label">Master database</p>
        <strong className="big-number">{enriched?.masters.position.total_games.toLocaleString() ?? "—"}</strong>
        <span>games in this position</span>
        <div className="data-row">
          <span>Played move</span>
          <strong>{enriched?.masters.played_move?.total_games.toLocaleString() ?? "not found"}</strong>
        </div>
      </article>

      <article className="panel data-card">
        <p className="section-label">Online players</p>
        <strong className="big-number">{enriched?.online_players.position.total_games.toLocaleString() ?? "—"}</strong>
        <span>games in this position</span>
        <div className="data-row">
          <span>Played move</span>
          <strong>{enriched?.online_players.played_move?.total_games.toLocaleString() ?? "not found"}</strong>
        </div>
      </article>

      <article className="panel data-card similar-card">
        <p className="section-label">Similar positions</p>
        {similarPositions.length ? (
          <div className="similar-list">
            {similarPositions.slice(0, 5).map((similar, index) => (
              <div className="similar-item" key={`${similar.fen}-${index}`}>
                <div>
                  <strong>{similar.opening || "Related position"}</strong>
                  <span>{similar.next_moves?.length ? similar.next_moves.join(", ") : "No continuation stored"}</span>
                </div>
                <em>{similar.move_san}</em>
              </div>
            ))}
          </div>
        ) : (
          <p>No similar positions loaded for this move.</p>
        )}
      </article>
    </section>
  );
}

function App() {
  const [pgn, setPgn] = useState(SAMPLE_PGN);
  const [includeHumanStats, setIncludeHumanStats] = useState(true);
  const [includeSimilarPositions, setIncludeSimilarPositions] = useState(true);
  const [includeExplanations, setIncludeExplanations] = useState(false);
  const [analysis, setAnalysis] = useState<AnalyzeResponse | null>(null);
  const [selectedMoveIndex, setSelectedMoveIndex] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const selectedMove = analysis?.moves[selectedMoveIndex];

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
      setSelectedMoveIndex(0);
    } catch (caughtError) {
      setAnalysis(null);
      setSelectedMoveIndex(0);
      setError(caughtError instanceof Error ? caughtError.message : "Analysis failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand-lockup">
          <span className="brand-mark">♜</span>
          <div>
            <strong>Chess Analyzer</strong>
            <span>Illuminate the game · Every move tells a story</span>
          </div>
        </div>
        <div className="notation-strip">
          {analysis ? `${analysis.game.White ?? "White"} vs ${analysis.game.Black ?? "Black"}` : "Paste a PGN to begin"}
        </div>
      </header>

      <main className="analysis-layout">
        <aside className="left-rail">
          <BoardPanel
            analysis={analysis}
            selectedMove={selectedMove}
            selectedMoveIndex={selectedMoveIndex}
            onSelectMove={setSelectedMoveIndex}
          />
          {analysis ? <SummaryPanel summary={analysis.summary} /> : null}
        </aside>

        <section className="main-stack">
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
            <>
              <section className="panel game-card">
                <p className="section-label">Game</p>
                <div>
                  <h1>
                    {analysis.game.White ?? "White"} vs {analysis.game.Black ?? "Black"}
                  </h1>
                  <strong>{analysis.game.Result ?? "?"}</strong>
                </div>
                <span>{analysis.game.Event ?? "Unknown event"}</span>
              </section>

              <EvaluationGraph
                moves={analysis.moves}
                selectedMoveIndex={selectedMoveIndex}
                onSelectMove={setSelectedMoveIndex}
              />

              <section className="workbench-grid">
                <MoveTable
                  moves={analysis.moves}
                  selectedMoveIndex={selectedMoveIndex}
                  onSelectMove={setSelectedMoveIndex}
                />
                <SelectedMovePanel selectedMove={selectedMove} />
              </section>

              <DatabasePanels selectedMove={selectedMove} />
            </>
          ) : (
            <section className="panel empty-hero">
              <p className="section-label">Ready</p>
              <h1>Load a PGN to begin analysis.</h1>
              <p>Your backend will classify moves, calculate eval loss, query human games, and surface similar positions.</p>
            </section>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
