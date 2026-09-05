from backend.classifier.rules import (
    determine_category,
    determine_confidence,
    determine_human_review,
)


def classify(answers: dict) -> dict:
    category, reasons = determine_category(answers)
    confidence = determine_confidence(answers, category)
    needs_human_review = determine_human_review(answers, category, confidence)

    return {
        "category": category,
        "confidence": confidence,
        "reason": reasons,
        "needs_human_review": needs_human_review,
    }
