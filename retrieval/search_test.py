"""Simple search smoke test script."""

from retrieval.index_documents import index_documents
from retrieval.vector_store import VectorStore


def main() -> None:
    store = index_documents(["Sample support document"], VectorStore())
    print(f"Indexed {len(store.documents)} documents")


if __name__ == "__main__":
    main()
