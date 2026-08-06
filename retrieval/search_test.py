"""
Manual retrieval check — embed a test query and see what comes back.
This is where you test Roman-Urdu retrieval quality specifically before
trusting it; don't assume it works, verify it.

Usage:
    python -m retrieval.search_test "kya mai ye product lota sakta hu"
    python -m retrieval.search_test "return policy" --doc-type buyer_policy
"""
import argparse

from embedding.embedder import embed_query
from retrieval.vector_store import search


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query", type=str)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--doc-type", type=str, default=None)
    args = parser.parse_args()

    query_embedding = embed_query(args.query)
    results = search(query_embedding, top_k=args.top_k, doc_type_filter=args.doc_type)

    print(f"\nQuery: {args.query}\n")
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    distances = results["distances"][0]

    if not docs:
        print("No results.")
        return

    for i, (doc, meta, dist) in enumerate(zip(docs, metas, distances)):
        print(f"--- Result {i + 1} (distance={dist:.4f}) ---")
        print(f"Source: {meta['doc_title']} > {meta['section_heading'] or 'no heading'}")
        print(doc[:200] + ("..." if len(doc) > 200 else ""))
        print()


if __name__ == "__main__":
    main()