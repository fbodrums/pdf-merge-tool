"""Merge de vários fragmentos PDF em um único arquivo."""

from __future__ import annotations

from io import BytesIO

from pypdf import PdfReader, PdfWriter


def merge_pdf_parts(parts: list[bytes]) -> bytes:
    """Mescla PDFs na ordem fornecida."""
    writer = PdfWriter()
    for part in parts:
        reader = PdfReader(BytesIO(part))
        for page in reader.pages:
            writer.add_page(page)
    out = BytesIO()
    writer.write(out)
    return out.getvalue()
