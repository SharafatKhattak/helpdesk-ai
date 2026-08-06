from ingestion.chunker import chunk_document


def test_chunk_document_splits_on_headings():
    text = (
        "# Return window\n"
        "You can return within 30 days.\n\n"
        "# Refund method\n"
        "Refunds go back to your original payment method."
    )
    chunks = chunk_document(
        text=text,
        doc_id="test_doc",
        doc_title="Test Policy",
        doc_type="buyer_policy",
    )
    assert len(chunks) == 2
    assert chunks[0].section_heading == "Return window"
    assert chunks[1].section_heading == "Refund method"


def test_chunk_document_handles_no_headings():
    text = "Just a plain paragraph with no heading markers at all."
    chunks = chunk_document(
        text=text,
        doc_id="test_doc2",
        doc_title="Plain doc",
        doc_type="faq",
    )
    assert len(chunks) == 1
    assert chunks[0].section_heading is None
