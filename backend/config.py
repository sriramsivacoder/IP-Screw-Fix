from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DOCS_DIR = DATA_DIR / "raw"
CHROMA_DIR = BASE_DIR / "chroma_db"

COLLECTION_NAME = "ayurveda_legal_docs"

# Change this if you pulled a different Ollama model.
OLLAMA_MODEL = "qwen3:8b"
OLLAMA_URL = "http://localhost:11434/api/chat"

# Local embedding model. The same model must be used for indexing and queries.
EMBEDDING_MODEL = "BAAI/bge-m3"

CHUNK_SIZE = 1800       # characters; simple MVP starting point
CHUNK_OVERLAP = 250
TOP_K = 5
MAX_CONTEXT_CHARS = 12000
