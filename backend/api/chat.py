from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.rag.retriever import retrieve
from backend.rag.generator import generate_answer

router = APIRouter()

class ChatRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)

class Source(BaseModel):
    document: str
    page: int | str
    section: str | None = None
    distance: float

class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        results = retrieve(request.question)

        if not results:
            return ChatResponse(
                answer=(
                    "I could not retrieve sufficient evidence from the "
                    "current knowledge base to answer this question reliably."
                ),
                sources=[]
            )

        answer = generate_answer(request.question, results)

        sources = []
        for item in results:
            metadata = item["metadata"]
            sources.append(Source(
                document=str(metadata.get("document", "Unknown")),
                page=metadata.get("page", "Unknown"),
                section=metadata.get("section"),
                distance=item["distance"]
            ))

        return ChatResponse(answer=answer, sources=sources)

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
