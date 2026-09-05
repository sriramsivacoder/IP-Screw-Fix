from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DOCS_DIR = DATA_DIR / "raw"
CHROMA_DIR = BASE_DIR / "chroma_db"

COLLECTION_NAME = "ayurveda_legal_docs"

OLLAMA_MODEL = "qwen3:8b"
OLLAMA_URL = "http://localhost:11434/api/chat"

EMBEDDING_MODEL = "BAAI/bge-m3"

CHUNK_SIZE = 1800
CHUNK_OVERLAP = 250
TOP_K = 5
MAX_CONTEXT_CHARS = 12000
