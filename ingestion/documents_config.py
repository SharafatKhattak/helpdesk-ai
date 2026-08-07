"""
Auto-discovers documents from data/raw/<doc_type>/<filename>. The
folder name IS the doc_type value directly — no mapping needed since
folders are already named as clean slugs.
"""
from pathlib import Path
from typing import TypedDict

from config import DATA_RAW_DIR

VALID_DOC_TYPES = {"buyer_policy", "seller_policy", "policy"}


class DocMeta(TypedDict):
    filename: str
    doc_id: str
    doc_title: str
    doc_type: str
    language: str
    folder_name: str


OVERRIDES: dict[str, dict] = {
    "return_policy.md": {"language": "ur-roman"},
    # "some_file.md": {"doc_title": "Custom Title Override"},
}


def _guess_title(filename: str) -> str:
    stem = Path(filename).stem
    return stem.replace("_", " ").replace("-", " ").title()


def discover_documents() -> list[DocMeta]:
    documents: list[DocMeta] = []
    if not DATA_RAW_DIR.exists():
        return documents

    for folder in DATA_RAW_DIR.iterdir():
        if not folder.is_dir():
            continue

        doc_type = folder.name
        if doc_type not in VALID_DOC_TYPES:
            print(f"WARNING — unrecognized folder '{folder.name}' in data/raw/, skipping. "
                  f"Expected one of: {sorted(VALID_DOC_TYPES)}")
            continue

        for file_path in folder.iterdir():
            if not file_path.is_file() or file_path.name.startswith("."):
                continue

            filename = file_path.name
            override = OVERRIDES.get(filename, {})

            documents.append(
                {
                    "filename": filename,
                    "doc_id": f"{doc_type}__{Path(filename).stem}",
                    "doc_title": override.get("doc_title", _guess_title(filename)),
                    "doc_type": doc_type,
                    "language": override.get("language", "en"),
                    "folder_name": folder.name,
                }
            )

    return documents