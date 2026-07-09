# Backend Overview

The backend is a FastAPI application built around a service-oriented analysis pipeline.

---

## Core Responsibilities

- Accept PGN input
- Parse and validate games
- Evaluate positions with Stockfish
- Classify moves
- Enrich analysis with Lichess data
- Retrieve similar positions
- Generate AI explanations
- Return stable JSON responses

---

## Main Backend Modules

### `api/`

FastAPI route definitions.

### `analyzer/`

Core analysis logic, engine orchestration, summaries, explanations, and response serialization.

### `models/`

Dataclasses used to represent analysis results, evaluations, human statistics, and enriched moves.

### `similarity/`

Feature extraction, retrieval logic, FAISS index code, and position records.

### `scripts/`

Offline scripts for building datasets and FAISS indexes.

### `tests/`

Backend test suite covering analysis, models, API behavior, Lichess clients, retrieval, and serialization.

---

## API Contract

The main endpoint is:

```text
POST /analyze
```

Request options:

- `pgn`
- `include_human_stats`
- `include_similar_positions`
- `include_explanations`

The response contains:

- Game metadata
- Move-by-move analysis
- Player summary
- Optional human stats
- Optional similar positions
- Optional AI explanations
