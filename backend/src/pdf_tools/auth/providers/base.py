# Copyright (C) 2026 Fabio Rafael Belliny
#
# SPDX-License-Identifier: GPL-3.0-only

"""Contrato comum para provedores de autenticação."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class AuthResult:
    """Identidade autenticada exposta na sessão (claim `sub`)."""

    subject: str
    provider_id: str


class AuthProvider(ABC):
    """Implementação de um modo de login (LDAP, OIDC futuro, etc.)."""

    @abstractmethod
    def authenticate(self, username: str, password: str) -> AuthResult:
        """Valida credenciais ou levanta exceção."""
