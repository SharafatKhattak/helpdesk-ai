"""
Phase 1 CLI: parse a document, chunk it, and print/save the result for
manual inspection. No embedding or vector DB yet — this step is purely
about verifying the chunks look right before we build on top of them.

Usage:
    python -m ingestion.run_ingest data/raw/return_policy.pdf \
        --doc-id return_policy \
        --doc-title "Return Policy" \
        --doc-type buyer_policy
"""
import argparse
import json
from pathlib import Path

from config import DATA_PROCESSED_DIR
from ingestion.chunker import chunk_document
from ingestion.parsers import parse_document


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", type=Path)
    parser.add_argument("--doc-id", required=True)
    parser.add_argument("--doc-title", required=True)
    parser.add_argument("--doc-type", required=True)
    parser.add_argument("--language", default="en")
    args = parser.parse_args()

    raw_text = parse_document(args.file_path)
    chunks = chunk_document(
        text=raw_text,
        doc_id=args.doc_id,
        doc_title=args.doc_title,
        doc_type=args.doc_type,
        language=args.language,
    )

    print(f"\nParsed {args.file_path.name} -> {len(chunks)} chunks\n")
    for i, chunk in enumerate(chunks):
        preview = chunk.text[:200] + ("..." if len(chunk.text) > 200 else "")
        print(f"--- Chunk {i + 1} [{chunk.section_heading or 'no heading'}] ---")
        print(preview)
        print()

    out_path = DATA_PROCESSED_DIR / f"{args.doc_id}_chunks.json"
    out_path.write_text(
        json.dumps(
            [c.model_dump(mode="json") for c in chunks], indent=2, ensure_ascii=False
        ),
        encoding="utf-8",
    )
    print(f"Saved full chunk data to {out_path}")


if __name__ == "__main__":
    main()
