import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import App from "./App";
import { analyzePgn } from "./api";
import type { AnalyzeResponse } from "./types";

vi.mock("react-chessboard", () => ({
  Chessboard: ({ options }: { options?: { position?: string } }) => (
    <div data-testid="chessboard" data-position={options?.position} />
  ),
}));

vi.mock("./api", () => ({
  analyzePgn: vi.fn(),
}));

const analysisResponse: AnalyzeResponse = {
  game: {
    White: "Alice",
    Black: "Bob",
    Result: "1-0",
    Event: "Navigation test",
  },
  moves: [
    {
      move_number: 1,
      move_colour: "White",
      move_san: "e4",
      best_move_san: "e4",
      fen_state_before: "start-fen",
      fen_state_after: "fen-after-e4",
      eval_before: { centipawns: 0, mate_in: null },
      eval_after: { centipawns: 0.2, mate_in: null },
      delta: 0,
      classification: "Best",
      is_checkmate: false,
    },
    {
      move_number: 1,
      move_colour: "Black",
      move_san: "e5",
      best_move_san: "e5",
      fen_state_before: "fen-after-e4",
      fen_state_after: "fen-after-e5",
      eval_before: { centipawns: 0.2, mate_in: null },
      eval_after: { centipawns: 0.1, mate_in: null },
      delta: 0,
      classification: "Good",
      is_checkmate: false,
    },
  ],
  summary: {
    white: {
      total_moves: 1,
      best_moves: 1,
      good_moves: 0,
      inaccuracies: 0,
      mistakes: 0,
      blunders: 0,
      average_eval_loss: 0,
    },
    black: {
      total_moves: 1,
      best_moves: 0,
      good_moves: 1,
      inaccuracies: 0,
      mistakes: 0,
      blunders: 0,
      average_eval_loss: 0,
    },
  },
};

function boardPosition() {
  return screen.getByTestId("chessboard").getAttribute("data-position");
}

describe("App board navigation", () => {
  afterEach(() => {
    vi.clearAllMocks();
  });

  it("updates the rendered board position when navigation controls are clicked", async () => {
    vi.mocked(analyzePgn).mockResolvedValue(analysisResponse);

    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: /analyze game/i }));

    await waitFor(() => {
      expect(boardPosition()).toBe("fen-after-e4");
    });

    fireEvent.click(screen.getByRole("button", { name: /next/i }));
    expect(boardPosition()).toBe("fen-after-e5");

    fireEvent.click(screen.getByRole("button", { name: /prev/i }));
    expect(boardPosition()).toBe("fen-after-e4");

    fireEvent.click(screen.getByRole("button", { name: /next/i }));
    expect(boardPosition()).toBe("fen-after-e5");

    fireEvent.click(screen.getByRole("button", { name: /first/i }));
    expect(boardPosition()).toBe("fen-after-e4");
  });
});
