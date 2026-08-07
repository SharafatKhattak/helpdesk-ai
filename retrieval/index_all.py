"""
Batch-indexes every *_chunks.json file in data/processed/ into Chroma —
run this after run_ingest_all.py has produced the chunk files.

Usage:
    python -m retrieval.index_all
"""
import json

from config import DATA_PROCESSED_DIR
from embedding.embedder import embed_texts
from models.schemas import Chunk
from retrieval.vector_store import add_chunks, delete_by_doc_id


def main():
    chunk_files = sorted(DATA_PROCESSED_DIR.glob("*_chunks.json"))

    if not chunk_files:
        print(f"No *_chunks.json files found in {DATA_PROCESSED_DIR}")
        return

    print(f"Found {len(chunk_files)} chunk file(s) to index:\n")

    for chunks_file in chunk_files:
        raw = json.loads(chunks_file.read_text(encoding="utf-8"))
        chunks = [Chunk(**item) for item in raw]

        if not chunks:
            print(f"  {chunks_file.name}: no chunks, skipping.")
            continue

        doc_id = chunks[0].doc_id
        delete_by_doc_id(doc_id)  # idempotent — replaces old chunks if re-indexing

        embeddings = embed_texts([c.text for c in chunks])
        add_chunks(chunks, embeddings)
        print(f"  {chunks_file.name}: indexed {len(chunks)} chunks (doc_id='{doc_id}').")


if __name__ == "__main__":
    main()