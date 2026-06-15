"""Context Optimizer.

Takes raw retrieved chunks and produces a lean, high-signal context for the
reasoning LLM. Implements the three methods from the spec:

  1. Remove duplicate chunks  -> near-duplicate detection via embedding cosine
  2. Chunk reranking          -> cross-encoder relevance scoring
  3. Context compression      -> keep top-N, then trim to a character budget

Reports an estimated token saving (before vs after) as the "expected benefit".
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from .. import config, embeddings


def _approx_tokens(text: str) -> int:
    # ~4 chars/token is a reasonable English approximation.
    return max(1, len(text) // 4)


def _cosine(a, b) -> float:
    return sum(x * y for x, y in zip(a, b))  # vectors are normalized


def _dedup(chunks: List[dict]) -> List[dict]:
    """Drop near-duplicate chunks using embedding cosine similarity."""
    if len(chunks) <= 1:
        return chunks
    vecs = embeddings.embed([c["text"] for c in chunks])
    kept: List[dict] = []
    kept_vecs = []
    for c, v in zip(chunks, vecs):
        if any(_cosine(v, kv) >= config.DEDUP_THRESHOLD for kv in kept_vecs):
            continue
        kept.append(c)
        kept_vecs.append(v)
    return kept


@dataclass
class OptimizerReport:
    chunks_in: int = 0
    chunks_after_dedup: int = 0
    chunks_out: int = 0
    tokens_before: int = 0
    tokens_after: int = 0
    saved_pct: float = 0.0
    chunks: List[dict] = field(default_factory=list)

    def as_dict(self) -> Dict:
        return {
            "chunks_in": self.chunks_in,
            "chunks_after_dedup": self.chunks_after_dedup,
            "chunks_out": self.chunks_out,
            "tokens_before": self.tokens_before,
            "tokens_after": self.tokens_after,
            "saved_pct": self.saved_pct,
        }


def optimize(query: str, chunks: List[dict]) -> OptimizerReport:
    report = OptimizerReport(chunks_in=len(chunks))
    report.tokens_before = sum(_approx_tokens(c["text"]) for c in chunks)

    if not chunks:
        return report

    # 1. Dedup
    deduped = _dedup(chunks)
    report.chunks_after_dedup = len(deduped)

    # 2. Rerank (cross-encoder); fall back to vector similarity order
    scores = embeddings.rerank(query, [c["text"] for c in deduped])
    for c, s in zip(deduped, scores):
        c["rerank_score"] = round(float(s), 4)
    if any(scores):
        deduped.sort(key=lambda c: c["rerank_score"], reverse=True)
    else:
        deduped.sort(key=lambda c: c.get("similarity", 0), reverse=True)

    # 3. Compress: keep top-N, then enforce a character budget
    kept = deduped[: config.RERANK_TOP_N]
    budget = config.MAX_CONTEXT_CHARS
    final: List[dict] = []
    used = 0
    for c in kept:
        text = c["text"]
        if used + len(text) > budget:
            remaining = budget - used
            if remaining < 200:
                break
            text = text[:remaining].rsplit(" ", 1)[0] + " …"
            c = {**c, "text": text}
        final.append(c)
        used += len(text)

    report.chunks = final
    report.chunks_out = len(final)
    report.tokens_after = sum(_approx_tokens(c["text"]) for c in final)
    if report.tokens_before:
        report.saved_pct = round(
            100 * (1 - report.tokens_after / report.tokens_before), 1
        )
    return report
