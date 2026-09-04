from backend.ingestion.ingest import chunk_text

def test_chunking():
    text = "This is a test sentence. " * 300
    chunks = chunk_text(text, chunk_size=500, overlap=50)

    assert len(chunks) > 1
    assert all(chunk.strip() for chunk in chunks)
