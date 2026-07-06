# Chess Analyzer

Chess Analyzer is an end-to-end system for analyzing chess games from raw PGN to actionable insights.

The project builds a complete analysis pipeline that:

- Parses and validates PGN files
- Reconstructs board states move-by-move
- Evaluates positions using Stockfish
- Classifies moves as Best, Good, Inaccuracy, Mistake, or Blunder
- Compares moves against master and online game databases
- Retrieves similar elite positions using handcrafted feature vectors indexed with FAISS
- Generates AI-powered move explanations using engine analysis, human game statistics, and retrieved similar positions

---

# Setup

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

# Local Demo

## 1. Build the similarity index

If you already have `data/positions.jsonl`, build the FAISS index:

```bash
python3 scripts/build_faiss_index.py
```

This creates:

- `data/positions.faiss`
- `data/positions_metadata.jsonl`

---

## 2. Start the backend

```bash
uvicorn api.app:app --reload
```

The backend will be available at:

```
http://127.0.0.1:8000
```

Opening this URL directly will display the API health check.

---

## 3. Start the frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the application at:

```
http://localhost:5173
```

Paste or upload a PGN and analyze the game.

The frontend automatically proxies API requests (such as `/analyze`) to the FastAPI backend running on `http://127.0.0.1:8000`.

---

## Optional analysis features

The API supports enabling additional analysis:

- `include_human_stats`
- `include_similar_positions`
- `include_explanations`

---

# CLI

Run the analyzer from the command line:

```bash
python3 main.py
```

---

# Running Tests

## Backend

```bash
python3 -m pytest
```

## Frontend

```bash
cd frontend
npm test
npm run build
```
