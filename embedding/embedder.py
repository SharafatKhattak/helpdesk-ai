"""Embedding interface for converting text into vector representations."""

from typing import Iterable, List


class Embedder:
    """Simple placeholder embedder implementation."""

    def __init__(self, model_name: str = "default") -> None:
        self.model_name = model_name

    def embed_texts(self, texts: Iterable[str]) -> List[List[float]]:
        """Return embeddings for the provided texts.

        This stub intentionally raises a clear error until a real embedding
        backend is wired in.
        """
        raise NotImplementedError("Embedding backend is not configured yet.")
