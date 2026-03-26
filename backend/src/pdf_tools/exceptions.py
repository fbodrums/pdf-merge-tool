"""Exceções de domínio para manipulação de PDF."""


class PDFToolsError(Exception):
    """Erro base."""


class InvalidPDFError(PDFToolsError):
    """Arquivo não é um PDF válido ou está corrompido."""


class PasswordProtectedError(PDFToolsError):
    """PDF requer senha para leitura."""


class PageOutOfRangeError(PDFToolsError):
    """Página solicitada fora do intervalo do documento."""
