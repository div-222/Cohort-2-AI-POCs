"""Build the document index from the markdown corpus in ``data/``.

We use a markdown-aware chunker: split on headings first (so each chunk keeps
a coherent topic + heading breadcrumb), then sub-split any oversized section by
character window with overlap. Each chunk carries metadata used for filtered
retrieval and citations.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Tuple

from . import config, vectorstore


def _domain_for(filename: str) -> str:
    name = filename.lower()
    if name.startswith("it_"):
        return "IT"
    return "HR"


def _pretty_title(filename: str) -> str:
    stem = Path(filename).stem
    stem = re.sub(r"^(it_sop_|it_|hr_|sails_)", "", stem, flags=re.IGNORECASE)
    return stem.replace("_", " ").title()


def _split_by_headings(md: str) -> List[Tuple[str, str]]:
    """Return (heading_breadcrumb, section_text) tuples."""
    lines = md.splitlines()
    sections: List[Tuple[str, str]] = []
    crumb: List[str] = []
    buf: List[str] = []
    cur_heading = ""

    def flush():
        text = "\n".join(buf).strip()
        if text:
            sections.append((cur_heading, text))

    for line in lines:
        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            flush()
            buf = []
            level = len(m.group(1))
            title = m.group(2).strip()
            crumb = crumb[: level - 1] + [title]
            cur_heading = " > ".join(crumb)
            buf.append(line)
        else:
            buf.append(line)
    flush()
    return sections


def _window(text: str, size: int, overlap: int) -> List[str]:
    if len(text) <= size:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks


def chunk_markdown(md: str) -> List[Tuple[str, str]]:
    """Return (heading, chunk_text) pairs ready for embedding."""
    out: List[Tuple[str, str]] = []
    for heading, section in _split_by_headings(md):
        for piece in _window(section, config.CHUNK_SIZE, config.CHUNK_OVERLAP):
            out.append((heading, piece.strip()))
    return out


def build_index(verbose: bool = True) -> Dict[str, int]:
    """(Re)build the document collection from scratch. Returns a small report."""
    vectorstore.reset_documents()

    files = sorted(config.DATA_DIR.glob("*.md"))
    total_chunks = 0
    per_doc = {}

    for path in files:
        md = path.read_text(encoding="utf-8")
        domain = _domain_for(path.name)
        title = _pretty_title(path.name)
        chunks = chunk_markdown(md)

        ids, texts, metas = [], [], []
        for i, (heading, text) in enumerate(chunks):
            if not text:
                continue
            ids.append(f"{path.stem}::{i}")
            texts.append(text)
            metas.append(
                {
                    "source": path.name,
                    "title": title,
                    "domain": domain,
                    "heading": heading or title,
                }
            )
        if texts:
            vectorstore.add_documents(ids, texts, metas)
        per_doc[path.name] = len(texts)
        total_chunks += len(texts)
        if verbose:
            print(f"  indexed {path.name:40s} -> {len(texts):3d} chunks ({domain})")

    report = {"files": len(files), "chunks": total_chunks, "per_doc": per_doc}
    if verbose:
        print(f"\nDone: {len(files)} files, {total_chunks} chunks.")
    return report


if __name__ == "__main__":
    print("Building document index from", config.DATA_DIR)
    build_index(verbose=True)
