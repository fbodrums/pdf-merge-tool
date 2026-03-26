"""Armazenamento em memória de sessões de upload (TTL); PDFs em disco temporário."""

from __future__ import annotations

import os
import secrets
import tempfile
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path

TTL_SECONDS = 30 * 60


def _default_upload_dir() -> Path:
    """Pasta do repositório `backend/` quando roda a partir do código-fonte; senão /tmp."""
    here = Path(__file__).resolve()
    backend_root = here.parent.parent.parent.parent
    if (backend_root / "pyproject.toml").is_file():
        return backend_root / "data" / "uploads"
    return Path(tempfile.gettempdir()) / "pdf_tools_uploads"


def _upload_dir() -> Path:
    raw = os.environ.get("PDF_TOOLS_UPLOAD_DIR", "").strip()
    if raw:
        return Path(raw).expanduser().resolve()
    return _default_upload_dir()


UPLOAD_DIR = _upload_dir()
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class StoredFile:
    file_id: str
    filename: str
    file_path: Path
    password: str | None = None
    total_pages: int | None = None
    password_protected: bool = False

    @property
    def data(self) -> bytes:
        return self.file_path.read_bytes()


@dataclass
class SessionData:
    session_id: str
    files: dict[str, StoredFile] = field(default_factory=dict)
    expires_at: float = field(default_factory=lambda: time.time() + TTL_SECONDS)


def _safe_unlink(path: Path) -> None:
    try:
        path.unlink(missing_ok=True)
    except OSError:
        pass


class SessionStore:
    def __init__(self) -> None:
        self._sessions: dict[str, SessionData] = {}

    @staticmethod
    def _delete_session_files(session: SessionData) -> None:
        for sf in session.files.values():
            _safe_unlink(sf.file_path)

    def _purge_expired(self) -> None:
        now = time.time()
        dead = [sid for sid, s in self._sessions.items() if s.expires_at < now]
        for sid in dead:
            s = self._sessions[sid]
            self._delete_session_files(s)
            del self._sessions[sid]

    def create_session(self) -> SessionData:
        self._purge_expired()
        sid = secrets.token_urlsafe(16)
        s = SessionData(session_id=sid)
        self._sessions[sid] = s
        return s

    def get(self, session_id: str) -> SessionData | None:
        self._purge_expired()
        s = self._sessions.get(session_id)
        if s is None:
            return None
        if time.time() > s.expires_at:
            self._delete_session_files(s)
            del self._sessions[session_id]
            return None
        return s

    def touch(self, session_id: str) -> None:
        s = self.get(session_id)
        if s:
            s.expires_at = time.time() + TTL_SECONDS


store = SessionStore()


def new_file_id() -> str:
    return str(uuid.uuid4())
