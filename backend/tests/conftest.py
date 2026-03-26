"""Fixtures de teste."""

from __future__ import annotations

from io import BytesIO

import pytest
from pypdf import PdfWriter


@pytest.fixture
def three_page_pdf() -> bytes:
    w = PdfWriter()
    for _ in range(3):
        w.add_blank_page(width=612, height=792)
    buf = BytesIO()
    w.write(buf)
    return buf.getvalue()


@pytest.fixture
def one_page_pdf() -> bytes:
    w = PdfWriter()
    w.add_blank_page(width=612, height=792)
    buf = BytesIO()
    w.write(buf)
    return buf.getvalue()
