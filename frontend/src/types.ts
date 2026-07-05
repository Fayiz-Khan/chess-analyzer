export interface Evaluation {
  centipawns: number | null;
  mate_in: number | null;
}

export interface EngineMove {
  move_number: number;
  move_colour: string;
  move_san: string;
  best_move_san: string;
  fen_state_before: string;
  fen_state_after: string;
  eval_before: Evaluation;
  eval_after: Evaluation;
  delta: number | null;
  classification: string;
  is_checkmate: boolean;
}

export interface MoveStats {
  san: string;
  average_rating: number;
  white_wins: number;
  black_wins: number;
  draws: number;
  total_games: number;
}

export interface SimilarPosition {
  distance: number;
  fen: string;
  move_san: string;
  next_moves: string[];
  result: string | null;
  white_elo: number | null;
  black_elo: number | null;
  eco: string | null;
  opening: string | null;
}

export interface EnrichedMove {
  engine: EngineMove;
  masters: {
    position: {
      white_wins: number;
      black_wins: number;
      draws: number;
      total_games: number;
      master_moves: MoveStats[];
    };
    played_move: MoveStats | null;
  };
  online_players: {
    position: {
      white_wins: number;
      black_wins: number;
      draws: number;
      total_games: number;
      online_player_moves: MoveStats[];
    };
    played_move: MoveStats | null;
  };
  explanation: string | null;
  similar_positions?: SimilarPosition[];
}

export type MoveResult = EngineMove | EnrichedMove;

export interface PlayerSummary {
  total_moves: number;
  best_moves: number;
  good_moves: number;
  inaccuracies: number;
  mistakes: number;
  blunders: number;
  average_eval_loss: number;
}

export interface AnalysisSummary {
  white: PlayerSummary;
  black: PlayerSummary;
}

export interface AnalyzeResponse {
  game: Record<string, string>;
  moves: MoveResult[];
  summary: AnalysisSummary;
}

export interface AnalyzeOptions {
  includeHumanStats: boolean;
  includeSimilarPositions: boolean;
  includeExplanations: boolean;
}

export function isEnrichedMove(move: MoveResult): move is EnrichedMove {
  return "engine" in move;
}

export function formatEvaluation(evaluation: Evaluation): string {
  if (evaluation.mate_in !== null) {
    return `M${evaluation.mate_in}`;
  }

  if (evaluation.centipawns === null) {
    return "N/A";
  }

  return evaluation.centipawns.toFixed(2);
}
