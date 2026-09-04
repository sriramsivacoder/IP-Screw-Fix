from functools import lru_cache
from sentence_transformers import SentenceTransformer
from backend.config import EMBEDDING_MODEL

@lru_cache(maxsize=1)
def get_embedding_model():
    return SentenceTransformer(EMBEDDING_MODEL)

def embed_query(text: str):
    model = get_embedding_model()
    return model.encode(
        [text],
        normalize_embeddings=True
    ).tolist()[0]
