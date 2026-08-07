"""
Loads a chunk JSON file produced by Phase 1's run_ingest.py, embeds each
chunk locally, and indexes it into the local Chroma store.

Usage:
    python -m retrieval.index_documents data/processed/return_policy_chunks.json
"""
import argparse
import json
from pathlib import Path

from embedding.embedder import embed_texts
from models.schemas import Chunk
from retrieval.vector_store import add_chunks, delete_by_doc_id


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("chunks_file", type=Path)
    args = parser.parse_args()

    raw = json.loads(args.chunks_file.read_text(encoding="utf-8"))
    chunks = [Chunk(**item) for item in raw]

    print(f"Embedding {len(chunks)} chunks from {args.chunks_file.name}...")
    embeddings = embed_texts([c.text for c in chunks])

    add_chunks(chunks, embeddings)
    print(f"Indexed {len(chunks)} chunks into Chroma collection '{args.chunks_file.stem}'.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("chunks_file", type=Path)
    args = parser.parse_args()

    raw = json.loads(args.chunks_file.read_text(encoding="utf-8"))
    chunks = [Chunk(**item) for item in raw]

    if not chunks:
        print("No chunks found in file — nothing to index.")
        return

    doc_id = chunks[0].doc_id

    # Idempotent re-indexing: clear any existing chunks for this doc_id
    # first, so re-running on an updated document replaces old chunks
    # instead of piling up duplicates.
    delete_by_doc_id(doc_id)

    print(f"Embedding {len(chunks)} chunks from {args.chunks_file.name} (doc_id={doc_id})...")
    embeddings = embed_texts([c.text for c in chunks])

    add_chunks(chunks, embeddings)
    print(f"Indexed {len(chunks)} chunks for doc_id='{doc_id}'.")