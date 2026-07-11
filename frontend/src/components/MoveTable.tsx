import { formatEvaluation, type MoveResult } from "../types";

interface MoveTableProps {
  moves: MoveResult[];
  selectedMoveIndex: number;
  onSelectMove: (index: number) => void;
}

function classificationClass(classification: string): string {
  return classification.toLowerCase().replace(/\s+/g, "-");
}

export function MoveTable({ moves, selectedMoveIndex, onSelectMove }: MoveTableProps) {
  return (
    <section className="panel move-panel">
      <div className="panel-heading-row">
        <div>
          <p className="section-label">Move list</p>
          <h2>Critical line</h2>
        </div>
        <span className="muted-text">{moves.length} moves</span>
      </div>

      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>White</th>
              <th>Black</th>
              <th>Eval</th>
              <th>Best</th>
              <th>Class</th>
            </tr>
          </thead>
          <tbody>
            {moves.map((move, index) => {
              const engine = "engine" in move ? move.engine : move;
              const isWhite = engine.move_colour.toLowerCase() === "white";

              return (
                <tr
                  key={`${engine.move_number}-${engine.move_colour}-${index}`}
                  className={index === selectedMoveIndex ? "selected-row" : ""}
                  onClick={() => onSelectMove(index)}
                >
                  <td>{engine.move_number}</td>
                  <td>{isWhite ? engine.move_san : "·"}</td>
                  <td>{!isWhite ? engine.move_san : "·"}</td>
                  <td>{formatEvaluation(engine.eval_after)}</td>
                  <td>{engine.best_move_san}</td>
                  <td>
                    <span className={`classification ${classificationClass(engine.classification)}`}>
                      {engine.classification}
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </section>
  );
}
