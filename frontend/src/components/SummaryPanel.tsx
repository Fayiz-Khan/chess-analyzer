import type { AnalysisSummary } from "../types";

interface SummaryPanelProps {
  summary: AnalysisSummary;
}

function StatLine({ label, value, tone }: { label: string; value: number | string; tone?: string }) {
  return (
    <div className={`stat-line ${tone ?? ""}`}>
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function PlayerCard({ label, stats }: { label: string; stats: AnalysisSummary["white"] }) {
  return (
    <article className="summary-card">
      <p className="section-label">{label}</p>
      <StatLine label="✓ best" value={stats.best_moves} tone="green" />
      <StatLine label="! good" value={stats.good_moves} />
      <StatLine label="?! inaccuracy" value={stats.inaccuracies} tone="gold" />
      <StatLine label="? mistake" value={stats.mistakes} tone="orange" />
      <StatLine label="?? blunder" value={stats.blunders} tone="red" />
      <div className="summary-footer">
        <span>Avg CPL</span>
        <strong>{stats.average_eval_loss.toFixed(2)}</strong>
      </div>
    </article>
  );
}

export function SummaryPanel({ summary }: SummaryPanelProps) {
  return (
    <section className="summary-panel">
      <PlayerCard label="White" stats={summary.white} />
      <PlayerCard label="Black" stats={summary.black} />
    </section>
  );
}
