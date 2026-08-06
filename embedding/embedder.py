"""
Wraps the local multilingual embedding model. This exact model must be
used for BOTH indexing (this phase) and query-time retrieval (Phase 3) —
mixing embedding models produces incompatible vector spaces and silently
broken search. Don't swap EMBEDDING_MODEL_NAME later without re-indexing
every document from scratch.
"""
from typing import List

from sentence_transformers import SentenceTransformer

from config import EMBEDDING_MODEL_NAME

_model = None  # lazy-loaded singleton so we don't reload the model on every call


def get_embedder() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    return _model


def embed_texts(texts: List[str]) -> List[List[float]]:
    model = get_embedder()
    embeddings = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
    return embeddings.tolist()


def embed_query(query: str) -> List[float]:
    return embed_texts([query])[0]