from pathlib import Path
import re
import fitz
import chromadb
from sentence_transformers import SentenceTransformer

from backend.config import (
    RAW_DOCS_DIR, CHROMA_DIR, COLLECTION_NAME,
    EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP
)

def clean_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def chunk_text(text: str, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    text = clean_text(text)
    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))

        # Prefer a natural boundary near the end of the chunk.
        if end < len(text):
            candidates = [
                text.rfind("\n\n", start, end),
                text.rfind(". ", start, end),
                text.rfind(" ", start, end),
            ]
            boundary = max(candidates)
            if boundary > start + chunk_size // 2:
                end = boundary + 1

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break
        start = max(0, end - overlap)

    return chunks

def extract_chunks_from_pdf(pdf_path: Path):
    doc = fitz.open(pdf_path)
    records = []

    for page_index, page in enumerate(doc):
        page_text = clean_text(page.get_text())
        if not page_text:
            continue

        page_chunks = chunk_text(page_text)

        for chunk_index, chunk in enumerate(page_chunks):
            records.append({
                "text": chunk,
                "metadata": {
                    "document": pdf_path.name,
                    "page": page_index + 1,
                    "chunk": chunk_index + 1,
                    "source_type": "official_document"
                }
            })

    doc.close()
    return records

def ingest():
    pdf_files = sorted(RAW_DOCS_DIR.glob("*.pdf"))

    if not pdf_files:
        raise RuntimeError(
            f"No PDF files found in {RAW_DOCS_DIR}. "
            "Put your authoritative PDFs there first."
        )

    model = SentenceTransformer(EMBEDDING_MODEL)

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    # Rebuild the collection for predictable MVP experiments.
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"description": "Ayurveda/IPR legal source chunks"}
    )

    all_records = []
    for pdf_path in pdf_files:
        print(f"Processing: {pdf_path.name}")
        all_records.extend(extract_chunks_from_pdf(pdf_path))

    texts = [r["text"] for r in all_records]
    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True
    ).tolist()

    ids = [f"chunk-{i:06d}" for i in range(len(all_records))]
    metadatas = [r["metadata"] for r in all_records]

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(f"\nIndexed {len(texts)} chunks.")
    print(f"ChromaDB: {CHROMA_DIR}")
    print(f"Collection: {COLLECTION_NAME}")

if __name__ == "__main__":
    ingest()
