"""
Ingests every document auto-discovered from data/raw/<doc_type>/<filename>.

Usage:
    python -m ingestion.run_ingest_all
"""
import json

from config import DATA_RAW_DIR, DATA_PROCESSED_DIR
from ingestion.chunker import chunk_document
from ingestion.documents_config import discover_documents
from ingestion.parsers import parse_document


def main():
    documents = discover_documents()

    if not documents:
        print(f"No documents found under {DATA_RAW_DIR}/<doc_type>/<filename>")
        return

    print(f"Discovered {len(documents)} document(s):\n")
    for doc in documents:
        file_path = DATA_RAW_DIR / doc["folder_name"] / doc["filename"]

        print(f"Processing [{doc['doc_type']}] {doc['filename']}...")

        # Parse the document
        raw_text = parse_document(file_path)

        # Chunk it
        chunks = chunk_document(
            text=raw_text,
            doc_id=doc["doc_id"],
            doc_title=doc["doc_title"],
            doc_type=doc["doc_type"],
            language=doc["language"],
        )

        # Save chunks to JSON
        out_path = DATA_PROCESSED_DIR / f"{doc['doc_id']}_chunks.json"
        out_path.write_text(
            json.dumps(
                [c.model_dump(mode="json") for c in chunks], indent=2, ensure_ascii=False
            ),
            encoding="utf-8",
        )

        print(f"  OK: {len(chunks)} chunks -> {out_path.name}\n")


if __name__ == "__main__":
    main()