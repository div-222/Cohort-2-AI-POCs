"""ChromaDB wrapper for the document index and the semantic memory store.

Two persistent collections live side by side:
  * ``documents`` — chunked HR/IT policy text used for Agentic RAG retrieval.
  * ``memory``    — past Q&A interactions used as Semantic Memory.

Embeddings are computed by our local sentence-transformers model and passed in
explicitly, so Chroma never needs network access.
"""
from __future__ import annotations

from typing import Dict, List, Optional

import chromadb

from . import config, embeddings

_client: Optional[chromadb.ClientAPI] = None


def client() -> chromadb.ClientAPI:
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=str(config.CHROMA_DIR))
    return _client


def documents_collection():
    return client().get_or_create_collection(
        "documents", metadata={"hnsw:space": "cosine"}
    )


def memory_collection():
    return client().get_or_create_collection(
        "memory", metadata={"hnsw:space": "cosine"}
    )


# --- Document index -------------------------------------------------------
def reset_documents() -> None:
    try:
        client().delete_collection("documents")
    except Exception:
        pass


def add_documents(ids: List[str], texts: List[str], metadatas: List[Dict]) -> None:
    col = documents_collection()
    vecs = embeddings.embed(texts)
    col.add(ids=ids, documents=texts, embeddings=vecs, metadatas=metadatas)


def query_documents(query: str, top_k: int, where: Optional[Dict] = None) -> List[Dict]:
    col = documents_collection()
    if col.count() == 0:
        return []
    qvec = embeddings.embed([query])[0]
    res = col.query(
        query_embeddings=[qvec],
        n_results=min(top_k, col.count()),
        where=where or None,
        include=["documents", "metadatas", "distances"],
    )
    out = []
    for doc, meta, dist in zip(
        res["documents"][0], res["metadatas"][0], res["distances"][0]
    ):
        out.append(
            {
                "text": doc,
                "metadata": meta,
                # cosine distance -> similarity
                "similarity": round(1.0 - dist, 4),
            }
        )
    return out


def document_count() -> int:
    try:
        return documents_collection().count()
    except Exception:
        return 0
