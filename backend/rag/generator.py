import requests

from backend.config import OLLAMA_MODEL, OLLAMA_URL, MAX_CONTEXT_CHARS

SYSTEM_PROMPT = """You are an information assistant for Ayurveda-related intellectual-property questions.

You are NOT a lawyer and must not present your response as legal advice.

Answer ONLY from the retrieved legal evidence sections provided below. Do not use your general knowledge to fill missing legal facts.

Rules:
1. Never invent statutes, sections, rules, treaties, cases, dates, or sources.
2. If the evidence is insufficient, explicitly say that the available sources are insufficient to answer reliably.
3. Distinguish what the source says from your explanation.
4. Keep the answer concise and in plain language.
5. Refer to sources using [Source N] markers next to material claims.
6. Do not claim that a product is legally patentable, compliant, or approved unless the supplied evidence actually supports that conclusion.
7. The formulation classification and potential IPR routes provided are application-generated context and are NOT legal authority. Use them only to understand the context of the question.
8. Recommend professional legal review for any specific legal determination."""


def build_evidence_context(results: list) -> tuple[str, int]:
    parts = []
    total_chars = 0

    for i, item in enumerate(results, start=1):
        meta = item["metadata"]

        lines = [f"[Source {i}]"]

        if meta.get("document"):
            lines.append(f"Document: {meta['document']}")
        if meta.get("jurisdiction"):
            lines.append(f"Jurisdiction: {meta['jurisdiction']}")
        if meta.get("authority"):
            lines.append(f"Authority: {meta['authority']}")
        if meta.get("source_type"):
            lines.append(f"Source Type: {meta['source_type']}")
        if meta.get("page"):
            lines.append(f"Page: {meta['page']}")
        if meta.get("section"):
            lines.append(f"Section: {meta['section']}")
        if meta.get("article"):
            lines.append(f"Article: {meta['article']}")
        if meta.get("effective_date"):
            lines.append(f"Effective Date: {meta['effective_date']}")

        lines.append(f"Text:\n{item['text']}")

        block = "\n".join(lines) + "\n"

        if total_chars + len(block) > MAX_CONTEXT_CHARS:
            break

        parts.append(block)
        total_chars += len(block)

    return "\n---\n".join(parts), len(parts)


def build_ipr_summary(ipr_routes: dict | None) -> str:
    if not ipr_routes or not ipr_routes.get("routes"):
        return "No potential IPR routes identified."

    lines = []
    for route in ipr_routes["routes"]:
        ipr_label = route.get("ipr", "").replace("_", " ").title()
        relevance = route.get("relevance", "")
        reason = route.get("reason", "")
        lines.append(f"- {ipr_label} ({relevance}): {reason}")

    return "\n".join(lines)


def generate_answer(
    question: str,
    results: list,
    jurisdiction: str = "India",
    classification: dict | None = None,
    ipr_routes: dict | None = None,
) -> str:
    evidence_context, source_count = build_evidence_context(results)

    classification_text = "Not provided."
    if classification:
        category = classification.get("category", "unknown").replace("_", " ").title()
        confidence = classification.get("confidence", "low").title()
        reasons = " ".join(classification.get("reason", []))
        classification_text = (
            f"Likely category: {category} (Confidence: {confidence}). {reasons}"
        )
        if classification.get("needs_human_review"):
            classification_text += " Human and legal review is recommended."

    ipr_text = build_ipr_summary(ipr_routes)

    user_prompt = f"""USER QUESTION:
{question}

JURISDICTION:
{jurisdiction}

FORMULATION CLASSIFICATION (application-generated context — not legal authority):
{classification_text}

POTENTIAL IPR ROUTES (application-generated context — not legal authority):
{ipr_text}

RETRIEVED LEGAL EVIDENCE ({source_count} source(s)):
{evidence_context}

Instructions:
- Answer using only the retrieved legal evidence above.
- Include [Source N] markers next to material claims.
- Do not cite the classification or IPR routes as legal authority.
- If the evidence does not adequately answer the question, say so explicitly."""

    payload = {
        "model": OLLAMA_MODEL,
        "stream": False,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        "options": {"temperature": 0.1},
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=360)
    response.raise_for_status()

    data = response.json()
    return data["message"]["content"]
