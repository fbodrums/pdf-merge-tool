"""Testes de page_config."""

import pytest

from pdf_tools.core.page_config import parse_page_tokens, resolve_pages_for_document
from pdf_tools.exceptions import PageOutOfRangeError


def test_parse_simple_numbers() -> None:
    assert parse_page_tokens("1, 3, 5") == [1, 3, 5]


def test_parse_range() -> None:
    assert parse_page_tokens("2-4") == [2, 3, 4]


def test_parse_combined() -> None:
    assert parse_page_tokens("1,3-5,8") == [1, 3, 4, 5, 8]


def test_parse_duplicates_removed_sorted() -> None:
    assert parse_page_tokens("1,1,2-3,2") == [1, 2, 3]


def test_invalid_range() -> None:
    with pytest.raises(ValueError, match="Intervalo inválido"):
        parse_page_tokens("5-2")


def test_invalid_token() -> None:
    with pytest.raises(ValueError):
        parse_page_tokens("1,abc")


def test_resolve_default() -> None:
    assert resolve_pages_for_document(None, 5) == [1, 2]
    assert resolve_pages_for_document("", 5) == [1, 2]


def test_resolve_default_single_page_doc() -> None:
    assert resolve_pages_for_document(None, 1) == [1]


def test_resolve_out_of_range() -> None:
    with pytest.raises(PageOutOfRangeError):
        resolve_pages_for_document("10", 5)
