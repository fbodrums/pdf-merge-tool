"""Testes de pdf_merger."""

from io import BytesIO

from pypdf import PdfReader, PdfWriter

from pdf_tools.core.pdf_merger import merge_pdf_parts


def _one_pager() -> bytes:
    w = PdfWriter()
    w.add_blank_page(width=612, height=792)
    buf = BytesIO()
    w.write(buf)
    return buf.getvalue()


def test_merge_two_parts() -> None:
    a, b = _one_pager(), _one_pager()
    merged = merge_pdf_parts([a, b])
    r = PdfReader(BytesIO(merged))
    assert len(r.pages) == 2


def test_merge_single() -> None:
    merged = merge_pdf_parts([_one_pager()])
    r = PdfReader(BytesIO(merged))
    assert len(r.pages) == 1
