from datetime import date
from typing import Optional

from pydantic import BaseModel


class Chunk(BaseModel):
    chunk_id: str
    doc_id: str
    doc_title: str
    doc_type: str                          # e.g. "buyer_policy", "seller_policy", "faq"
    section_heading: Optional[str] = None
    text: str
    source_url: Optional[str] = None
    version: str = "1.0"
    last_updated: Optional[date] = None
    language: str = "en"                   # "en", "ur", or "ur-roman"
