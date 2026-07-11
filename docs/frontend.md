# Frontend

The frontend is a React and TypeScript application built with Vite.

It provides the interactive analysis workspace for loading PGNs, choosing optional enrichment features, navigating move positions, and reading the backend analysis response.

---

## Core Responsibilities

- Accept pasted PGN text or uploaded PGN files
- Send analysis requests to the FastAPI backend
- Toggle optional human statistics, similar positions, and AI explanations
- Render a non-draggable chessboard from backend FEN states
- Navigate analyzed moves with First, Previous, Next, move-table rows, and graph points
- Display player summaries, move classifications, engine evaluations, database evidence, similar positions, and generated explanations

---

## Main Frontend Modules

### `src/App.tsx`

Owns the main analysis state, selected move index, board position, evaluation graph, and page layout.

### `src/api.ts`

Wraps the `/analyze` request and maps frontend option names to the backend API contract.

### `src/types.ts`

Defines the TypeScript response types shared by the UI.

### `src/components/PgnInput.tsx`

Handles PGN input, upload, feature toggles, and the analyze action.

### `src/components/MoveTable.tsx`

Displays the analyzed move list and lets users select a move.

### `src/components/SummaryPanel.tsx`

Displays per-player classification counts and average evaluation loss.

---

## Frontend Data Flow

```text
PGN input
   │
   ▼
Analyze button
   │
   ▼
api.ts POST /analyze
   │
   ▼
AnalyzeResponse
   │
   ├── selectedMoveIndex
   │       └── Chessboard position from fen_state_after
   │
   ├── MoveTable selected row
   ├── EvaluationGraph marker
   ├── SelectedMovePanel details
   ├── SummaryPanel player stats
   └── DatabasePanels optional enrichment
```

---

## Testing

Frontend tests use Vitest, jsdom, React Testing Library, and jest-dom.

The regression test in `src/App.test.tsx` verifies that analyzing a game and clicking First, Previous, and Next updates the chessboard position. This covers the main board-navigation workflow.

```bash
cd frontend
npm ci
npm test
npm run build
```
