"""Retrieval utilities for searching embedded documents."""

from .index_documents import index_documents
from .vector_store import VectorStore

__all__ = ["VectorStore", "index_documents"]
