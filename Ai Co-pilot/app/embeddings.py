"""Local embedding + reranking models (sentence-transformers).

Models are loaded lazily and cached as module-level singletons so the heavy
weights are only read into memory once per process. Everything here runs
fully offline after the first download.
"""
from __future__ import annotations

from functools import lru_cache
from typing import List

from . import config

_embedder = None
_reranker = None


def _get_embedder():
    global _embedder
    if _embedder is None:
        from sentence_transformers import SentenceTransformer

        _embedder = SentenceTransformer(config.EMBEDDING_MODEL)
    return _embedder


def embed(texts: List[str]) -> List[List[float]]:
    """Embed a batch of texts into normalized vectors."""
    model = _get_embedder()
    vecs = model.encode(
        texts, normalize_embeddings=True, show_progress_bar=False, convert_to_numpy=True
    )
    return vecs.tolist()


@lru_cache(maxsize=512)
def embed_one(text: str) -> tuple:
    """Embed a single string (cached). Returns a tuple so it's hashable."""
    return tuple(embed([text])[0])


def _get_reranker():
    global _reranker
    if _reranker is None:
        from sentence_transformers import CrossEncoder

        _reranker = CrossEncoder(config.RERANKER_MODEL)
    return _reranker


def rerank(query: str, passages: List[str]) -> List[float]:
    """Return a relevance score for each passage given the query.

    Uses a cross-encoder, which is far more accurate than bi-encoder cosine
    similarity for ranking. Falls back gracefully if the model is unavailable.
    """
    if not passages:
        return []
    try:
        model = _get_reranker()
        pairs = [[query, p] for p in passages]
        scores = model.predict(pairs, show_progress_bar=False)
        return [float(s) for s in scores]
    except Exception:
        # If the reranker can't load, signal "no opinion" so callers keep
        # the original vector-search order.
        return [0.0] * len(passages)
