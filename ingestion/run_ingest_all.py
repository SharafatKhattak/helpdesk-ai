"""
Ingests every document auto-discovered from data/raw/<doc_type>/<filename>.

Usage:
    python -m ingestion.run_ingest_all
"""
from config import DATA_RAW_DIR
from ingestion.documents_config import discover_documents
from ingestion.run_ingest import ingest_document


def main():
    documents = discover_documents()

    if not documents:
        print(f"No documents found under {DATA_RAW_DIR}/<doc_type>/<filename>")
        return

    print(f"Discovered {len(documents)} document(s):\n")
    for doc in documents:
        file_path = DATA_RAW_DIR / doc["folder_name"] / doc["filename"]

        chunks, out_path = ingest_document(
            file_path=file_path,
            doc_id=doc["doc_id"],
            doc_title=doc["doc_title"],
            doc_type=doc["doc_type"],
            language=doc["language"],
        )
        print(f"  [{doc['doc_type']}] {doc['filename']}: {len(chunks)} chunks -> {out_path.name}")


if __name__ == "__main__":
    main()