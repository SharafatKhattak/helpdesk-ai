"""
Local Chroma vector store wrapper — runs embedded in-process (no server
to run), persists to disk at CHROMA_DIR.
"""
from typing import List, Optional

import chromadb

from config import CHROMA_COLLECTION_NAME, CHROMA_DIR
from models.schemas import Chunk

_client = None


def get_client():
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return _client


def get_collection():
    return get_client().get_or_create_collection(name=CHROMA_COLLECTION_NAME)


def add_chunks(chunks: List[Chunk], embeddings: List[List[float]]) -> None:
    collection = get_collection()
    collection.add(
        ids=[c.chunk_id for c in chunks],
        embeddings=embeddings,
        documents=[c.text for c in chunks],
        metadatas=[
            {
                "doc_id": c.doc_id,
                "doc_title": c.doc_title,
                "doc_type": c.doc_type,
                "section_heading": c.section_heading or "",
                "source_url": c.source_url or "",
                "version": c.version,
                "language": c.language,
            }
            for c in chunks
        ],
    )


def search(
    query_embedding: List[float],
    top_k: int = 5,
    doc_type_filter: Optional[str] = None,
) -> dict:
    collection = get_collection()
    where = {"doc_type": doc_type_filter} if doc_type_filter else None
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where=where,
    )