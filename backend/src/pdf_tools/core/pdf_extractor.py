"""Extração de páginas específicas."""

from __future__ import annotations

from io import BytesIO

from pypdf import PdfReader, PdfWriter

from pdf_tools.core.page_config import resolve_pages_for_document
from pdf_tools.core.pdf_reader import read_pdf


def extract_pages_bytes(
    pdf_bytes: bytes,
    pages_spec: str | None,
    password: str | None = None,
) -> bytes:
    """
    Extrai páginas conforme especificação (None = padrão 1,2).
    Retorna PDF com apenas as páginas selecionadas.
    """
    reader = read_pdf(pdf_bytes, password=password)
    total = len(reader.pages)
    pages_1based = resolve_pages_for_document(pages_spec, total)

    writer = PdfWriter()
    for p in pages_1based:
        writer.add_page(reader.pages[p - 1])

    out = BytesIO()
    writer.write(out)
    return out.getvalue()
