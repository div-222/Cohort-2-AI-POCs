"""Retriever Agent.

Thin wrapper over the vector store that performs (optionally domain-filtered)
semantic search and returns the top-K candidate chunks for the Context
Optimizer to refine.
"""
from __future__ import annotations

from typing import List, Optional

from .. import config, vectorstore


def retrieve(query: str, domain_filter: Optional[str] = None, top_k: Optional[int] = None) -> List[dict]:
    top_k = top_k or config.RETRIEVE_TOP_K
    where = {"domain": domain_filter} if domain_filter in ("HR", "IT") else None
    hits = vectorstore.query_documents(query, top_k=top_k, where=where)
    # If a domain filter returned nothing (e.g. mixed query), retry unfiltered.
    if not hits and where:
        hits = vectorstore.query_documents(query, top_k=top_k)
    return hits
