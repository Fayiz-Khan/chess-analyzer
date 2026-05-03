# Chess Analyzer

Chess Analyzer is an end-to-end system for analyzing chess games from raw PGN to actionable insights.

The project builds a full analysis pipeline that:

- Parses and validates chess games
- Reconstructs board states move-by-move
- Evaluates positions using Stockfish
- Detects blunders and inaccuracies
- Compares moves against real-game data
- (Future) Converts handwritten scoresheets into structured PGN

The goal is to combine software engineering, data processing, and machine learning to create a practical analysis tool for competitive players.

---

## Setup

```bash
git clone https://github.com/your-username/chess-analyzer.git
cd chess-analyzer
pip install -r requirements.txt
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
brew install stockfish
python3 main.py