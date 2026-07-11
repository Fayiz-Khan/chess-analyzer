# Architecture

Chess Analyzer is built as a layered full-stack system.

The project separates frontend interaction, HTTP routing, analysis orchestration, engine evaluation, data enrichment, retrieval, explanation generation, and response serialization. This keeps the API thin, makes each layer independently testable, and lets optional features be enabled without changing the core engine-analysis path.

---

## High-Level System

```text
User PGN
   │
   ▼
React Frontend
   │
   ▼
FastAPI /analyze Endpoint
   │
   ▼
Analysis Service
   │
   ├── PGN Parsing
   ├── Stockfish Evaluation
   ├── Move Classification
   ├── Human Statistics Enrichment
   ├── Similar Position Retrieval
   ├── AI Explanation Generation
   └── Response Serialization
   │
   ▼
AnalyzeResponse JSON
   │
   ▼
React Results UI
   ├── Chessboard position
   ├── Move table
   ├── Evaluation graph
   ├── Summary cards
   └── Optional enrichment panels
```

---

## Request Flow

```text
User action
   │
   ▼
PgnInput
   │
   ▼
frontend/src/api.ts
   │  POST /analyze
   ▼
api/app.py
   │
   ▼
analyzer/analysis_service.py
   │
   ├── analyzer/analyzer.py
   │      ├── python-chess PGN replay
   │      └── Stockfish evaluation
   │
   ├── analyzer/summarizer.py
   │
   ├── analyzer/master_enricher.py
   │      └── api/lichess_client.py
   │
   ├── similarity/similarity_service.py
   │      ├── feature_extractor.py
   │      └── faiss_index.py
   │
   ├── analyzer/explanation_service.py
   │      └── OpenAI Responses API
   │
   └── analyzer/response_builder.py
          │
          ▼
React UI state
   ├── selectedMoveIndex
   ├── board FEN
   ├── move details
   └── summaries/enrichment
```

---

## Optional Feature Modes

Core analysis always parses PGN, evaluates positions with Stockfish, classifies moves, and returns summaries.

Optional flags add progressively richer evidence:

```text
include_human_stats
   └── Lichess Masters and Online Explorer data

include_similar_positions
   └── Local JSONL dataset + FAISS index lookup

include_explanations
   └── OpenAI explanation using engine, human, and retrieved context
```

If the local similar-position dataset is missing, the app still runs and returns no similar positions for that move.

---

## Backend Layers

### API Layer

The FastAPI layer receives requests and returns JSON responses.

It does not own chess logic.

### Analysis Service

The analysis service orchestrates the pipeline:

1. Write PGN to a temporary path
2. Run engine analysis
3. Build game summary
4. Optionally enrich with human statistics
5. Optionally retrieve similar positions
6. Optionally generate AI explanations
7. Return a serialized response

### Engine Layer

The engine layer wraps Stockfish and exposes a simple interface for evaluating positions.

### Enrichment Layer

The enrichment layer calls Lichess Explorer APIs and maps returned data into domain models.

### Retrieval Layer

The retrieval layer converts FEN positions into handcrafted vectors and searches a FAISS index for nearest neighbors.

### Explanation Layer

The explanation layer builds a grounded prompt and calls the OpenAI Responses API.

### Response Builder

The response builder converts Python domain objects into frontend-friendly JSON.

### Frontend Layer

The React frontend owns UI state, request options, selected move navigation, and presentation.

It renders board positions from `fen_state_after`, lets users navigate moves through controls, table rows, or graph points, and displays optional enrichment only when the backend response includes it.

---

## Verification

The project includes both backend and frontend verification:

- Backend pytest coverage for engine analysis, API behavior, models, response serialization, summarization, Lichess clients, retrieval, and FAISS index behavior.
- Frontend Vitest coverage for type helpers and board-navigation interaction.
- CI installs Stockfish, runs backend tests, installs frontend dependencies with `npm ci`, runs frontend tests, and builds the Vite app.

---

## Why this architecture?

The project intentionally avoids putting all logic inside the FastAPI route.

Instead:

```text
api/app.py
   ↓
analysis_service.py
   ↓
domain services
```

This makes the code easier to test, extend, and debug.

For example, the retrieval implementation can move from handcrafted vectors to neural embeddings without changing the API contract.
