# Copyright (C) 2026 Fabio Rafael Belliny
#
# SPDX-License-Identifier: GPL-3.0-only

"""Configuração de autenticação a partir do ambiente."""

from __future__ import annotations

import os
from dataclasses import dataclass


def _env_bool(key: str, default: bool = False) -> bool:
    raw = os.environ.get(key)
    if raw is None:
        return default
    return raw.strip().lower() in ("1", "true", "yes", "on")


def _first_nonempty(*keys: str) -> str:
    """Lê a primeira variável de ambiente definida e não vazia (aliases tipo Laravel)."""
    for key in keys:
        raw = os.environ.get(key)
        if raw is not None and str(raw).strip():
            return str(raw).strip()
    return ""


def _normalize_ldap_domain(raw: str) -> str:
    """Aceita `spotsul.local` ou `@spotsul.local` (como no Laravel)."""
    t = raw.strip()
    if t.startswith("@"):
        return t[1:].strip()
    return t


@dataclass(frozen=True)
class AuthSettings:
    """Parâmetros de auth + LDAP. Quando `enabled` é falso, demais campos podem estar vazios."""

    enabled: bool
    provider_id: str
    jwt_secret: str
    jwt_expire_minutes: int
    jwt_algorithm: str
    cookie_name: str
    cookie_secure: bool
    cookie_samesite: str
    ldap_host: str
    ldap_port: int
    ldap_domain: str
    ldap_bind_dn: str
    ldap_bind_password: str
    ldap_user_base_dn: str
    ldap_user_filter: str
    ldap_start_tls: bool
    ldap_use_ssl: bool
    ldap_connect_timeout: float
    ldap_receive_timeout: float
    ldap_auto_referrals: bool

    @staticmethod
    def from_env() -> AuthSettings:
        enabled = _env_bool("AUTH_ENABLED", False)
        provider_id = os.environ.get("AUTH_PROVIDER", "ldap").strip().lower() or "ldap"
        jwt_secret = os.environ.get("AUTH_JWT_SECRET", "").strip()
        jwt_expire = int(os.environ.get("AUTH_JWT_EXPIRE_MINUTES", "480"))
        jwt_algorithm = os.environ.get("AUTH_JWT_ALGORITHM", "HS256").strip() or "HS256"
        cookie_name = os.environ.get("AUTH_COOKIE_NAME", "pdf_tools_auth").strip() or "pdf_tools_auth"
        cookie_secure = _env_bool("AUTH_COOKIE_SECURE", False)
        samesite = os.environ.get("AUTH_COOKIE_SAMESITE", "lax").strip().lower() or "lax"
        if samesite not in ("lax", "strict", "none"):
            samesite = "lax"

        ldap_host = _first_nonempty("LDAP_HOST", "LDAP_HOSTNAME")
        ldap_domain = _normalize_ldap_domain(_first_nonempty("LDAP_DOMAIN"))
        ldap_bind_dn = _first_nonempty("LDAP_BIND_DN")
        ldap_bind_password = _first_nonempty("LDAP_BIND_PASSWORD")
        ldap_user_base_dn = _first_nonempty("LDAP_USER_BASE_DN", "LDAP_BASE_DN")
        ldap_user_filter = _first_nonempty("LDAP_USER_FILTER")

        # SSL/TLS: nomes deste projeto ou os mesmos do Laravel (LDAP_SSL / LDAP_TLS)
        ldap_use_ssl = _env_bool("LDAP_USE_SSL", False) or _env_bool("LDAP_SSL", False)
        if os.environ.get("LDAP_START_TLS") is not None:
            ldap_start_tls = _env_bool("LDAP_START_TLS", False)
        elif os.environ.get("LDAP_TLS") is not None:
            ldap_start_tls = _env_bool("LDAP_TLS", False)
        else:
            ldap_start_tls = False

        port_raw = os.environ.get("LDAP_PORT", "").strip()
        if port_raw:
            ldap_port = int(port_raw)
        else:
            ldap_port = 636 if ldap_use_ssl else 389

        # Laravel: LDAP_TIMEOUT=5, LDAP_OPT_REFERRALS=0 → não seguir referrals
        try:
            ldap_connect_timeout = float(os.environ.get("LDAP_TIMEOUT", "5").strip() or "5")
        except ValueError:
            ldap_connect_timeout = 5.0
        ldap_receive_timeout = ldap_connect_timeout

        opt_ref = os.environ.get("LDAP_OPT_REFERRALS")
        if opt_ref is not None:
            ldap_auto_referrals = opt_ref.strip() not in ("0", "", "false", "False", "no")
        else:
            ldap_auto_referrals = _env_bool("LDAP_REFERRALS", False)

        return AuthSettings(
            enabled=enabled,
            provider_id=provider_id,
            jwt_secret=jwt_secret,
            jwt_expire_minutes=max(1, jwt_expire),
            jwt_algorithm=jwt_algorithm,
            cookie_name=cookie_name,
            cookie_secure=cookie_secure,
            cookie_samesite=samesite,
            ldap_host=ldap_host,
            ldap_port=ldap_port,
            ldap_domain=ldap_domain,
            ldap_bind_dn=ldap_bind_dn,
            ldap_bind_password=ldap_bind_password,
            ldap_user_base_dn=ldap_user_base_dn,
            ldap_user_filter=ldap_user_filter,
            ldap_start_tls=ldap_start_tls,
            ldap_use_ssl=ldap_use_ssl,
            ldap_connect_timeout=ldap_connect_timeout,
            ldap_receive_timeout=ldap_receive_timeout,
            ldap_auto_referrals=ldap_auto_referrals,
        )

    def validate_for_startup(self) -> None:
        """Levanta ValueError se auth habilitada e configuração mínima ausente."""
        if not self.enabled:
            return
        if not self.jwt_secret:
            raise ValueError("AUTH_JWT_SECRET é obrigatório quando AUTH_ENABLED=true")
        if self.provider_id == "ldap":
            if not self.ldap_host:
                raise ValueError(
                    "LDAP_HOST ou LDAP_HOSTNAME é obrigatório quando AUTH_ENABLED=true e AUTH_PROVIDER=ldap",
                )
            if not self.ldap_user_base_dn:
                raise ValueError(
                    "LDAP_USER_BASE_DN ou LDAP_BASE_DN é obrigatório quando AUTH_ENABLED=true e AUTH_PROVIDER=ldap",
                )
            if not self.ldap_user_filter or "%(username)s" not in self.ldap_user_filter:
                raise ValueError(
                    "LDAP_USER_FILTER deve conter o placeholder %(username)s quando AUTH_PROVIDER=ldap",
                )
        else:
            raise ValueError(f"Provedor de autenticação não suportado: {self.provider_id!r}")
