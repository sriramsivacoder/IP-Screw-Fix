import requests

from backend.config import (
    OLLAMA_MODEL, OLLAMA_URL, MAX_CONTEXT_CHARS
)

SYSTEM_PROMPT = """You are an information assistant for Ayurveda-related
intellectual-property questions.

You are NOT a lawyer and must not present your response as legal advice.

Answer ONLY from the supplied evidence. Do not use your general knowledge
to fill missing legal facts.

Rules:
1. Never invent statutes, sections, rules, treaties, cases, dates, or sources.
2. If the evidence is insufficient, explicitly say that the available sources
   are insufficient to answer reliably.
3. Distinguish what the source says from your explanation.
4. Keep the answer concise and plain-language.
5. Refer to sources using [Source N] markers.
6. Do not claim that a product is legally patentable, compliant, or approved
   unless the supplied evidence actually supports that conclusion.
"""

def build_context(results):
    parts = []
    total = 0

    for i, item in enumerate(results, start=1):
        meta = item["metadata"]
        block = (
            f"[Source {i}]\n"
            f"Document: {meta.get('document', 'Unknown')}\n"
            f"Page: {meta.get('page', 'Unknown')}\n"
            f"Section: {meta.get('section', 'Not identified')}\n"
            f"Text:\n{item['text']}\n"
        )

        if total + len(block) > MAX_CONTEXT_CHARS:
            break

        parts.append(block)
        total += len(block)

    return "\n---\n".join(parts)

def generate_answer(question: str, results):
    context = build_context(results)

    user_prompt = f"""Question:
{question}

Evidence:
{context}

Answer using only the evidence above.
Include [Source N] markers next to material claims.
If the evidence does not adequately answer the question, say so."""

    payload = {
        "model": OLLAMA_MODEL,
        "stream": False,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        "options": {
            "temperature": 0.1
        }
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=180
    )
    response.raise_for_status()

    data = response.json()
    return data["message"]["content"]
