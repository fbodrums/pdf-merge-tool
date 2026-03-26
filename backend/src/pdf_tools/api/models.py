"""Modelos Pydantic da API."""

from __future__ import annotations

from pydantic import BaseModel, Field


class UploadedFileInfo(BaseModel):
    file_id: str
    filename: str
    total_pages: int | None = None
    size_bytes: int
    password_protected: bool = False


class UploadResponse(BaseModel):
    session_id: str
    files: list[UploadedFileInfo]


class UnlockRequest(BaseModel):
    session_id: str
    file_id: str
    password: str = Field(..., min_length=1)


class UnlockResponse(BaseModel):
    file_id: str
    total_pages: int
    password_protected: bool = False


class MergeItem(BaseModel):
    file_id: str
    pages: str | None = None  # None = padrão


class MergeRequest(BaseModel):
    session_id: str
    items: list[MergeItem]
    output_filename: str | None = "merged.pdf"


class ErrorResponse(BaseModel):
    detail: str
