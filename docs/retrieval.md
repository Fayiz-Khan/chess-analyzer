# Retrieval System

The retrieval system powers the similar-position evidence used in the RAG explanation pipeline.

It uses:

- A local corpus of elite chess positions
- Handcrafted chess feature vectors
- FAISS vector search
- Metadata lookup for retrieved positions

---

## Position Dataset

The dataset builder turns elite PGNs into `PositionRecord` objects.

Each record stores:

- FEN before the move
- Move played
- Next moves
- Result
- Player ratings
- ECO code
- Opening name

These records are written to:

```text
data/positions.jsonl
```

Each line is one searchable position.

---

## Feature Extraction

Each FEN is converted into a numeric vector using handcrafted chess features.

Examples include:

- Material balance
- Side to move
- Bishop counts
- Castling rights
- Isolated pawns
- Doubled pawns
- Open files
- Semi-open files

This is not a neural embedding. It is an interpretable handcrafted vector representation.

---

## FAISS Index

The FAISS index stores only numeric vectors.

```text
positions.faiss
```

The metadata file stores the chess information:

```text
positions_metadata.jsonl
```

The order links the two files together:

```text
FAISS vector 0  → metadata line 0
FAISS vector 1  → metadata line 1
FAISS vector 2  → metadata line 2
```

When FAISS returns an index, the app uses that index to recover the original chess record.

---

## Runtime Search

```text
Query FEN
   ↓
Feature Extractor
   ↓
Query Vector
   ↓
FAISS Search
   ↓
Top-K Vector IDs
   ↓
Metadata Lookup
   ↓
SimilarPosition objects
```

The retrieved positions are passed into the explanation prompt as supporting context.

---

## Why FAISS?

The initial implementation used brute-force search:

```text
for every record:
    compute distance
sort all distances
return top k
```

That worked, but it did not scale well.

FAISS moves the nearest-neighbor search into an optimized vector index, allowing the system to search a much larger position corpus efficiently.
