"""
Simple query interface for testing the RAG system.

Usage:
    python query.py
"""
from embedding.embedder import embed_query
from retrieval.vector_store import search


def main():
    print("=" * 60)
    print("SoftStore Support Assistant - Query Interface")
    print("=" * 60)
    print("\nType 'quit' to exit\n")

    while True:
        query = input("\nYour question: ").strip()

        if not query:
            continue

        if query.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        # Embed and search
        query_embedding = embed_query(query)
        results = search(query_embedding, top_k=3)

        docs = results["documents"][0]
        metas = results["metadatas"][0]
        distances = results["distances"][0]

        if not docs:
            print("\nNo results found.")
            continue

        print("\n" + "=" * 60)
        print(f"Top {len(docs)} results:")
        print("=" * 60)

        for i, (doc, meta, dist) in enumerate(zip(docs, metas, distances)):
            print(f"\n[Result {i + 1}] (similarity: {1 - dist:.2%})")
            print(f"Source: {meta['doc_title']}")
            if meta.get("section_heading"):
                print(f"Section: {meta['section_heading']}")
            print(f"Type: {meta['doc_type']}")
            print("-" * 60)
            print(doc[:300] + ("..." if len(doc) > 300 else ""))
            print()


if __name__ == "__main__":
    main()
