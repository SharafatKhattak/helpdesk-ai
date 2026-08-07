"""
Gemini API client for generating responses with retrieved context.
"""
from google import genai
from typing import List, Optional

from config import GEMINI_API_KEY, GEMINI_MODEL


def get_client():
    """Get configured Gemini client."""
    if not GEMINI_API_KEY:
        raise ValueError(
            "GEMINI_API_KEY not found. Please set it in .env file or environment."
        )
    return genai.Client(api_key=GEMINI_API_KEY)


def generate_answer(
    query: str,
    context_chunks: List[dict],
    conversation_history: Optional[List[dict]] = None,
) -> dict:
    """
    Generate an answer using Gemini with retrieved context.

    Args:
        query: User's question
        context_chunks: List of retrieved chunks with metadata
        conversation_history: Optional prior turns for multi-turn context

    Returns:
        dict with 'answer', 'sources', and 'model' keys
    """
    client = get_client()

    # Build context section from retrieved chunks
    context_parts = []
    sources = []

    for i, chunk in enumerate(context_chunks, 1):
        doc_title = chunk.get("doc_title", "Unknown")
        section = chunk.get("section_heading", "")
        text = chunk.get("text", "")
        doc_type = chunk.get("doc_type", "")

        context_parts.append(
            f"[Source {i}: {doc_title}" +
            (f" - {section}" if section else "") +
            f"]\n{text}"
        )

        sources.append({
            "source_num": i,
            "doc_title": doc_title,
            "section": section,
            "doc_type": doc_type,
        })

    context_text = "\n\n".join(context_parts)

    # Build prompt
    system_instruction = """You are a helpful customer support assistant for SoftStore, an online marketplace platform.

Your role:
- Answer questions accurately based ONLY on the provided context documents
- Be concise and clear
- If the context doesn't contain enough information, say so honestly
- Cite sources by referring to [Source N] numbers
- Support both English and Romanized Urdu queries
- Distinguish between buyer-facing and seller-facing policies when relevant

Response guidelines:
- Start with a direct answer
- Reference specific sources: "According to [Source 1]..."
- If multiple sources say different things, note the discrepancy
- Don't make up information not in the context
- Keep answers under 150 words unless more detail is explicitly requested"""

    prompt = f"""{system_instruction}

CONTEXT DOCUMENTS:
{context_text}

USER QUESTION: {query}

Provide a helpful answer based on the context above. Cite your sources."""

    # Generate response
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    return {
        "answer": response.text,
        "sources": sources,
        "model": GEMINI_MODEL,
    }
