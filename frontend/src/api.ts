import type { AnalyzeOptions, AnalyzeResponse } from "./types";

export async function analyzePgn(
  pgn: string,
  options: AnalyzeOptions,
): Promise<AnalyzeResponse> {
  const response = await fetch("/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      pgn,
      include_human_stats: options.includeHumanStats,
      include_similar_positions: options.includeSimilarPositions,
      include_explanations: options.includeExplanations,
    }),
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || "Analysis request failed");
  }

  return response.json();
}
