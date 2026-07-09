# Architecture

Chess Analyzer is built as a layered full-stack system.

The backend separates HTTP routing, analysis orchestration, engine evaluation, data enrichment, retrieval, and response serialization. This keeps the API thin and makes each layer independently testable.

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
```

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
