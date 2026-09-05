from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.chat import router as chat_router
from backend.api.classify import router as classify_router

app = FastAPI(
    title="Ayurveda IPR Assistant — Phase 2",
    version="0.2.0",
    description=(
        "Formulation Classifier + IPR Router + Jurisdiction Switch + "
        "Structured RAG Context. Local citation-grounded assistant using Ollama and ChromaDB."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api")
app.include_router(classify_router, prefix="/api")


@app.get("/health")
def health():
    return {"status": "ok", "phase": 2}
