"""Parsing e validação de especificação de páginas (1-based)."""

from __future__ import annotations

import re
from typing import Iterable

from pdf_tools.exceptions import PageOutOfRangeError

_DEFAULT_PAGES = (1, 2)
_TOKEN_RE = re.compile(r"^\s*(\d+)\s*-\s*(\d+)\s*$")
_NUM_RE = re.compile(r"^\s*(\d+)\s*$")


def parse_page_tokens(spec: str) -> list[int]:
    """
    Converte string como '1,3-5,8' em lista de páginas 1-based, sem duplicatas, ordenada.
    Espaços são ignorados. Partes vazias são ignoradas.
    """
    spec = (spec or "").strip()
    if not spec:
        return []

    pages: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        m_range = _TOKEN_RE.match(part)
        if m_range:
            start, end = int(m_range.group(1)), int(m_range.group(2))
            if start > end:
                raise ValueError(
                    "Intervalo inválido: o início deve ser menor ou igual ao fim"
                )
            for p in range(start, end + 1):
                pages.add(p)
            continue
        m_num = _NUM_RE.match(part)
        if m_num:
            pages.add(int(m_num.group(1)))
            continue
        raise ValueError(f"Trecho inválido na especificação de páginas: {part!r}")

    return sorted(pages)


def _pages_within_total(pages: Iterable[int], total_pages: int) -> None:
    for p in pages:
        if p < 1 or p > total_pages:
            raise PageOutOfRangeError(
                f"Página {p} não existe. O documento possui {total_pages} página(s)."
            )


def resolve_pages_for_document(
    spec: str | None,
    total_pages: int,
) -> list[int]:
    """
    Retorna lista 1-based de páginas a extrair.
    - spec vazio/None: padrão (1,2) limitado a páginas existentes.
    - spec preenchido: parse + validação contra total_pages.
    """
    if total_pages < 1:
        return []

    if spec is None or not str(spec).strip():
        raw = [p for p in _DEFAULT_PAGES if p <= total_pages]
        return raw

    pages = parse_page_tokens(str(spec))
    _pages_within_total(pages, total_pages)
    return pages
