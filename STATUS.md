# SoftStore Support Assistant - Project Status

**Last Updated:** 2026-08-07

## ✅ What's Working

### 1. Document Ingestion Pipeline
- **Status:** Fully operational
- **What it does:**
  - Auto-discovers documents from `data/raw/{policy|seller_policy|buyer_policy}/`
  - Parses PDF, DOCX, HTML, and Markdown files
  - Performs heading-aware chunking (500 tokens/chunk, 50 token overlap)
  - Saves chunks to `data/processed/*_chunks.json`

**Run it:**
```bash
source venv/Scripts/activate
python -m ingestion.run_ingest_all
```

### 2. Embedding & Vector Store
- **Status:** Fully operational
- **Model:** `paraphrase-multilingual-MiniLM-L12-v2` (supports English + Urdu)
- **Vector DB:** ChromaDB (local, persistent)
- **What it does:**
  - Embeds all chunks from processed JSON files
  - Indexes into ChromaDB with metadata (doc_type, section_heading, language)
  - Supports filtered search by doc_type

**Run it:**
```bash
source venv/Scripts/activate
python -m retrieval.index_all
```

### 3. Retrieval/Search
- **Status:** Fully operational
- **What it does:**
  - Semantic search over indexed documents
  - Returns top-k relevant chunks with metadata
  - Supports filtering by doc_type (buyer_policy, seller_policy, policy)

**Test it:**
```bash
# General query
python -m retrieval.search_test "What is the return policy?"

# Filtered by doc_type
python -m retrieval.search_test "What are commission fees?" --doc-type seller_policy

# Interactive interface
python query.py
```

## 📊 Current Data

**Indexed Documents:** 12 files, 64 total chunks

### Policy (5 files)
- 00_Cross_Verification_Report.pdf (7 chunks)
- 01_Terms_and_Conditions.pdf (4 chunks)
- 02_Privacy_Policy.pdf x3 duplicates (3 chunks each) ⚠️

### Seller Policy (7 files)
- 03_Seller_Terms_and_Conditions.pdf (4 chunks)
- 04_Seller_Policies.pdf x2 duplicates (4 chunks each) ⚠️
- 05_Commission_and_Fee_Schedule.pdf (4 chunks)
- FBA_FEE_SCHEDULE_DRAFT.md (8 chunks)
- FBA_SELLER_GUIDE.md (7 chunks)
- What-You-Can-Sell-on-SoftStore.pdf (13 chunks)

### Buyer Policy (0 files)
- Empty folder

## ⚠️ Known Issues

1. **Duplicate files** - Multiple copies of Privacy Policy and Seller Policies should be deduplicated
2. **Conflicting fee schedules** - Both `05_Commission_and_Fee_Schedule.pdf` and `FBA_FEE_SCHEDULE_DRAFT.md` exist
3. **PDF heading extraction** - PDFs don't preserve heading structure well (flat text)
4. **No buyer-specific policies** - `buyer_policy/` folder is empty

## 🚧 Next Phase: LLM Integration (Gemini API)

**What's needed:**
- [ ] Gemini API key setup
- [ ] RAG prompt engineering (query → retrieval → answer generation)
- [ ] Citation mechanism (show source documents)
- [ ] Multi-turn conversation context
- [ ] Response quality evaluation
- [ ] Query classification (buyer vs seller intent)

## 📁 Project Structure

```
support-assistant/
├── config.py                    # Configuration (paths, model names)
├── models/schemas.py            # Pydantic models (Chunk)
├── ingestion/
│   ├── parsers.py              # Multi-format parsing
│   ├── chunker.py              # Heading-aware chunking
│   ├── documents_config.py     # Auto-discovery
│   └── run_ingest_all.py       # Batch ingestion
├── embedding/
│   └── embedder.py             # Sentence transformer wrapper
├── retrieval/
│   ├── vector_store.py         # ChromaDB interface
│   ├── index_all.py            # Batch indexing
│   └── search_test.py          # CLI search test
├── query.py                     # Interactive query interface
├── data/
│   ├── raw/                    # Source documents
│   │   ├── policy/
│   │   ├── seller_policy/
│   │   └── buyer_policy/
│   ├── processed/              # Generated chunk JSONs
│   └── chroma_db/              # Vector database
└── venv/                       # Python environment
```

## 🎯 Architecture Decisions

1. **Local-first:** ChromaDB runs embedded (no server), embeddings are local
2. **Heading-aware chunking:** Policy clauses stay intact, not fragmented mid-section
3. **Multilingual:** Supports English + Romanized Urdu queries
4. **Metadata-rich:** Every chunk tracks doc_type, section, language for filtering
5. **Idempotent re-indexing:** Re-running ingestion replaces old chunks (no duplicates)

## 🔑 Environment Requirements

**Python:** 3.10+
**Dependencies:** See `requirements.txt`
- pdfplumber, python-docx, beautifulsoup4
- langchain-text-splitters
- sentence-transformers
- chromadb
- pydantic

**Not yet configured:**
- Gemini API key (for next phase)
