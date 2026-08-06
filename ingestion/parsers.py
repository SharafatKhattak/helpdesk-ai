"""
Parsers: raw source file -> plain text, with heading structure preserved
as '#'-style markers so the chunker (chunker.py) can split on them.
"""
from pathlib import Path

import pdfplumber
from bs4 import BeautifulSoup
from docx import Document


def parse_pdf(path: Path) -> str:
    text_parts = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    return "\n\n".join(text_parts)


def parse_docx(path: Path) -> str:
    doc = Document(path)
    lines = []
    for para in doc.paragraphs:
        if not para.text.strip():
            continue
        if para.style.name.startswith("Heading"):
            level = para.style.name.replace("Heading ", "")
            prefix = "#" * int(level) if level.isdigit() else "#"
            lines.append(f"{prefix} {para.text.strip()}")
        else:
            lines.append(para.text.strip())
    return "\n\n".join(lines)


def parse_html(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    # Strip boilerplate — adjust selectors to match your actual source site
    for tag in soup(["nav", "header", "footer", "script", "style"]):
        tag.decompose()

    lines = []
    for el in soup.find_all(["h1", "h2", "h3", "p", "li"]):
        text = el.get_text(strip=True)
        if not text:
            continue
        if el.name in ("h1", "h2", "h3"):
            level = int(el.name[1])
            lines.append(f"{'#' * level} {text}")
        else:
            lines.append(text)
    return "\n\n".join(lines)


def parse_markdown(path: Path) -> str:
    return path.read_text(encoding="utf-8")


PARSERS = {
    ".pdf": parse_pdf,
    ".docx": parse_docx,
    ".html": parse_html,
    ".htm": parse_html,
    ".md": parse_markdown,
    ".markdown": parse_markdown,
}


def parse_document(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix not in PARSERS:
        raise ValueError(
            f"No parser registered for file type: {suffix} "
            f"(supported: {', '.join(PARSERS)})"
        )
    return PARSERS[suffix](path)
