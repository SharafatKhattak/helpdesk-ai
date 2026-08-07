"""
Interactive RAG chatbot with Gemini LLM.

Usage:
    python chatbot.py
"""
from embedding.embedder import embed_query
from llm.gemini_client import generate_answer
from retrieval.vector_store import search


def format_sources(sources):
    """Format source citations for display."""
    if not sources:
        return ""

    lines = ["\nSources:"]
    for src in sources:
        section = f" > {src['section']}" if src['section'] else ""
        lines.append(f"  [{src['source_num']}] {src['doc_title']}{section}")
    return "\n".join(lines)


def main():
    print("=" * 70)
    print("SoftStore AI Support Assistant (Gemini-powered RAG)")
    print("=" * 70)
    print("\nI can help you with:")
    print("  - Seller policies and commission fees")
    print("  - Platform terms and conditions")
    print("  - Product listing guidelines")
    print("  - FBA (Fulfilled by SoftStore) information")
    print("\nType 'quit' to exit, 'help' for options\n")

    conversation_history = []

    while True:
        query = input("\nYou: ").strip()

        if not query:
            continue

        if query.lower() in ("quit", "exit", "q"):
            print("\nThank you for using SoftStore Support! Goodbye!")
            break

        if query.lower() == "help":
            print("\nCommands:")
            print("  quit/exit/q - Exit the chatbot")
            print("  help - Show this message")
            print("  clear - Clear conversation history")
            continue

        if query.lower() == "clear":
            conversation_history.clear()
            print("\nConversation history cleared")
            continue

        # Retrieve relevant chunks
        print("\nSearching knowledge base...", end="", flush=True)
        query_embedding = embed_query(query)
        results = search(query_embedding, top_k=5)

        # Prepare context chunks
        context_chunks = []
        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]

        for doc, meta in zip(docs, metas):
            context_chunks.append({
                "text": doc,
                "doc_title": meta.get("doc_title", ""),
                "section_heading": meta.get("section_heading", ""),
                "doc_type": meta.get("doc_type", ""),
            })

        # Generate answer with Gemini
        print("\rGenerating response...    ", end="", flush=True)
        try:
            result = generate_answer(
                query=query,
                context_chunks=context_chunks,
                conversation_history=conversation_history,
            )

            answer = result["answer"]
            sources = result["sources"]

            # Display answer
            print(f"\rAssistant: {answer}")

            # Display sources
            print(format_sources(sources))

            # Track conversation
            conversation_history.append({"role": "user", "content": query})
            conversation_history.append({"role": "assistant", "content": answer})

            # Keep only last 6 turns (3 exchanges) for context window management
            if len(conversation_history) > 6:
                conversation_history = conversation_history[-6:]

        except Exception as e:
            print(f"\rError: {str(e)}")
            print("Please try rephrasing your question or check your API key.")


if __name__ == "__main__":
    main()
