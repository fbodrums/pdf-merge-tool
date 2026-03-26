# Copyright (C) 2026 Fabio Rafael Belliny
#
# SPDX-License-Identifier: GPL-3.0-only

"""Rotas públicas de autenticação e metadados."""

from __future__ import annotations

import logging

import jwt
from fastapi import APIRouter, HTTPException, Request, Response
from pydantic import BaseModel, Field

from pdf_tools.auth.jwt_tokens import create_access_token, decode_access_token
from pdf_tools.auth.providers.ldap import LdapInvalidCredentials, LdapServiceUnavailable
from pdf_tools.auth.providers.registry import get_auth_provider
from pdf_tools.auth.settings import AuthSettings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["auth"])


class AuthConfigResponse(BaseModel):
    auth_required: bool = Field(description="Se a ferramenta exige login")
    provider: str | None = Field(description="Provedor configurado (ex.: ldap)")


class LoginRequest(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class MeResponse(BaseModel):
    sub: str | None = None
    provider: str | None = None


@router.get("/config", response_model=AuthConfigResponse)
def auth_config() -> AuthConfigResponse:
    s = AuthSettings.from_env()
    if not s.enabled:
        return AuthConfigResponse(auth_required=False, provider=None)
    return AuthConfigResponse(auth_required=True, provider=s.provider_id)


@router.get("/me", response_model=MeResponse)
def auth_me(request: Request) -> MeResponse:
    s = AuthSettings.from_env()
    if not s.enabled:
        return MeResponse(sub=None, provider=None)

    raw = request.cookies.get(s.cookie_name) or _bearer(request)
    if not raw:
        raise HTTPException(status_code=401, detail="Não autenticado")

    try:
        payload = decode_access_token(raw, s)
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Sessão inválida ou expirada") from None

    sub = payload.get("sub")
    if not isinstance(sub, str) or not sub:
        raise HTTPException(status_code=401, detail="Sessão inválida")

    provider = payload.get("provider")
    prov = provider if isinstance(provider, str) else None
    return MeResponse(sub=sub, provider=prov)


def _bearer(request: Request) -> str | None:
    h = request.headers.get("Authorization")
    if h and h.lower().startswith("bearer "):
        return h[7:].strip() or None
    return None


@router.post("/login")
def auth_login(body: LoginRequest) -> Response:
    s = AuthSettings.from_env()
    if not s.enabled:
        raise HTTPException(status_code=400, detail="Autenticação desabilitada no servidor")

    try:
        s.validate_for_startup()
    except ValueError as e:
        logger.error("Configuração de auth inválida: %s", e)
        raise HTTPException(status_code=503, detail="Autenticação não configurada corretamente") from e

    provider = get_auth_provider(s)
    try:
        result = provider.authenticate(body.username, body.password)
    except LdapInvalidCredentials:
        raise HTTPException(status_code=401, detail="Credenciais inválidas") from None
    except LdapServiceUnavailable:
        raise HTTPException(
            status_code=503,
            detail="Serviço de autenticação indisponível. Tente novamente mais tarde.",
        ) from None
    except ValueError as e:
        logger.exception("Falha no provedor de auth: %s", e)
        raise HTTPException(status_code=503, detail="Serviço de autenticação indisponível") from e

    token = create_access_token(
        subject=result.subject,
        provider=result.provider_id,
        settings=s,
    )

    response = Response(status_code=204)
    max_age = s.jwt_expire_minutes * 60
    response.set_cookie(
        key=s.cookie_name,
        value=token,
        max_age=max_age,
        httponly=True,
        secure=s.cookie_secure,
        samesite=s.cookie_samesite,  # type: ignore[arg-type]
        path="/",
    )
    return response


@router.post("/logout")
def auth_logout() -> Response:
    s = AuthSettings.from_env()
    response = Response(status_code=204)
    if s.enabled:
        response.delete_cookie(key=s.cookie_name, path="/")
    return response
