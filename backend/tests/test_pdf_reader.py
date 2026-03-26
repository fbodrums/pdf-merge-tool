"""Testes de pdf_reader."""

import pytest
from pypdf import PdfWriter

from pdf_tools.core.pdf_reader import read_pdf
from pdf_tools.exceptions import InvalidPDFError


def test_read_valid_pdf(three_page_pdf: bytes) -> None:
    r = read_pdf(three_page_pdf)
    assert len(r.pages) == 3


def test_read_invalid_bytes() -> None:
    with pytest.raises(InvalidPDFError):
        read_pdf(b"not a pdf")
