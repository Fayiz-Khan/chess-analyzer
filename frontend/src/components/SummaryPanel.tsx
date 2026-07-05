import type { AnalysisSummary } from "../types";

interface SummaryPanelProps {
  summary: AnalysisSummary;
}

function PlayerCard({
  label,
  stats,
}: {
  label: string;
  stats: AnalysisSummary["white"];
}) {
  return (
    <article className="summary-card">
      <h3>{label}</h3>
      <dl>
        <div>
          <dt>Moves</dt>
          <dd>{stats.total_moves}</dd>
        </div>
        <div>
          <dt>Best</dt>
          <dd>{stats.best_moves}</dd>
        </div>
        <div>
          <dt>Good</dt>
          <dd>{stats.good_moves}</dd>
        </div>
        <div>
          <dt>Inaccuracies</dt>
          <dd>{stats.inaccuracies}</dd>
        </div>
        <div>
          <dt>Mistakes</dt>
          <dd>{stats.mistakes}</dd>
        </div>
        <div>
          <dt>Blunders</dt>
          <dd>{stats.blunders}</dd>
        </div>
        <div>
          <dt>Avg eval loss</dt>
          <dd>{stats.average_eval_loss.toFixed(2)}</dd>
        </div>
      </dl>
    </article>
  );
}

export function SummaryPanel({ summary }: SummaryPanelProps) {
  return (
    <section className="panel summary-panel">
      <h2>Summary</h2>
      <div className="summary-grid">
        <PlayerCard label="White" stats={summary.white} />
        <PlayerCard label="Black" stats={summary.black} />
      </div>
    </section>
  );
}
