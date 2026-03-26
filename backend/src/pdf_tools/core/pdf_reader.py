"""Leitura e metadados de PDF."""

from __future__ import annotations

from io import BytesIO
from typing import BinaryIO

from pypdf import PdfReader

from pdf_tools.exceptions import InvalidPDFError, PasswordProtectedError


def read_pdf(data: bytes | BinaryIO, password: str | None = None) -> PdfReader:
    """Abre um PdfReader; levanta exceções de domínio em caso de falha."""
    try:
        bio = BytesIO(data) if isinstance(data, bytes) else data
        reader = PdfReader(bio, strict=True)
    except Exception as e:  # noqa: BLE001 — pypdf pode levantar vários tipos
        raise InvalidPDFError("Arquivo PDF inválido ou corrompido.") from e

    if getattr(reader, "is_encrypted", False):
        if password is None:
            raise PasswordProtectedError("PDF protegido por senha.")
        try:
            ok = reader.decrypt(password)
        except Exception as e:  # noqa: BLE001
            raise InvalidPDFError("Não foi possível ler o PDF.") from e
        if ok == 0:
            raise InvalidPDFError("Senha incorreta.")

    try:
        _ = len(reader.pages)
    except Exception as e:  # noqa: BLE001
        raise InvalidPDFError("Não foi possível ler as páginas do PDF.") from e

    return reader


def pdf_metadata(reader: PdfReader) -> tuple[int, bool]:
    """Retorna (total_pages, is_encrypted)."""
    total = len(reader.pages)
    enc = bool(getattr(reader, "is_encrypted", False))
    return total, enc
