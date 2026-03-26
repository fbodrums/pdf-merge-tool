"""Testes de autenticação opcional e rotas /api/auth/*."""

from __future__ import annotations

import importlib
import os
from unittest.mock import patch

import jwt
import pytest
from fastapi.testclient import TestClient

from pdf_tools.auth.settings import AuthSettings


@pytest.fixture
def client_no_auth(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.delenv("AUTH_ENABLED", raising=False)
    monkeypatch.setenv("AUTH_ENABLED", "false")
    import pdf_tools.main as main_mod

    importlib.reload(main_mod)
    return TestClient(main_mod.app)


@pytest.fixture
def client_auth_enabled(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setenv("AUTH_ENABLED", "true")
    monkeypatch.setenv("AUTH_PROVIDER", "ldap")
    monkeypatch.setenv("AUTH_JWT_SECRET", "test-secret-key-for-jwt-signing-only")
    monkeypatch.setenv("LDAP_HOST", "127.0.0.1")
    monkeypatch.setenv("LDAP_PORT", "1389")
    monkeypatch.setenv("LDAP_USER_BASE_DN", "dc=test,dc=local")
    monkeypatch.setenv("LDAP_USER_FILTER", "(uid=%(username)s)")
    import pdf_tools.main as main_mod

    importlib.reload(main_mod)
    return TestClient(main_mod.app)


def test_auth_config_when_disabled(client_no_auth: TestClient) -> None:
    r = client_no_auth.get("/api/auth/config")
    assert r.status_code == 200
    assert r.json() == {"auth_required": False, "provider": None}


def test_auth_me_when_disabled(client_no_auth: TestClient) -> None:
    r = client_no_auth.get("/api/auth/me")
    assert r.status_code == 200
    assert r.json()["sub"] is None


def test_upload_without_token_when_auth_enabled(client_auth_enabled: TestClient) -> None:
    from io import BytesIO

    from pypdf import PdfWriter

    w = PdfWriter()
    w.add_blank_page(width=612, height=792)
    buf = BytesIO()
    w.write(buf)
    pdf = buf.getvalue()

    r = client_auth_enabled.post(
        "/api/upload",
        files=[("files", ("a.pdf", pdf, "application/pdf"))],
    )
    assert r.status_code == 401


def test_login_and_upload_with_mock_ldap(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("AUTH_ENABLED", "true")
    monkeypatch.setenv("AUTH_PROVIDER", "ldap")
    monkeypatch.setenv("AUTH_JWT_SECRET", "test-secret-key-for-jwt-signing-only")
    monkeypatch.setenv("LDAP_HOST", "127.0.0.1")
    monkeypatch.setenv("LDAP_PORT", "1389")
    monkeypatch.setenv("LDAP_USER_BASE_DN", "dc=test,dc=local")
    monkeypatch.setenv("LDAP_USER_FILTER", "(uid=%(username)s)")

    from pdf_tools.auth.providers.base import AuthResult

    with patch(
        "pdf_tools.auth.providers.ldap.LdapAuthProvider.authenticate",
        return_value=AuthResult(subject="alice", provider_id="ldap"),
    ):
        import pdf_tools.main as main_mod

        importlib.reload(main_mod)
        c = TestClient(main_mod.app)

        r = c.post(
            "/api/auth/login",
            json={"username": "alice", "password": "secret"},
        )
        assert r.status_code == 204, r.text
        cookie = r.cookies.get("pdf_tools_auth")
        assert cookie

        from io import BytesIO

        from pypdf import PdfWriter

        w = PdfWriter()
        w.add_blank_page(width=612, height=792)
        buf = BytesIO()
        w.write(buf)
        pdf = buf.getvalue()

        up = c.post(
            "/api/upload",
            files=[("files", ("a.pdf", pdf, "application/pdf"))],
            cookies={"pdf_tools_auth": cookie},
        )
        assert up.status_code == 200, up.text


def test_jwt_roundtrip_for_me(client_auth_enabled: TestClient) -> None:
    import time

    s = AuthSettings.from_env()
    now = int(time.time())
    token = jwt.encode(
        {"sub": "bob", "provider": "ldap", "iat": now, "exp": now + 3600},
        s.jwt_secret,
        algorithm=s.jwt_algorithm,
    )
    r = client_auth_enabled.get(
        "/api/auth/me",
        cookies={s.cookie_name: token},
    )
    assert r.status_code == 200
    assert r.json()["sub"] == "bob"
    assert r.json()["provider"] == "ldap"
