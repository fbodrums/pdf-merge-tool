"""Testes da API FastAPI."""

import importlib
from io import BytesIO
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from pypdf import PdfWriter

import pdf_tools.main as main_mod


@pytest.fixture(autouse=True)
def _disable_auth_for_api_tests(monkeypatch: pytest.MonkeyPatch) -> None:
    """Evita que `backend/.env` com AUTH_ENABLED=true quebre testes sem sessão."""
    monkeypatch.setenv("AUTH_ENABLED", "false")
    importlib.reload(main_mod)


@pytest.fixture
def client() -> TestClient:
    """Usa `main_mod.app` para refletir `importlib.reload` feito em outros testes."""
    return TestClient(main_mod.app)


def _pdf_bytes(pages: int = 2) -> bytes:
    w = PdfWriter()
    for _ in range(pages):
        w.add_blank_page(width=612, height=792)
    buf = BytesIO()
    w.write(buf)
    return buf.getvalue()


def test_health(client: TestClient) -> None:
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_upload_and_merge(client: TestClient) -> None:
    pdf = _pdf_bytes(3)
    r = client.post(
        "/api/upload",
        files=[
            ("files", ("a.pdf", pdf, "application/pdf")),
            ("files", ("b.pdf", pdf, "application/pdf")),
        ],
    )
    assert r.status_code == 200, r.text
    data = r.json()
    sid = data["session_id"]
    fids = [f["file_id"] for f in data["files"]]

    m = client.post(
        "/api/merge",
        json={
            "session_id": sid,
            "items": [
                {"file_id": fids[0], "pages": "1"},
                {"file_id": fids[1], "pages": "1-2"},
            ],
            "output_filename": "out.pdf",
        },
    )
    assert m.status_code == 200, m.text
    assert m.headers["content-type"] == "application/pdf"
    body = m.content
    from pypdf import PdfReader

    pr = PdfReader(BytesIO(body))
    assert len(pr.pages) == 3


def test_upload_invalid(client: TestClient) -> None:
    r = client.post(
        "/api/upload",
        files=[("files", ("bad.pdf", b"nope", "application/pdf"))],
    )
    assert r.status_code == 422


def test_upload_atomic_rollback_cleans_temp_files(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Com falha no meio do lote, nenhum arquivo deve permanecer no diretório de upload."""
    monkeypatch.setattr(main_mod, "UPLOAD_DIR", tmp_path)
    pdf = _pdf_bytes(2)
    r = client.post(
        "/api/upload",
        files=[
            ("files", ("ok.pdf", pdf, "application/pdf")),
            ("files", ("bad.pdf", b"not-a-pdf", "application/pdf")),
        ],
    )
    assert r.status_code == 422
    assert list(tmp_path.iterdir()) == []


def test_upload_returns_size_bytes_from_file(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(main_mod, "UPLOAD_DIR", tmp_path)
    pdf = _pdf_bytes(1)
    r = client.post(
        "/api/upload",
        files=[("files", ("a.pdf", pdf, "application/pdf"))],
    )
    assert r.status_code == 200
    info = r.json()["files"][0]
    assert info["size_bytes"] == len(pdf)
