# ♟️ Chess Analyzer

Chess Analyzer is a full-stack AI-powered chess analysis platform that combines **Stockfish**, **large-scale human game statistics**, **FAISS vector search**, and **Retrieval-Augmented Generation (RAG)** to generate grounded natural-language explanations for chess games.

Rather than simply labeling moves as mistakes or blunders, Chess Analyzer explains **why** a move was good or bad by combining engine analysis, historical human play, and similar elite positions retrieved from a local vector index.

---

## Highlights

- Stockfish-powered engine evaluation
- Move classification: Best, Good, Inaccuracy, Mistake, Blunder
- Lichess Masters and Online Explorer enrichment
- FAISS-based similar-position retrieval
- Retrieval-Augmented Generation (RAG) explanation pipeline
- OpenAI-powered natural-language coaching explanations
- React + TypeScript frontend
- FastAPI backend
- Backend and frontend test coverage

---

## Motivation

Traditional chess engines are extremely strong, but their output is often hard to interpret. A player may see that a move is a blunder, but not understand the reason.

Chess Analyzer bridges that gap by combining multiple sources of chess knowledge:

- **Stockfish** for objective engine evaluation
- **Lichess databases** for practical human move statistics
- **FAISS retrieval** for similar elite-game positions
- **OpenAI** for natural-language explanations

This creates a system that explains chess moves using evidence instead of relying only on raw engine numbers or unguided LLM output.

---

## Features

### Engine Analysis

- Parse complete PGN files
- Reconstruct board states move-by-move
- Evaluate positions with Stockfish
- Compute evaluation loss
- Classify moves automatically
- Generate player summaries

### Human Statistics

- Query the Lichess Masters Explorer
- Query the Lichess Online Explorer
- Compare played moves against historical move frequencies
- Show whether a move appears in master or online games

### Retrieval-Augmented Generation

- Build a local corpus of elite chess positions
- Extract handcrafted feature vectors from FEN positions
- Build a FAISS vector index
- Retrieve top-k similar elite positions
- Use retrieved positions as context for AI explanations

### Frontend

- Paste or upload PGNs
- Toggle human stats, similar positions, and AI explanations
- View move-by-move engine analysis
- View summary statistics for each player
- View enriched move details in a React UI

---

## Technology Stack

### Backend

- Python
- FastAPI
- python-chess
- Stockfish
- Requests
- NumPy
- pytest

### AI and Retrieval

- OpenAI Responses API
- Retrieval-Augmented Generation (RAG)
- FAISS vector search
- Handcrafted chess position feature engineering
- Euclidean nearest-neighbor similarity

### Data Sources

- Lichess Masters Explorer API
- Lichess Online Explorer API
- Lichess Elite Database
- Local JSONL position corpus

### Frontend

- React
- TypeScript
- Vite
- Vitest

---

## System Architecture

```text
                        React Frontend
                               │
                               ▼
                    FastAPI REST API (/analyze)
                               │
                               ▼
                      Analysis Service Layer
                               │
       ┌───────────────────────┼───────────────────────┐
       ▼                       ▼                       ▼
 PGN Parsing              Stockfish              Human Statistics
 python-chess             Evaluation             Lichess APIs
                               │
                               ▼
                       Move Classification
                               │
                               ▼
                    Similar Position Retrieval
                               │
          ┌────────────────────┼────────────────────┐
          ▼                    ▼                    ▼
 Handcrafted Features     FAISS Index        Position Metadata
          │                    │                    │
          └────────────────────┴────────────────────┘
                               │
                               ▼
                    Retrieval-Augmented Prompt
                               │
                               ▼
                      OpenAI Explanation Layer
                               │
                               ▼
                       JSON Response Builder
                               │
                               ▼
                         React Results UI
```

---

## Retrieval Pipeline

Chess Analyzer uses a local retrieval system over elite chess positions.

### Offline Indexing

```text
Lichess Elite PGN
        │
        ▼
Position Dataset Builder
        │
        ▼
positions.jsonl
        │
        ▼
Feature Extraction
        │
        ▼
Handcrafted Position Vectors
        │
        ▼
FAISS Index Builder
        │
        ├────────► positions.faiss
        └────────► positions_metadata.jsonl
```

### Runtime Retrieval

```text
Current Position FEN
        │
        ▼
Feature Extraction
        │
        ▼
Query Vector
        │
        ▼
FAISS Nearest-Neighbor Search
        │
        ▼
Top-K Similar Elite Positions
        │
        ▼
LLM Prompt Context
```

The FAISS index stores numeric vectors. The metadata file maps each vector back to the original chess position, move, opening, continuation, and game information.

---

## Retrieval-Augmented Generation (RAG)

The explanation layer follows a Retrieval-Augmented Generation pipeline.

Instead of asking an LLM to explain a move from scratch, Chess Analyzer builds a grounded prompt using:

- Stockfish evaluation
- Best engine move
- Evaluation loss
- Move classification
- Lichess Masters statistics
- Lichess Online statistics
- Similar elite positions retrieved from FAISS

```text
Engine Evaluation
        │
        ▼
Move Classification
        │
        ▼
Human Database Evidence
        │
        ▼
Similar Elite Position Retrieval
        │
        ▼
Retrieved Chess Context
        │
        ▼
OpenAI Explanation
```

This helps the system produce explanations that are grounded in concrete chess evidence rather than relying only on the language model.

---

## Engineering Highlights

- Designed a layered backend architecture separating API routing, analysis orchestration, retrieval, and explanation services.
- Integrated Stockfish to evaluate every move in a PGN.
- Built automatic move classification based on evaluation loss.
- Added Lichess Masters and Online Explorer enrichment.
- Created a local chess knowledge base from elite games.
- Engineered handcrafted feature vectors for chess positions.
- Replaced brute-force similarity search with a persistent FAISS vector index.
- Added a RAG-style explanation pipeline combining engine output, human statistics, and retrieved similar positions.
- Built a React + TypeScript frontend for interactive PGN analysis.
- Added backend, retrieval, serialization, API, and frontend tests.

---

## Repository Structure

```text
chess-analyzer/
├── analyzer/              # Core analysis, engine orchestration, explanations
├── api/                   # FastAPI application
├── frontend/              # React + TypeScript frontend
├── models/                # Domain models
├── scripts/               # Dataset and FAISS index builders
├── similarity/            # Feature extraction, FAISS index, retrieval logic
├── tests/                 # Backend tests
├── data/                  # Local generated datasets and indexes (ignored)
├── config.py              # Configuration and environment defaults
└── README.md
```

---

## Setup

Clone the repository and install the backend dependencies.

```bash
git clone https://github.com/your-username/chess-analyzer.git
cd chess-analyzer
pip install -r requirements.txt
```

Install Stockfish.

### macOS

```bash
brew install stockfish
```

### Linux

```bash
sudo apt-get update
sudo apt-get install -y stockfish

export ENGINE_PATH=/usr/games/stockfish
```

---

## Environment Variables

Create a `.env` file for optional API credentials and configuration.

```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4.1-mini

MY_SECRET_LICHESS_TOKEN=your_lichess_token

ENGINE_PATH=/opt/homebrew/bin/stockfish
ENGINE_DEPTH=10

SIMILAR_POSITION_COUNT=5
MAX_SIMILARITY_RECORDS=5000
```

---

## Local Demo

### 1. Build the similarity index

If you already have `data/positions.jsonl`, build the FAISS index:

```bash
python3 scripts/build_faiss_index.py
```

This creates:

- `data/positions.faiss`
- `data/positions_metadata.jsonl`

These files are generated locally and should not be committed.

---

### 2. Start the backend

```bash
uvicorn api.app:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

Opening this URL directly will display the API health check.

---

### 3. Start the frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the application at:

```text
http://localhost:5173
```

Paste or upload a PGN and analyze the game.

The frontend automatically proxies API requests such as `/analyze` to the FastAPI backend running on `http://127.0.0.1:8000`.

---

## Optional Analysis Features

The `/analyze` endpoint supports additional flags:

- `include_human_stats`
- `include_similar_positions`
- `include_explanations`

Example request:

```json
{
  "pgn": "[Event \"Demo\"]\n[White \"Alice\"]\n[Black \"Bob\"]\n[Result \"0-1\"]\n\n1. f4 e5 2. g4 Qh4# 0-1",
  "include_human_stats": true,
  "include_similar_positions": true,
  "include_explanations": true
}
```

---

## CLI

Run the analyzer from the command line:

```bash
python3 main.py
```

---

## Running Tests

### Backend

```bash
python3 -m pytest
```

### Frontend

```bash
cd frontend
npm test
npm run build
```

---

## Future Work

- Learned neural chess embeddings
- More expressive board representation for retrieval
- Interactive chessboard visualization
- Saved game history
