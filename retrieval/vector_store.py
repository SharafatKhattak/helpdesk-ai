"""Vector store abstraction for document retrieval."""

from typing import Any, List


class VectorStore:
    """Placeholder vector store implementation."""

    def __init__(self, collection_name: str = "support-assistant") -> None:
        self.collection_name = collection_name
        self.documents: List[Any] = []

    def add_documents(self, documents: List[Any]) -> None:
        """Store documents in memory until a persistent backend is used."""
        self.documents.extend(documents)

    def search(self, query: str, top_k: int = 5) -> List[Any]:
        """Return the top matching documents for a query."""
        raise NotImplementedError("Search backend is not configured yet.")
