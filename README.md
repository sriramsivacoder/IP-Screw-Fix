# Ayurveda IPR Assistant — Phase 2

A beginner-friendly, locally-run Retrieval-Augmented Generation (RAG) assistant for Ayurveda intellectual property research. Built for the **Smart India Hackathon**.

> **Legal Disclaimer**
> This system provides information based on its curated legal source corpus only. It is **not a substitute for professional legal advice**. The formulation classification and potential IPR routes produced by this system are application-generated and do not constitute legal or regulatory determinations. The authoritative documents in the knowledge base are the only evidence used for answers. Consult a qualified legal professional for any specific legal guidance.

---

## Overview

The assistant helps users understand potential intellectual property routes relevant to Ayurvedic formulations. It does this by:

1. Collecting formulation details through a step-by-step questionnaire
2. Classifying the formulation into a likely regulatory category using rule-based logic
3. Identifying potentially relevant IPR routes (patent, trademark, GI, traditional knowledge, etc.)
4. Filtering retrieved legal documents by jurisdiction (India or International)
5. Generating grounded answers using Ollama, citing only retrieved authoritative documents

---

## Phase 1 — MVP RAG

Phase 1 established the core RAG pipeline:

- PDF legal documents → PyMuPDF extraction → text chunking → sentence embeddings → ChromaDB
- User question → embedding → vector similarity retrieval → Ollama generation
- FastAPI backend with a single `POST /api/chat` endpoint
- Minimal frontend scaffold

---

## Phase 2 — Classifier + IPR Router + Jurisdiction Switch

Phase 2 adds:

- **Formulation Classifier**: rule-based classification of formulations into categories
- **Clarifying Questionnaire**: six-step, conditional question flow
- **IPR Router**: maps answers to potentially relevant intellectual property routes with reasons
- **Jurisdiction Switch**: India / International toggle that filters ChromaDB retrieval
- **Structured RAG Context**: the Ollama prompt is clearly structured into separate sections
- **Expanded Metadata**: documents carry jurisdiction, authority, section, article, effective date, source URL
- **Sidecar Metadata**: optional `.metadata.json` files alongside PDFs for enriched metadata
- **Professional Frontend**: React + Vite + Tailwind CSS v4 + Framer Motion with AYUSH color system

---

## Architecture

```
User Answers (Questionnaire)
        ↓
Formulation Classifier (rule-based)
        ↓
IPR Router
        ↓
Jurisdiction Selector (India / International)
        ↓
Jurisdiction-filtered ChromaDB Retrieval
        ↓
Structured Ollama Prompt (question + classification + IPR routes + evidence)
        ↓
Grounded Answer + Sources + Classification + IPR Routes
```

The classifier and IPR router produce **application context**, not legal evidence. The RAG answer is grounded only in retrieved authoritative documents.

---

## Formulation Classifier

The classifier is entirely rule-based. No LLM is used for classification.

**Input**: answers to six questions  
**Output**: category, confidence (high/medium/low), reasons, needs_human_review flag

**Categories**:

| Category | Description |
|---|---|
| `classical_medicine` | Based on an authoritative classical Ayurvedic text, not substantially modified |
| `proprietary_or_modified_medicine` | Based on classical sources but substantially modified |
| `new_or_non_classical_medicine` | Not based on classical Ayurvedic sources |
| `food_nutraceutical` | Intended as food or nutraceutical |
| `cosmetic` | Intended as cosmetic |
| `unknown` | Insufficient information to classify |

`not_sure` is preserved throughout and propagates to lower confidence and human review flags.

---

## IPR Router

Eight potentially relevant routes are assessed:

| Route | When Identified |
|---|---|
| Patent | New or novel manufacturing process; substantially modified formulation |
| Trademark | Always potentially relevant for brand names and product identifiers |
| Design | Always potentially relevant for visual appearance and packaging |
| Copyright | Always potentially relevant for labels, artwork, documentation |
| Trade Secret | Always potentially relevant for confidential formulation know-how |
| Geographical Indication | Geographical association or regional reputation reported |
| Plant Variety Protection | Formulation involves a medicine or new plant variety |
| Traditional Knowledge / Prior Art | Formulation is intended as medicine |

Routes are labelled **Potentially Relevant** or **Unclear**. They are not legal conclusions.

---

## Jurisdiction Switch

- Default: **India**
- Options: **India** / **International**
- The selected jurisdiction is applied as a ChromaDB metadata filter
- India and International documents are **never mixed** in a single retrieval context
- The selected jurisdiction is included in the API response and displayed in the UI

---

## RAG Workflow

```
User question
    ↓
Embed question (BAAI/bge-m3)
    ↓
ChromaDB filtered query (jurisdiction = selected)
    ↓
Top-K retrieved chunks
    ↓
Structured Ollama prompt:
    - USER QUESTION
    - JURISDICTION
    - FORMULATION CLASSIFICATION (application context, not legal authority)
    - POTENTIAL IPR ROUTES (application context, not legal authority)
    - RETRIEVED LEGAL EVIDENCE (cited sources)
    ↓
Grounded answer with [Source N] markers
```

If no evidence is retrieved, the system says so explicitly rather than guessing.

---

## Document Metadata

Each indexed chunk carries:

```json
{
  "document": "patents_act_1970.pdf",
  "jurisdiction": "India",
  "authority": "IP India",
  "source_type": "statute",
  "page": 8,
  "chunk": 2,
  "section": "Section 3(p)",
  "article": "",
  "effective_date": "2024-08-01",
  "source_url": "https://ipindia.gov.in/"
}
```

If a field is not known, it defaults to an empty string. No metadata is invented.

---

## Sidecar Metadata Files

Place a `.metadata.json` file alongside each PDF in `data/raw/` to provide enriched metadata.

**Example**:

```
data/raw/
  patents_act_1970.pdf
  patents_act_1970.metadata.json
```

**Example metadata file**:

```json
{
  "jurisdiction": "India",
  "authority": "IP India",
  "source_type": "statute",
  "section": "",
  "article": "",
  "effective_date": "2024-08-01",
  "source_url": "https://ipindia.gov.in/"
}
```

If no sidecar file exists, the document defaults to `jurisdiction: India` and `source_type: official_document`.

**Important**: The metadata in sidecar files must be manually verified against the authoritative source. The system does not validate or verify metadata.

---

## Folder Structure

```
ayurveda-ipr/
├── backend/
│   ├── main.py                  FastAPI application
│   ├── config.py                Paths, model config, settings
│   ├── api/
│   │   ├── chat.py              POST /api/chat
│   │   └── classify.py         POST /api/classify, GET /api/questions
│   ├── classifier/
│   │   ├── questions.py         Questionnaire definition
│   │   ├── rules.py             Rule-based classification logic
│   │   └── classifier.py       Orchestrates classification
│   ├── router/
│   │   └── ipr_router.py       IPR route identification
│   ├── ingestion/
│   │   └── ingest.py           PDF → chunks → embeddings → ChromaDB
│   └── rag/
│       ├── embeddings.py        Sentence transformer model
│       ├── retriever.py         ChromaDB retrieval with jurisdiction filter
│       └── generator.py        Structured Ollama context and generation
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── StepIndicator.jsx
│   │   │   ├── JurisdictionSwitch.jsx
│   │   │   ├── ClassificationCard.jsx
│   │   │   ├── IprRoutes.jsx
│   │   │   ├── SourceList.jsx
│   │   │   └── Disclaimer.jsx
│   │   ├── pages/
│   │   │   ├── FormulationPage.jsx
│   │   │   ├── ClassifyResultPage.jsx
│   │   │   └── ChatPage.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── data/
│   └── raw/                     Place authoritative PDFs here
├── tests/
│   └── test_chunking.py         Phase 1 chunking tests
├── chroma_db/                   ChromaDB persistent storage (gitignored)
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Installation

### 1. Clone and set up Python environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 2. Set up frontend

```bash
cd frontend
npm install
cd ..
```

---

## Ollama Setup

Install Ollama from https://ollama.com and pull the model:

```bash
ollama pull qwen3:8b
```

To use a different model, change `OLLAMA_MODEL` in `backend/config.py`.

Verify it is running:

```bash
ollama list
```

---

## Embedding Model

The default embedding model is `BAAI/bge-m3` loaded via Sentence Transformers. It downloads automatically on first use.

The same embedding model must be used for both ingestion and retrieval. Do not change `EMBEDDING_MODEL` in `backend/config.py` after ingesting documents without re-ingesting.

---

## ChromaDB

ChromaDB stores the indexed document chunks in `chroma_db/` at the project root. This directory is gitignored and must be rebuilt locally from the PDFs.

---

## Adding and Updating PDFs

1. Obtain authoritative PDF documents (Acts, Rules, Treaties, Guidelines).
2. Place them in `data/raw/`.
3. Optionally create a `.metadata.json` sidecar file for each PDF (see Sidecar Metadata section).
4. Re-run ingestion (see below).

**Recommended documents for India jurisdiction:**

- Patents Act, 1970 (as amended)
- Trade Marks Act, 1999
- Geographical Indications of Goods Act, 1999
- Biological Diversity Act, 2002
- Protection of Plant Varieties and Farmers Rights Act, 2001
- Drugs and Cosmetics Act, 1940
- AYUSH Ministry guidelines on Ayurvedic proprietary medicines

**Recommended documents for International jurisdiction:**

- TRIPS Agreement (WTO)
- Convention on Biological Diversity (CBD)
- Nagoya Protocol
- WIPO Traditional Knowledge documentation guidelines

Do not use unofficial summaries or blogs as the legal corpus.

---

## Running Ingestion

From the project root:

```bash
python -m backend.ingestion.ingest
```

This rebuilds the ChromaDB collection from all PDFs in `data/raw/`. Run this after adding or updating any documents.

---

## Running the Backend

```bash
uvicorn backend.main:app --reload
```

API will be available at `http://localhost:8000`.

Swagger UI: `http://localhost:8000/docs`

---

## Running the Frontend

```bash
cd frontend
npm run dev
```

Frontend will be available at `http://localhost:5173`.

---

## API Endpoints

### GET /health

Returns `{"status": "ok", "phase": 2}`.

### GET /api/questions

Returns the complete questionnaire definition.

### POST /api/classify

**Request:**
```json
{
  "answers": {
    "intended_use": "medicine",
    "classical_source": "yes",
    "substantially_modified": "no",
    "new_process": "not_sure",
    "geographical_association": "no",
    "biological_resources_from_india": "yes"
  }
}
```

**Response:**
```json
{
  "classification": {
    "category": "classical_medicine",
    "confidence": "medium",
    "reason": ["..."],
    "needs_human_review": true
  },
  "ipr_routes": {
    "routes": [
      {
        "ipr": "patent",
        "relevance": "unclear",
        "reason": "..."
      }
    ],
    "needs_human_review": true
  }
}
```

### POST /api/chat

**Request:**
```json
{
  "question": "What does Section 3(p) of the Patents Act say about traditional knowledge?",
  "jurisdiction": "India",
  "classification": { ... },
  "ipr_routes": { ... }
}
```

**Response:**
```json
{
  "answer": "...",
  "jurisdiction": "India",
  "classification": { ... },
  "ipr_routes": { ... },
  "sources": [
    {
      "document": "patents_act_1970.pdf",
      "page": 8,
      "section": "Section 3(p)",
      "authority": "IP India",
      "jurisdiction": "India",
      "effective_date": "2024-08-01",
      "source_url": "...",
      "distance": 0.18
    }
  ],
  "confidence": "medium",
  "needs_human_review": true
}
```

---

## Example Workflow

1. Open the frontend at `http://localhost:5173`
2. Answer the six formulation questions (e.g., Medicine → Classical source → No modification)
3. Review the likely classification (e.g., Classical Medicine, High Confidence)
4. Review potentially relevant IPR routes and their reasons
5. Select jurisdiction: India or International
6. Ask a question: "Is a classical Ayurvedic medicine eligible for patent protection under Indian law?"
7. Read the grounded answer with source citations

---

## Limitations

- The knowledge base is only as current as the documents you have added to `data/raw/`
- The system cannot access live legal databases or the internet
- Classification is based on answers to six questions and may not capture all regulatory nuances
- The assistant provides information only — it is not a legal advice system
- Answers are generated by a local Ollama model and may contain errors
- Source-grounding does not guarantee legal accuracy
- The system does not verify the authenticity or currency of ingested documents

---

## Future Phase 3

Potential additions for Phase 3:

- Multilingual support (Hindi and regional languages via Bhashini)
- Voice input and output
- Automatic metadata extraction from PDF structure
- Per-section chunking using table of contents
- Citation-level verification
- Legal knowledge graph
- Document freshness tracking and alerts
- AYUSH portal integration
- Confidence calibration from retrieval distances
- Claim-level source tracing
