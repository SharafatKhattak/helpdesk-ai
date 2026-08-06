"""
Heading-aware chunking, per the architecture doc:

1. Split primarily on '#'-prefixed headings (section boundaries) — a
   short policy clause stays as one chunk instead of being fragmented.
2. Any section still too long gets recursively sub-split with overlap.
"""
import re
import uuid
from typing import List, Optional

from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import CHUNK_OVERLAP_TOKENS, MAX_CHUNK_TOKENS
from models.schemas import Chunk

HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.*)$", re.MULTILINE)

# Rough chars-per-token approximation for mixed English/Urdu content.
# Good enough for a sizing heuristic — not a real tokenizer.
CHARS_PER_TOKEN = 4


def split_by_headings(text: str) -> List[dict]:
    """Splits text into (heading, body) sections based on '#' markers.
    Content before the first heading gets heading=None."""
    matches = list(HEADING_PATTERN.finditer(text))
    if not matches:
        return [{"heading": None, "body": text.strip()}]

    sections = []
    if matches[0].start() > 0:
        sections.append({"heading": None, "body": text[: matches[0].start()].strip()})

    for i, match in enumerate(matches):
        heading = match.group(2).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        sections.append({"heading": heading, "body": body})

    return [s for s in sections if s["body"]]


def chunk_document(
    text: str,
    doc_id: str,
    doc_title: str,
    doc_type: str,
    source_url: Optional[str] = None,
    language: str = "en",
) -> List[Chunk]:
    sections = split_by_headings(text)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=MAX_CHUNK_TOKENS * CHARS_PER_TOKEN,
        chunk_overlap=CHUNK_OVERLAP_TOKENS * CHARS_PER_TOKEN,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks: List[Chunk] = []
    for section in sections:
        body = section["body"]
        heading = section["heading"]

        if len(body) <= MAX_CHUNK_TOKENS * CHARS_PER_TOKEN:
            sub_texts = [body]
        else:
            sub_texts = splitter.split_text(body)

        for sub_text in sub_texts:
            chunks.append(
                Chunk(
                    chunk_id=str(uuid.uuid4()),
                    doc_id=doc_id,
                    doc_title=doc_title,
                    doc_type=doc_type,
                    section_heading=heading,
                    text=sub_text.strip(),
                    source_url=source_url,
                    language=language,
                )
            )

    return chunks
