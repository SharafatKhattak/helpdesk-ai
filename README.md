# SoftStore AI Support Assistant

Enterprise-grade RAG-based customer support system for SoftStore marketplace. Provides semantic search over policy documents with support for English and Romanized Urdu queries.

## 🚀 Quick Start

### 1. Activate Virtual Environment
```bash
source venv/Scripts/activate  # Windows Git Bash
# OR
venv\Scripts\activate.bat     # Windows CMD
```

### 2. **Fix API Key First! (IMPORTANT)**

Check your API key:
```bash
python check_api_key.py
```

If invalid, get a valid key from https://aistudio.google.com/apikey and update `.env`

### 3. Start the GUI Chatbot (Qt Interface)
```bash
python gui_chatbot.py
```

**Features:**
- Modern GUI with chat bubbles
- Real-time source citations panel  
- Non-blocking queries (threaded)
- Built-in API key validation

**Example queries:**
- "What are the seller commission fees?"
- "What products can I sell on SoftStore?"
- "How does FBA work?"
- "What are the return policies?"

### 3. Or Run Individual Pipeline Steps

**Step 1: Ingest documents** (parse + chunk)
```bash
python -m ingestion.run_ingest_all
```

**Step 2: Index into vector database** (embed + store)
```bash
python -m retrieval.index_all
```

**Step 3: Test retrieval only** (without LLM)
```bash
# Simple search
python -m retrieval.search_test "What is the return policy?"

# Filtered search
python -m retrieval.search_test "commission fees" --doc-type seller_policy
```

## 📂 Adding New Documents

1. Place files in the appropriate folder:
   - `data/raw/policy/` - General platform policies
   - `data/raw/seller_policy/` - Seller-specific policies
   - `data/raw/buyer_policy/` - Buyer-specific policies

2. Supported formats: PDF, DOCX, HTML, Markdown

3. Re-run the pipeline:
   ```bash
   python -m ingestion.run_ingest_all
   python -m retrieval.index_all
   ```

## 🏗️ Architecture

```
Query → Embedding → Vector Search → Top-K Chunks → Gemini LLM → Answer + Citations
```

**✅ Fully Implemented RAG Pipeline:**
- **Parsing:** Multi-format support (PDF/DOCX/HTML/MD)
- **Chunking:** Heading-aware (500 tokens/chunk, 50 overlap)
- **Embedding:** `paraphrase-multilingual-MiniLM-L12-v2`
- **Vector DB:** ChromaDB (local, persistent)
- **LLM:** Gemini 3.6 Flash (latest model)
- **RAG:** Context-aware generation with source citations
- **Interface:** Interactive CLI chatbot

## 📊 Current Status

✅ **Phase 1 Complete:** Document ingestion & retrieval
✅ **Phase 2 Complete:** Gemini RAG integration

**Operational:**
- 12 documents ingested (64 chunks indexed)
- Semantic search with metadata filtering
- Multi-language query support (EN + Urdu)
- RAG-powered chatbot with Gemini 3.6 Flash
- Automatic source citations

**Known Issues:**
- Some duplicate files in raw data (cleanup script available)
- Conflicting fee schedules need reconciliation
- Empty buyer_policy folder

See `PHASE2_COMPLETE.md` for full details.

## 🛠️ Tech Stack

- **Python 3.10+**
- **Parsing:** pdfplumber, python-docx, beautifulsoup4
- **Chunking:** langchain-text-splitters
- **Embeddings:** sentence-transformers
- **Vector DB:** chromadb
- **LLM:** google-genai (Gemini 3.6 Flash)
- **Validation:** pydantic
- **Config:** python-dotenv

## 📝 Configuration

**Environment Variables (`.env` file):**
```bash
GEMINI_API_KEY=your_api_key_here
```

**Edit `config.py` to customize:**
- `MAX_CHUNK_TOKENS` - Chunk size (default: 500)
- `CHUNK_OVERLAP_TOKENS` - Overlap size (default: 50)
- `EMBEDDING_MODEL_NAME` - Embedding model
- `GEMINI_MODEL` - Gemini model name (default: gemini-3.6-flash)
- `DEFAULT_TOP_K` - Search result count (default: 5)

## 🔧 Development

**Project structure:**
```
support-assistant/
├── config.py               # Configuration
├── models/schemas.py       # Data models
├── ingestion/             # Document processing
├── embedding/             # Embedding logic
├── retrieval/             # Vector search
├── query.py               # Interactive interface
└── data/                  # Data storage
```

**Key scripts:**
- `chatbot.py` - Interactive RAG chatbot (⭐ main interface)
- `ingestion/run_ingest_all.py` - Batch document ingestion
- `retrieval/index_all.py` - Batch vector indexing
- `retrieval/search_test.py` - CLI search tool (no LLM)
- `llm/gemini_client.py` - Gemini API wrapper

## 📄 License

Proprietary - SoftSkills Engineering (Pvt) Ltd

---

**Version:** 2.0 (Phase 2 - Gemini RAG Complete)  
**Last Updated:** 2026-08-07  
**Status:** Production-ready ✅
