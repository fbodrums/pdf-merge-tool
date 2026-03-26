# Copyright (C) 2026 Fabio Rafael Belliny
#
# SPDX-License-Identifier: GPL-3.0-only

"""Criação e validação de JWT de sessão."""

from __future__ import annotations

import time
from typing import Any

import jwt

from pdf_tools.auth.settings import AuthSettings


def create_access_token(
    *,
    subject: str,
    provider: str,
    settings: AuthSettings,
) -> str:
    now = int(time.time())
    exp = now + settings.jwt_expire_minutes * 60
    payload: dict[str, Any] = {
        "sub": subject,
        "provider": provider,
        "iat": now,
        "exp": exp,
    }
    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str, settings: AuthSettings) -> dict[str, Any]:
    return jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[settings.jwt_algorithm],
    )
