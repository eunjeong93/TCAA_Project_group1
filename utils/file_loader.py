"""
file_loader.py — TCAA Notes Search Engine
Loads plain text from .txt, .pdf, and .docx files into a single string.
Whitespace is normalized before returning.
"""

import os
import re
from typing import Optional


def load_file(filepath: str) -> str:
    """
    Load and return the text content of a .txt, .pdf, or .docx file.

    Supported extensions:
        .txt  — opened with UTF-8 encoding (bad bytes are ignored)
        .pdf  — text extracted via PyPDF2.PdfReader, page by page
        .docx — text extracted via python-docx, paragraph by paragraph

    After extraction, multiple consecutive whitespace characters (spaces,
    newlines, tabs) are collapsed to a single space and the result is stripped.
    This uses re.sub(r'\\s+', ' ', text).strip() — the only permitted use of
    the `re` module in this project.

    Args:
        filepath: Absolute or relative path to the file.

    Returns:
        A single normalized string of the file's text content.

    Raises:
        FileNotFoundError: If the path does not point to an existing file.
        ValueError:        If the file extension is not .txt, .pdf, or .docx.
        RuntimeError:      If PyPDF2 or python-docx raises an error while
                           reading a (possibly corrupted) file.
    """
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"File not found: {filepath!r}")

    _, ext = os.path.splitext(filepath)
    ext = ext.lower()

    if ext == ".txt":
        raw_text = _load_txt(filepath)
    elif ext == ".pdf":
        raw_text = _load_pdf(filepath)
    elif ext == ".docx":
        raw_text = _load_docx(filepath)
    else:
        raise ValueError(
            f"Unsupported file type {ext!r}. "
            "Accepted extensions: .txt, .pdf, .docx"
        )

    # Normalize whitespace: collapse runs of spaces/newlines/tabs to one space
    return re.sub(r'\s+', ' ', raw_text).strip()


# ── Private helpers ────────────────────────────────────────────────────────────

def _load_txt(filepath: str) -> str:
    """Read a plain-text file and return its contents as a string."""
    with open(filepath, encoding="utf-8", errors="ignore") as fh:
        return fh.read()


def _load_pdf(filepath: str) -> str:
    """Extract text from each page of a PDF and concatenate them."""
    try:
        import PyPDF2  # local import so txt/docx paths have no hard dependency
    except ImportError as exc:
        raise RuntimeError(
            "PyPDF2 is required to load PDF files. "
            "Install it with:  pip install PyPDF2"
        ) from exc

    try:
        pages: list[str] = []
        with open(filepath, "rb") as fh:
            reader = PyPDF2.PdfReader(fh)
            for page in reader.pages:
                page_text = page.extract_text() or ""
                pages.append(page_text)
        return "\n".join(pages)
    except Exception as exc:
        raise RuntimeError(
            f"Failed to read PDF {filepath!r}: {exc}"
        ) from exc


def _load_docx(filepath: str) -> str:
    """Extract text from every paragraph of a DOCX file."""
    try:
        import docx  # python-docx
    except ImportError as exc:
        raise RuntimeError(
            "python-docx is required to load DOCX files. "
            "Install it with:  pip install python-docx"
        ) from exc

    try:
        document = docx.Document(filepath)
        return "\n".join(para.text for para in document.paragraphs)
    except Exception as exc:
        raise RuntimeError(
            f"Failed to read DOCX {filepath!r}: {exc}"
        ) from exc
