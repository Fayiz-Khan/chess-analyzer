import { describe, expect, it } from "vitest";
import { formatEvaluation, isEnrichedMove } from "./types";

describe("formatEvaluation", () => {
  it("formats centipawn scores", () => {
    expect(formatEvaluation({ centipawns: 1.234, mate_in: null })).toBe("1.23");
  });

  it("formats mate scores", () => {
    expect(formatEvaluation({ centipawns: null, mate_in: -3 })).toBe("M-3");
  });
});

describe("isEnrichedMove", () => {
  it("detects enriched move payloads", () => {
    expect(
      isEnrichedMove({
        engine: {
          move_number: 1,
          move_colour: "White",
          move_san: "e4",
          best_move_san: "e4",
          fen_state_before: "fen",
          fen_state_after: "fen2",
          eval_before: { centipawns: 0, mate_in: null },
          eval_after: { centipawns: 0.2, mate_in: null },
          delta: 0.2,
          classification: "Good",
          is_checkmate: false,
        },
        masters: {
          position: {
            white_wins: 0,
            black_wins: 0,
            draws: 0,
            total_games: 0,
            master_moves: [],
          },
          played_move: null,
        },
        online_players: {
          position: {
            white_wins: 0,
            black_wins: 0,
            draws: 0,
            total_games: 0,
            online_player_moves: [],
          },
          played_move: null,
        },
        explanation: null,
      }),
    ).toBe(true);
  });
});
