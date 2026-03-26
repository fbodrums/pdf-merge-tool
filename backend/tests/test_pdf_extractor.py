"""Testes de pdf_extractor."""

import pytest

from pdf_tools.core.pdf_extractor import extract_pages_bytes
from pdf_tools.exceptions import PageOutOfRangeError


def test_extract_default_pages(three_page_pdf: bytes) -> None:
    out = extract_pages_bytes(three_page_pdf, None)
    from pypdf import PdfReader

    r = PdfReader(__import__("io").BytesIO(out))
    assert len(r.pages) == 2


def test_extract_custom_pages(three_page_pdf: bytes) -> None:
    out = extract_pages_bytes(three_page_pdf, "1,3")
    from pypdf import PdfReader

    r = PdfReader(__import__("io").BytesIO(out))
    assert len(r.pages) == 2


def test_extract_invalid_range(three_page_pdf: bytes) -> None:
    with pytest.raises(PageOutOfRangeError):
        extract_pages_bytes(three_page_pdf, "10")


def test_extract_single_page_doc(one_page_pdf: bytes) -> None:
    out = extract_pages_bytes(one_page_pdf, None)
    from pypdf import PdfReader

    r = PdfReader(__import__("io").BytesIO(out))
    assert len(r.pages) == 1
