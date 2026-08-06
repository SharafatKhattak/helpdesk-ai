from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_RAW_DIR = BASE_DIR / "data" / "raw"
DATA_PROCESSED_DIR = BASE_DIR / "data" / "processed"

DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Chunking
MAX_CHUNK_TOKENS = 500        # rough token budget per chunk before sub-splitting
CHUNK_OVERLAP_TOKENS = 50
