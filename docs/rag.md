# Retrieval-Augmented Generation

Chess Analyzer uses Retrieval-Augmented Generation to produce grounded chess explanations.

The LLM does not explain moves from scratch. It receives a prompt built from multiple evidence sources.

---

## Evidence Sources

For each move, the system can provide:

- Stockfish evaluation before the move
- Stockfish evaluation after the move
- Engine best move
- Evaluation loss
- Move classification
- Lichess Masters statistics
- Lichess Online statistics
- Similar positions from FAISS retrieval

---

## Prompt Flow

```text
MoveAnalysis
   │
   ├── Engine evidence
   ├── Human database evidence
   └── Similar-position evidence
          │
          ▼
Prompt Builder
          │
          ▼
OpenAI Responses API
          │
          ▼
Natural-language explanation
```

---

## Why this is RAG

The generation step is augmented with retrieved context.

Instead of asking the model:

```text
Explain this chess move.
```

the system asks:

```text
Explain this chess move using:
- Stockfish evaluation
- Human move statistics
- Similar positions
```

This makes explanations more grounded and reduces the chance of unsupported reasoning.
