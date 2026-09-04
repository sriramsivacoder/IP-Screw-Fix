# Ayurveda IPR Assistant — Phase 1

A beginner-friendly local RAG MVP using:

- Python
- FastAPI
- ChromaDB
- Sentence Transformers
- Ollama
- PyMuPDF

## 1. Install

Create a virtual environment and install:

```bash
pip install -r requirements.txt
```

## 2. Start Ollama

Make sure Ollama is running and that your selected model exists:

```bash
ollama list
```

The default configuration uses:

```text
qwen3:8b
```

If you use another model, change `OLLAMA_MODEL` in `backend/config.py`.

## 3. Add PDFs

Put authoritative PDFs in:

```text
data/raw/
```

Do not use random web articles for the legal corpus.

## 4. Build the vector database

From the project root:

```bash
python -m backend.ingestion.ingest
```

This extracts PDF text, chunks it, creates embeddings, and stores the chunks in ChromaDB.

## 5. Start the API

```bash
uvicorn backend.main:app --reload
```

Then open the FastAPI Swagger UI at:

```text
http://127.0.0.1:8000/docs
```

Use:

```text
POST /api/chat
```

Example:

```json
{
  "question": "What does Section 3(p) of the Patents Act address?"
}
```

## 6. Architecture

```text
PDF
 ↓
PyMuPDF
 ↓
Chunks + metadata
 ↓
Embedding model
 ↓
ChromaDB
 ↓
User question
 ↓
Question embedding
 ↓
Similarity retrieval
 ↓
Evidence + question
 ↓
Ollama
 ↓
Answer + sources
```

## Phase 1 limitations

This is an MVP, not a legal-advice system.

It does not yet implement:

- formulation classification
- IPR routing
- India/international jurisdiction toggle
- automated source freshness checking
- claim-level citation verification
- confidence calibration
- human escalation
- multilingual/voice support
- knowledge graph
- agentic workflows

Those belong in later phases.
