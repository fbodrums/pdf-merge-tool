# Copyright (C) 2026 Fabio Rafael Belliny
#
# SPDX-License-Identifier: GPL-3.0-only

"""Dependências FastAPI para validar sessão."""

from __future__ import annotations

import logging

import jwt
from fastapi import HTTPException, Request

from pdf_tools.auth.jwt_tokens import decode_access_token
from pdf_tools.auth.session_user import OPEN_SESSION, SessionUser
from pdf_tools.auth.settings import AuthSettings

logger = logging.getLogger(__name__)


def _bearer_token(request: Request) -> str | None:
    h = request.headers.get("Authorization")
    if h and h.lower().startswith("bearer "):
        return h[7:].strip() or None
    return None


def require_session_user(request: Request) -> SessionUser:
    """Exige JWT válido quando AUTH_ENABLED=true; caso contrário retorna sessão aberta."""
    settings = AuthSettings.from_env()
    if not settings.enabled:
        return OPEN_SESSION

    raw = request.cookies.get(settings.cookie_name) or _bearer_token(request)
    if not raw:
        raise HTTPException(status_code=401, detail="Não autenticado")

    try:
        payload = decode_access_token(raw, settings)
    except jwt.PyJWTError as e:
        logger.debug("JWT inválido: %s", e)
        raise HTTPException(status_code=401, detail="Sessão inválida ou expirada") from e

    sub = payload.get("sub")
    if not isinstance(sub, str) or not sub:
        raise HTTPException(status_code=401, detail="Sessão inválida")

    provider = payload.get("provider")
    prov = provider if isinstance(provider, str) else None
    return SessionUser(sub=sub, provider=prov)
