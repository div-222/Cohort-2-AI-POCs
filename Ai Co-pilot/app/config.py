"""Central configuration for the AI Co-Pilot POC.

All tunables live here so the rest of the code stays declarative. Values are
read from environment variables (loaded from a local ``.env``) with sensible
offline-friendly defaults.
"""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# Project layout -----------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
STORAGE_DIR = ROOT / "storage"
CHROMA_DIR = ROOT / ".chroma"
TOOL_LOG_PATH = STORAGE_DIR / "tool_activity.jsonl"
COST_LEDGER_PATH = STORAGE_DIR / "cost_ledger.jsonl"

STORAGE_DIR.mkdir(exist_ok=True)
CHROMA_DIR.mkdir(exist_ok=True)

load_dotenv(ROOT / ".env")

# LLM ----------------------------------------------------------------------
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash").strip()

# Local models -------------------------------------------------------------
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2").strip()
RERANKER_MODEL = os.getenv("RERANKER_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2").strip()

# Retrieval / RAG knobs ----------------------------------------------------
CHUNK_SIZE = 900          # target characters per chunk
CHUNK_OVERLAP = 150       # overlap between consecutive chunks
RETRIEVE_TOP_K = 8        # candidates pulled from the vector store
RERANK_TOP_N = 4          # chunks kept after the Context Optimizer
MEMORY_TOP_K = 3          # similar past interactions to consider
MEMORY_HIT_THRESHOLD = 0.86   # cosine sim above which memory is "confident"
DEDUP_THRESHOLD = 0.93        # cosine sim above which two chunks are duplicates
MAX_CONTEXT_CHARS = 6000      # hard cap fed to the reasoning LLM

# Gemini pricing (USD per 1,000,000 tokens). Used by the Cost Monitor.
# Source: public Gemini API pricing; adjust as needed for your account.
PRICING = {
    "gemini-2.0-flash":      {"input": 0.10,  "output": 0.40},
    "gemini-2.0-flash-lite": {"input": 0.075, "output": 0.30},
    "gemini-1.5-flash":      {"input": 0.075, "output": 0.30},
    "gemini-1.5-flash-8b":   {"input": 0.0375, "output": 0.15},
    "gemini-1.5-pro":        {"input": 1.25,  "output": 5.00},
    "gemini-2.5-flash":      {"input": 0.30,  "output": 2.50},
    "gemini-2.5-pro":        {"input": 1.25,  "output": 10.00},
}


def price_for(model: str) -> dict:
    """Return per-1M-token pricing for a model, defaulting to flash rates."""
    return PRICING.get(model, {"input": 0.10, "output": 0.40})


_PLACEHOLDER = "your-gcp-gemini-api-key-here"


def llm_available() -> bool:
    return bool(GOOGLE_API_KEY) and GOOGLE_API_KEY != _PLACEHOLDER
