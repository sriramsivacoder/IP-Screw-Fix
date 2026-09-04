from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.chat import router as chat_router

app = FastAPI(
    title="Ayurveda IPR Assistant - Phase 1",
    version="0.1.0",
    description="Local citation-grounded RAG MVP using Ollama and ChromaDB."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api")

@app.get("/health")
def health():
    return {"status": "ok"}
