# Copyright (C) 2026 Fabio Rafael Belliny
#
# SPDX-License-Identifier: GPL-3.0-only

"""Registro de fábricas de provedores por id."""

from __future__ import annotations

from typing import Callable

from pdf_tools.auth.providers.base import AuthProvider
from pdf_tools.auth.providers.ldap import LdapAuthProvider
from pdf_tools.auth.settings import AuthSettings

ProviderFactory = Callable[[AuthSettings], AuthProvider]

_REGISTRY: dict[str, ProviderFactory] = {
    "ldap": lambda s: LdapAuthProvider(s),
}


def get_auth_provider(settings: AuthSettings) -> AuthProvider:
    factory = _REGISTRY.get(settings.provider_id)
    if factory is None:
        raise ValueError(f"Provedor de autenticação não suportado: {settings.provider_id!r}")
    return factory(settings)
