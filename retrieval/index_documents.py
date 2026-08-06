"""Indexing utilities for loading documents into the vector store."""

from typing import Iterable, List

from .vector_store import VectorStore


def index_documents(documents: Iterable[str], store: VectorStore | None = None) -> VectorStore:
    """Index a collection of documents into a vector store."""
    vector_store = store or VectorStore()
    vector_store.add_documents(list(documents))
    return vector_store
