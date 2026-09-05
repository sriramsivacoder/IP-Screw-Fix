from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.rag.retriever import retrieve
from backend.rag.generator import generate_answer

router = APIRouter()


class ChatRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)
    jurisdiction: str = "India"
    classification: dict | None = None
    ipr_routes: dict | None = None


class Source(BaseModel):
    document: str
    page: int | str
    section: str | None = None
    article: str | None = None
    authority: str | None = None
    jurisdiction: str | None = None
    effective_date: str | None = None
    source_url: str | None = None
    distance: float


class ChatResponse(BaseModel):
    answer: str
    jurisdiction: str
    classification: dict | None = None
    ipr_routes: dict | None = None
    sources: list[Source]
    confidence: str | None = None
    needs_human_review: bool | None = None


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        results = retrieve(request.question, jurisdiction=request.jurisdiction)

        if not results:
            return ChatResponse(
                answer=(
                    "I could not retrieve sufficient evidence from the current knowledge base "
                    f"({request.jurisdiction} jurisdiction) to answer this question reliably. "
                    "Please ensure that relevant authoritative documents have been added to "
                    "data/raw/ and ingested using: python -m backend.ingestion.ingest"
                ),
                jurisdiction=request.jurisdiction,
                classification=request.classification,
                ipr_routes=request.ipr_routes,
                sources=[],
                confidence=request.classification.get("confidence") if request.classification else None,
                needs_human_review=True,
            )

        answer = generate_answer(
            question=request.question,
            results=results,
            jurisdiction=request.jurisdiction,
            classification=request.classification,
            ipr_routes=request.ipr_routes,
        )

        sources = []
        for item in results:
            meta = item["metadata"]
            sources.append(Source(
                document=str(meta.get("document", "Unknown")),
                page=meta.get("page", "Unknown"),
                section=meta.get("section") or None,
                article=meta.get("article") or None,
                authority=meta.get("authority") or None,
                jurisdiction=meta.get("jurisdiction") or None,
                effective_date=meta.get("effective_date") or None,
                source_url=meta.get("source_url") or None,
                distance=item["distance"],
            ))

        return ChatResponse(
            answer=answer,
            jurisdiction=request.jurisdiction,
            classification=request.classification,
            ipr_routes=request.ipr_routes,
            sources=sources,
            confidence=request.classification.get("confidence") if request.classification else None,
            needs_human_review=(
                request.classification.get("needs_human_review")
                if request.classification else None
            ),
        )

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
