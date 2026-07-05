# Chess Analyzer

Chess Analyzer is an end-to-end system for analyzing chess games from raw PGN to actionable insights.

The project builds a full analysis pipeline that:

- Parses and validates chess games
- Reconstructs board states move-by-move
- Evaluates positions using Stockfish
- Detects blunders and inaccuracies
- Compares moves against real-game data
- Retrieves similar elite positions with handcrafted vectors indexed by FAISS

---

## Setup

```bash
git clone https://github.com/your-username/chess-analyzer.git
cd chess-analyzer
pip install -r requirements.txt
brew install stockfish
```

On Linux:

```bash
sudo apt-get update && sudo apt-get install -y stockfish
export ENGINE_PATH=/usr/games/stockfish
```

---

## Local Demo

### 1. Build the position index

If you already have `data/positions.jsonl`:

```bash
python3 scripts/build_faiss_index.py
```

### 2. Start the API

```bash
uvicorn api.app:app --reload
```

### 3. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://127.0.0.1:5173`, paste or upload a PGN, and analyze the game.

The frontend proxies `/analyze` to `http://127.0.0.1:8000`.

Optional API flags:

- `include_human_stats`
- `include_similar_positions`
- `include_explanations`

---

## CLI

```bash
python3 main.py
```

---

## Tests

Backend:

```bash
python3 -m pytest
```

Frontend:

```bash
cd frontend
npm test
npm run build
```
