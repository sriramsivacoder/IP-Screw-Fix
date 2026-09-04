import chromadb

from backend.config import CHROMA_DIR, COLLECTION_NAME, TOP_K
from backend.rag.embeddings import embed_query

_client = chromadb.PersistentClient(path=str(CHROMA_DIR))

def get_collection():
    try:
        return _client.get_collection(COLLECTION_NAME)
    except Exception as exc:
        raise RuntimeError(
            "RAG collection not found. Run: "
            "python -m backend.ingestion.ingest"
        ) from exc

def retrieve(question: str, top_k: int = TOP_K):
    collection = get_collection()
    query_embedding = embed_query(question)

    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    documents = result.get("documents", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]
    distances = result.get("distances", [[]])[0]

    items = []
    for doc, metadata, distance in zip(documents, metadatas, distances):
        items.append({
            "text": doc,
            "metadata": metadata,
            "distance": float(distance)
        })

    return items
