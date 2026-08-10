# 🚀 How to Run the Support Assistant Project

## Complete Step-by-Step Guide

---

## 📋 Prerequisites

✅ Python 3.10+ installed  
✅ Virtual environment activated  
✅ All dependencies installed  

---

## 🔧 Setup (One-Time)

### 1. Activate Virtual Environment

```bash
cd C:\Users\SK\Desktop\support-assistant
source venv/Scripts/activate
```

**(On Windows CMD instead of Git Bash):**
```cmd
cd C:\Users\SK\Desktop\support-assistant
venv\Scripts\activate.bat
```

### 2. Verify Installation

```bash
python -c "import PyQt6; print('PyQt6 installed')"
python -c "from google import genai; print('Gemini SDK installed')"
```

### 3. Check API Key

Your current API key in `.env`:
```
GEMINI_API_KEY=AQ.Ab8RN6J06k0nCP_PqOcY4pPX8zFadSirzbhnq94cEhFipJo-sg
```

**Note:** This key format (`AQ.`) is non-standard. You mentioned it worked in a direct test. If you encounter authentication issues with the GUI, you may need a standard Google AI Studio API key (starts with `AIza`).

---

## 🎯 Running the Project

### Option 1: GUI Chatbot (Recommended)

**Launch the Qt-based graphical interface:**

```bash
python gui_chatbot.py
```

**What you'll see:**
- Modern chat interface with bubbles
- Sources panel on the right
- Input field at the bottom
- Status bar showing progress

**Try these questions:**
- "What are the seller commission fees?"
- "What products can I sell?"
- "How does FBA work?"

---

### Option 2: Re-run Ingestion Pipeline

If you add new documents or modify existing ones:

**Step 1: Parse & Chunk Documents**
```bash
python -m ingestion.run_ingest_all
```

**Output:**
```
Discovered 12 document(s):
Processing [policy] 01_Terms_and_Conditions.pdf...
  OK: 4 chunks -> policy__01_Terms_and_Conditions_chunks.json
...
```

**Step 2: Index into Vector Database**
```bash
python -m retrieval.index_all
```

**Output:**
```
Found 12 chunk file(s) to index:
  policy__01_Terms_and_Conditions_chunks.json: indexed 4 chunks...
...
```

---

### Option 3: Test Retrieval Only (No LLM)

Test if vector search is working without using the LLM:

```bash
python -m retrieval.search_test "What are the seller fees?"
```

**Output:**
```
Query: What are the seller fees?

--- Result 1 (distance=0.8542) ---
Source: 03 Seller Terms And Conditions
Seller commission fees are based on...
```

---

## 🗂️ Project Structure

```
support-assistant/
├── gui_chatbot.py              # ⭐ Main GUI application
├── config.py                   # Configuration
├── .env                        # API key (keep private)
│
├── data/
│   ├── raw/                    # Source documents
│   │   ├── policy/             # General platform policies
│   │   ├── seller_policy/      # Seller-specific docs
│   │   └── buyer_policy/       # Buyer-specific docs
│   ├── processed/              # Generated chunk JSONs
│   └── chroma_db/              # Vector database
│
├── ingestion/                  # Document processing
│   ├── parsers.py             # PDF/DOCX/HTML/MD parsers
│   ├── chunker.py             # Heading-aware chunking
│   ├── documents_config.py    # Auto-discovery
│   └── run_ingest_all.py      # Batch ingestion
│
├── embedding/
│   └── embedder.py            # Multilingual embeddings
│
├── retrieval/
│   ├── vector_store.py        # ChromaDB interface
│   ├── index_all.py           # Batch indexing
│   └── search_test.py         # Search testing
│
└── llm/
    └── gemini_client.py       # Gemini API wrapper
```

---

## 📝 Common Workflows

### Workflow 1: Daily Use

```bash
# Start the chatbot
python gui_chatbot.py

# Ask questions and get answers with citations
```

### Workflow 2: Add New Documents

```bash
# 1. Add PDF/DOCX/MD files to data/raw/<category>/
cp new_policy.pdf data/raw/policy/

# 2. Re-run ingestion
python -m ingestion.run_ingest_all

# 3. Re-index
python -m retrieval.index_all

# 4. Start chatbot
python gui_chatbot.py
```

### Workflow 3: Update Configuration

**Edit `config.py` to change:**
- `MAX_CHUNK_TOKENS` - Chunk size
- `GEMINI_MODEL` - Model to use
- `DEFAULT_TOP_K` - Number of search results

**Edit `.env` for:**
- `GEMINI_API_KEY` - Your API key

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'PyQt6'"

**Fix:**
```bash
source venv/Scripts/activate
pip install PyQt6
```

### Issue: "401 UNAUTHENTICATED" API Error

**Cause:** API key authentication issue

**Possible fixes:**

1. **Get standard Google AI Studio key:**
   - Go to: https://aistudio.google.com/apikey
   - Create API key (starts with `AIza`)
   - Update `.env`:
     ```
     GEMINI_API_KEY=AIzaSyD_your_key_here
     ```

2. **OR use Google Cloud credentials:**
   - If using GCP OAuth, set up application default credentials
   - Run: `gcloud auth application-default login`

### Issue: GUI doesn't start

**Check:**
```bash
# Verify Python version
python --version  # Should be 3.10+

# Verify PyQt6
python -c "from PyQt6.QtWidgets import QApplication; print('OK')"

# Check if running from correct directory
pwd  # Should be .../support-assistant
```

### Issue: No results from search

**Check:**
```bash
# Verify vector database exists
ls data/chroma_db/

# Re-index if needed
python -m retrieval.index_all
```

### Issue: "No chunks found"

**Fix:**
```bash
# Re-run ingestion
python -m ingestion.run_ingest_all

# Check processed files
ls data/processed/
```

---

## 📊 Current Data Status

**Indexed documents:** 12 files  
**Total chunks:** 64  
**Categories:**
- Policy: 5 files (some duplicates)
- Seller Policy: 7 files
- Buyer Policy: 0 files (empty)

**Vector database:** ChromaDB (local, persistent)  
**Embedding model:** paraphrase-multilingual-MiniLM-L12-v2  
**LLM model:** gemini-3.5-flash

---

## ⚡ Quick Commands Reference

```bash
# Activate environment
source venv/Scripts/activate

# Run GUI chatbot
python gui_chatbot.py

# Re-ingest documents
python -m ingestion.run_ingest_all

# Re-index vectors
python -m retrieval.index_all

# Test search
python -m retrieval.search_test "your question"

# Check dependencies
pip list | grep -E "PyQt6|google-genai|chromadb"
```

---

## 🎓 Usage Examples

### Example 1: Seller Question

**Launch:**
```bash
python gui_chatbot.py
```

**Ask:**
> "What are the commission fees for sellers?"

**Expected:**
- Detailed answer about commission structure
- Citations showing which documents were used
- Sources panel showing:
  - [1] Seller Terms And Conditions
  - [2] Commission and Fee Schedule

### Example 2: Product Listing

**Ask:**
> "What products can I sell on SoftStore?"

**Expected:**
- List of allowed products
- Restrictions and requirements
- Citations from seller policies

### Example 3: FBA Information

**Ask:**
> "How does Fulfilled by SoftStore (FBA) work?"

**Expected:**
- FBA process explanation
- Fee structure
- Requirements
- Citations from FBA guides

---

## 💡 Tips

**For best results:**
- Be specific in your questions
- Include context (buyer vs seller perspective)
- Check the Sources panel for citation details
- Ask follow-up questions for clarification

**Performance:**
- First query loads embedding model (~2-3 seconds)
- Subsequent queries are faster (~1-2 seconds)
- UI remains responsive during queries

**Maintenance:**
- Clean up duplicate files (see `cleanup_duplicates.py`)
- Update documents as policies change
- Re-run ingestion + indexing after updates

---

## 🔐 Security Notes

✅ **Do:**
- Keep `.env` file private
- Never commit API keys to git
- Regenerate keys if exposed

❌ **Don't:**
- Share `.env` file
- Commit `.env` to version control
- Hardcode API keys in source

---

## 📚 Documentation

- **Setup Guide:** GUI_SETUP.md
- **API Key Issues:** API_KEY_FIX.md
- **Project Status:** PHASE2_COMPLETE.md
- **Technical Details:** STATUS.md

---

## ✅ Quick Checklist

Before running:
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip list`)
- [ ] API key in `.env` file
- [ ] Documents in `data/raw/`
- [ ] ChromaDB indexed (`data/chroma_db/` exists)

To start:
```bash
python gui_chatbot.py
```

---

## 🆘 Need Help?

**If authentication issues persist:**

The key format `AQ.` suggests it might be:
1. A Google Cloud OAuth token (expires)
2. A non-standard API key format
3. Requires different authentication flow

**Standard Gemini API keys:**
- Start with `AIza`
- From https://aistudio.google.com/apikey
- 39 characters long
- Work with simple API key authentication

If current key continues to have issues, get a standard key from AI Studio.

---

## 🎉 Summary

**To run the project:**
1. Open terminal
2. `cd C:\Users\SK\Desktop\support-assistant`
3. `source venv/Scripts/activate`
4. `python gui_chatbot.py`
5. Ask questions!

**That's it!** 🚀
