"""Build the document index from the corpus in ``data/``.

Enhanced multi-format ingestion supporting:
- Markdown (.md)
- PDF (.pdf)
- Word documents (.docx)
- Text files (.txt)
- Web bookmarks/HTML (.html)

We use intelligent chunkers: split on headings/sections while preserving context,
then sub-split any oversized section by character window with overlap. Each chunk
carries metadata including timestamps for temporal queries.
"""
from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

from . import config, vectorstore

# Conditional imports for document processing
try:
    from PyPDF2 import PdfReader
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    from docx import Document as DocxDocument
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    HTML_AVAILABLE = True
except ImportError:
    HTML_AVAILABLE = False


def _domain_for(filename: str) -> str:
    """Categorize document by filename pattern."""
    name = filename.lower()
    if name.startswith("it_"):
        return "IT"
    elif name.startswith("hr_") or name.startswith("sails_"):
        return "HR"
    elif "note" in name or "bookmark" in name:
        return "Personal"
    elif "email" in name:
        return "Email"
    elif "article" in name or "research" in name:
        return "Research"
    return "General"


def _pretty_title(filename: str) -> str:
    stem = Path(filename).stem
    stem = re.sub(r"^(it_sop_|it_|hr_|sails_)", "", stem, flags=re.IGNORECASE)
    return stem.replace("_", " ").title()


def _extract_pdf_text(path: Path) -> str:
    """Extract text from PDF file."""
    if not PDF_AVAILABLE:
        return ""
    try:
        reader = PdfReader(str(path))
        text_parts = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)
        return "\n\n".join(text_parts)
    except Exception as e:
        print(f"  ⚠️  PDF extraction failed for {path.name}: {e}")
        return ""


def _extract_docx_text(path: Path) -> str:
    """Extract text from Word document."""
    if not DOCX_AVAILABLE:
        return ""
    try:
        doc = DocxDocument(str(path))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n\n".join(paragraphs)
    except Exception as e:
        print(f"  ⚠️  DOCX extraction failed for {path.name}: {e}")
        return ""


def _extract_html_text(path: Path) -> str:
    """Extract text from HTML/bookmark file."""
    if not HTML_AVAILABLE:
        return ""
    try:
        html = path.read_text(encoding="utf-8")
        soup = BeautifulSoup(html, 'html.parser')
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text()
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text
    except Exception as e:
        print(f"  ⚠️  HTML extraction failed for {path.name}: {e}")
        return ""


def extract_text(path: Path) -> str:
    """Extract text from any supported file format."""
    suffix = path.suffix.lower()
    
    if suffix == ".md":
        return path.read_text(encoding="utf-8")
    elif suffix == ".txt":
        return path.read_text(encoding="utf-8")
    elif suffix == ".pdf":
        return _extract_pdf_text(path)
    elif suffix == ".docx":
        return _extract_docx_text(path)
    elif suffix in [".html", ".htm"]:
        return _extract_html_text(path)
    else:
        # Try reading as text
        try:
            return path.read_text(encoding="utf-8")
        except Exception:
            return ""


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

    # Support multiple file formats
    patterns = ["*.md", "*.txt", "*.pdf", "*.docx", "*.html", "*.htm"]
    files = []
    for pattern in patterns:
        files.extend(config.DATA_DIR.glob(pattern))
    
    files = sorted(set(files))  # Remove duplicates
    total_chunks = 0
    per_doc = {}

    for path in files:
        text = extract_text(path)
        if not text:
            if verbose:
                print(f"  ⏭️  Skipped {path.name:40s} (no extractable text)")
            continue
            
        domain = _domain_for(path.name)
        title = _pretty_title(path.name)
        
        # Get file modification time for temporal queries
        mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
        
        # Chunk based on format
        if path.suffix.lower() == ".md":
            chunks = chunk_markdown(text)
        else:
            # Generic text chunking for non-markdown
            chunks = [(title, chunk) for chunk in _window(text, config.CHUNK_SIZE, config.CHUNK_OVERLAP)]

        ids, texts, metas = [], [], []
        for i, (heading, chunk_text) in enumerate(chunks):
            if not chunk_text.strip():
                continue
            ids.append(f"{path.stem}::{i}")
            texts.append(chunk_text)
            metas.append(
                {
                    "source": path.name,
                    "title": title,
                    "domain": domain,
                    "heading": heading or title,
                    "file_type": path.suffix.lower()[1:],  # Remove the dot
                    "modified_date": mtime.isoformat(),
                    "year": mtime.year,
                    "month": mtime.month,
                }
            )
        if texts:
            vectorstore.add_documents(ids, texts, metas)
        per_doc[path.name] = len(texts)
        total_chunks += len(texts)
        if verbose:
            file_type = path.suffix.upper()[1:]
            print(f"  indexed {path.name:40s} -> {len(texts):3d} chunks ({file_type}/{domain})")

    report = {"files": len(files), "chunks": total_chunks, "per_doc": per_doc}
    if verbose:
        print(f"\nDone: {len(files)} files, {total_chunks} chunks.")
    return report


def ingest_uploaded_file(
    file_content: bytes,
    filename: str,
    file_type: str,
    custom_title: str = "",
    domain: str = "Personal"
) -> Dict[str, int]:
    """Process and index a single uploaded file. Returns chunk count."""
    from io import BytesIO
    import tempfile
    
    # Save temporarily to extract text
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(filename).suffix) as tmp:
        tmp.write(file_content)
        tmp_path = Path(tmp.name)
    
    try:
        text = extract_text(tmp_path)
        if not text:
            return {"chunks": 0, "error": "Could not extract text"}
        
        title = custom_title or _pretty_title(filename)
        now = datetime.now(timezone.utc)
        
        # Chunk the document
        if tmp_path.suffix.lower() == ".md":
            chunks = chunk_markdown(text)
        else:
            chunks = [(title, chunk) for chunk in _window(text, config.CHUNK_SIZE, config.CHUNK_OVERLAP)]
        
        ids, texts, metas = [], [], []
        base_id = filename.replace(".", "_").replace(" ", "_")
        for i, (heading, chunk_text) in enumerate(chunks):
            if not chunk_text.strip():
                continue
            ids.append(f"{base_id}::{now.timestamp()}::{i}")
            texts.append(chunk_text)
            metas.append(
                {
                    "source": filename,
                    "title": title,
                    "domain": domain,
                    "heading": heading or title,
                    "file_type": file_type,
                    "modified_date": now.isoformat(),
                    "year": now.year,
                    "month": now.month,
                    "uploaded": True,
                }
            )
        
        if texts:
            vectorstore.add_documents(ids, texts, metas)
        
        return {"chunks": len(texts), "title": title}
    
    finally:
        # Clean up temp file
        tmp_path.unlink(missing_ok=True)


if __name__ == "__main__":
    print("Building document index from", config.DATA_DIR)
    build_index(verbose=True)
