from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.classifier.classifier import classify
from backend.classifier.questions import ALL_QUESTIONS
from backend.router.ipr_router import route_ipr

router = APIRouter()


class ClassifyRequest(BaseModel):
    answers: dict


class ClassifyResponse(BaseModel):
    classification: dict
    ipr_routes: dict


@router.post("/classify", response_model=ClassifyResponse)
def classify_route(request: ClassifyRequest):
    try:
        classification = classify(request.answers)
        ipr_routes = route_ipr(request.answers, classification)
        return ClassifyResponse(
            classification=classification,
            ipr_routes=ipr_routes,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/questions")
def get_questions():
    return {"questions": ALL_QUESTIONS}
