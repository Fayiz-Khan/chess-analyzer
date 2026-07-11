# ♟️ Chess Analyzer

Chess Analyzer is a full-stack AI-powered chess analysis platform that combines **Stockfish**, **human game statistics**, **FAISS vector search**, and **Retrieval-Augmented Generation (RAG)** to generate grounded natural-language explanations for chess games.

Rather than simply labeling moves as mistakes or blunders, Chess Analyzer explains **why** a move was good or bad by combining engine analysis, historical human play, and similar positions retrieved from a local vector index.

<img width="2940" height="1600" alt="image" src="https://github.com/user-attachments/assets/c01776cf-e306-4ded-884c-356d47c8eb67" />


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
- **FAISS retrieval** over a local corpus built from a downloaded Lichess Elite PGN
- **OpenAI** for natural-language explanations

This creates a system that explains chess moves using evidence instead of relying only on raw engine numbers or unguided LLM output.

---

## Features

### Engine Analysis

- Parse complete PGN games
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

- Build a local corpus of chess positions from a downloaded Lichess Elite PGN
- Extract handcrafted feature vectors from FEN positions
- Build a FAISS vector index
- Retrieve top-k similar positions
- Use retrieved positions as context for AI explanations

### Frontend

- Paste or upload PGNs
- Toggle human stats, similar positions, and AI explanations
- Navigate the analyzed game on an interactive chessboard
- Click move-table rows or evaluation graph points to inspect positions
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
- Downloaded Lichess Elite PGN corpus (local, ignored)
- Local JSONL position corpus

### Frontend

- React
- TypeScript
- Vite
- react-chessboard
- React Testing Library
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

Chess Analyzer uses a local retrieval system over positions extracted from PGN games.

### Offline Indexing

```text
Downloaded Lichess Elite PGN
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
- Similar positions retrieved from FAISS

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
                    Similar Position Retrieval
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
- Created a local chess knowledge base from a downloaded Lichess Elite PGN.
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
├── docs/                  # Architecture, backend, frontend, retrieval, and RAG docs
├── data/                  # Local generated datasets and indexes (ignored)
├── config.py              # Configuration and environment defaults
└── README.md
```

Additional documentation:

- `docs/architecture.md`
- `docs/backend.md`
- `docs/frontend.md`
- `docs/retrieval.md`
- `docs/rag.md`

---

## Setup

Clone the repository and install the backend dependencies. Python 3.12 is recommended because CI runs on Python 3.12.

```bash
git clone git@github.com:Fayiz-Khan/chess-analyzer.git
cd chess-analyzer
python3 -m venv .venv
source .venv/bin/activate
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

Copy `.env.example` to `.env` and adjust paths or optional API credentials for your machine.

```bash
cp .env.example .env
```

`ENGINE_PATH` must point to your Stockfish binary. `OPENAI_API_KEY` is only required when AI explanations are enabled. `MY_SECRET_LICHESS_TOKEN` is optional for Lichess Explorer requests.

### API keys and tokens

Core engine analysis only requires Stockfish. These credentials unlock optional enrichment features:

- **OpenAI API key**: create a key from the OpenAI platform API keys page: `https://platform.openai.com/api-keys`. Put it in `.env` as `OPENAI_API_KEY`. This is only needed when `include_explanations` is enabled.
- **Lichess token**: create one from your Lichess account preferences under API access tokens: `https://lichess.org/account/oauth/token`. Put it in `.env` as `MY_SECRET_LICHESS_TOKEN`. The app uses Explorer endpoints, so a token is optional; if you create one, avoid account-control scopes that this app does not need.

---

## Local Demo

### 1. Optional: Build the similarity index

Similar-position retrieval is optional. If `data/positions.jsonl` is missing, the app still runs and returns an empty similar-position list.

This project uses a locally downloaded Lichess Elite PGN as the retrieval source. The Lichess Elite Database is available at `https://database.nikonoel.fr/`; it provides monthly downloadable PGN archives built from filtered lichess.org games. The raw PGN and generated index files are ignored because they are large, so they are not included in the repository.

To rebuild the retrieval index from scratch:

1. Download a monthly PGN archive from `https://database.nikonoel.fr/`, or provide another compatible PGN file.
2. Extract the downloaded archive.
3. Place or rename the extracted PGN at `data/elite/lichess_elite_2021-12.pgn`, or update the command below to use your local filename.
4. Build the JSONL position dataset:

```bash
python3 scripts/build_position_dataset.py data/elite/lichess_elite_2021-12.pgn --output data/positions.jsonl
```

5. Build the FAISS index:

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
npm ci
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
npm ci
npm test
npm run build
```

---

## Future Work

- Learned neural chess embeddings
- More expressive board representation for retrieval
- Saved game history
- Move annotations directly on the chessboard
