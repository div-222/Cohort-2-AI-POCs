"""Memory Agent — Semantic Memory.

Stores successful Q&A interactions and retrieves semantically-similar past
solutions so repetitive questions can be answered faster and with higher
confidence. Backed by a dedicated Chroma collection (embeddings on the user
question). Feedback updates the stored score.

Memory schema (per spec):
  { user_query, intent, answer, feedback, score, timestamp, sources }
"""
from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import List, Optional

from .. import config, embeddings, vectorstore


def _mem_id(query: str, ts: str) -> str:
    return hashlib.sha1(f"{query}|{ts}".encode("utf-8")).hexdigest()[:16]


def store(query: str, intent: str, answer: str, sources: List[str], score: float = 1.0) -> str:
    """Persist a successful interaction. Returns the memory id."""
    col = vectorstore.memory_collection()
    ts = datetime.now(timezone.utc).isoformat()
    mem_id = _mem_id(query, ts)
    vec = embeddings.embed([query])[0]
    col.add(
        ids=[mem_id],
        documents=[query],
        embeddings=[vec],
        metadatas=[
            {
                "user_query": query,
                "intent": intent,
                "answer": answer,
                "feedback": "",
                "score": float(score),
                "timestamp": ts,
                "sources": " | ".join(sources),
            }
        ],
    )
    return mem_id


def recall(query: str, top_k: Optional[int] = None) -> List[dict]:
    """Return semantically similar past interactions, best first."""
    col = vectorstore.memory_collection()
    if col.count() == 0:
        return []
    top_k = top_k or config.MEMORY_TOP_K
    qvec = embeddings.embed([query])[0]
    res = col.query(
        query_embeddings=[qvec],
        n_results=min(top_k, col.count()),
        include=["documents", "metadatas", "distances"],
    )
    out = []
    for doc, meta, dist, _id in zip(
        res["documents"][0], res["metadatas"][0], res["distances"][0], res["ids"][0]
    ):
        out.append(
            {
                "id": _id,
                "question": doc,
                "answer": meta.get("answer", ""),
                "intent": meta.get("intent", ""),
                "score": meta.get("score", 0.0),
                "feedback": meta.get("feedback", ""),
                "sources": meta.get("sources", ""),
                "similarity": round(1.0 - dist, 4),
            }
        )
    return out


def best_hit(query: str) -> Optional[dict]:
    """Return the top recall only if it clears the confidence threshold."""
    hits = recall(query, top_k=1)
    if hits and hits[0]["similarity"] >= config.MEMORY_HIT_THRESHOLD:
        return hits[0]
    return None


def update_feedback(mem_id: str, feedback: str) -> None:
    """Apply 👍/👎 feedback to a stored memory and adjust its score."""
    col = vectorstore.memory_collection()
    try:
        rec = col.get(ids=[mem_id], include=["metadatas"])
        if not rec["ids"]:
            return
        meta = rec["metadatas"][0]
        score = float(meta.get("score", 1.0))
        score = min(1.0, score + 0.1) if feedback == "up" else max(0.0, score - 0.4)
        meta["feedback"] = feedback
        meta["score"] = score
        col.update(ids=[mem_id], metadatas=[meta])
    except Exception:
        pass


def count() -> int:
    try:
        return vectorstore.memory_collection().count()
    except Exception:
        return 0
