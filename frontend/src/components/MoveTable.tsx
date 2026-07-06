import {
  formatEvaluation,
  isEnrichedMove,
  type MoveResult,
} from "../types";

interface MoveTableProps {
  moves: MoveResult[];
}

function classificationClass(classification: string): string {
  return classification.toLowerCase().replace(/\s+/g, "-");
}

export function MoveTable({ moves }: MoveTableProps) {
  return (
    <section className="panel move-panel">
      <h2>Moves</h2>
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>Side</th>
              <th>Move</th>
              <th>Best</th>
              <th>Eval Before</th>
              <th>Eval After</th>
              <th>Delta</th>
              <th>Class</th>
            </tr>
          </thead>
          <tbody>
            {moves.map((move, index) => {
              const engine = isEnrichedMove(move) ? move.engine : move;

              return (
                <tr key={`${engine.move_number}-${engine.move_colour}-${index}`}>
                  <td>{engine.move_number}</td>
                  <td>{engine.move_colour}</td>
                  <td>{engine.move_san}</td>
                  <td>{engine.best_move_san}</td>
                  <td>{formatEvaluation(engine.eval_before)}</td>
                  <td>{formatEvaluation(engine.eval_after)}</td>
                  <td>{engine.delta?.toFixed(2) ?? "N/A"}</td>
                  <td>
                    <span
                      className={`classification ${classificationClass(engine.classification)}`}
                    >
                      {engine.classification}
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {moves.map((move, index) =>
        isEnrichedMove(move) ? (
          <article className="move-detail" key={`detail-${index}`}>
            <h3>
              Move {move.engine.move_number} · {move.engine.move_san}
            </h3>

            {move.explanation ? <p className="explanation">{move.explanation}</p> : null}

            <div className="detail-grid">
              <div>
                <h4>Master Database</h4>
                <p>{move.masters.position.total_games} games in position</p>
                {move.masters.played_move ? (
                  <p>
                    Played move seen in {move.masters.played_move.total_games} master
                    games
                  </p>
                ) : (
                  <p>Played move not found in master database</p>
                )}
              </div>

              <div>
                <h4>Online Players</h4>
                <p>{move.online_players.position.total_games} games in position</p>
                {move.online_players.played_move ? (
                  <p>
                    Played move seen in{" "}
                    {move.online_players.played_move.total_games} online games
                  </p>
                ) : (
                  <p>Played move not found in online database</p>
                )}
              </div>
            </div>

            {move.similar_positions && move.similar_positions.length > 0 ? (
              <div className="similar-positions">
                <h4>Similar Positions</h4>
                <ul>
                  {move.similar_positions.map((similar, similarIndex) => (
                    <li key={`${similar.fen}-${similarIndex}`}>
                      <strong>{similar.move_san}</strong>
                      {similar.opening ? ` · ${similar.opening}` : ""}
                      {similar.next_moves.length > 0
                        ? ` · continues ${similar.next_moves.join(", ")}`
                        : ""}
                    </li>
                  ))}
                </ul>
              </div>
            ) : null}
          </article>
        ) : null,
      )}
    </section>
  );
}
