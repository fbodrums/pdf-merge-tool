# Copyright (C) 2026 Fabio Rafael Belliny
#
# SPDX-License-Identifier: GPL-3.0-only

"""Provedor LDAP: busca de DN + bind com senha do usuário."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from ldap3 import Connection, Server, SUBTREE
from ldap3.core.exceptions import LDAPException, LDAPSocketOpenError
from ldap3.utils.conv import escape_filter_chars

from pdf_tools.auth.providers.base import AuthProvider, AuthResult

if TYPE_CHECKING:
    from pdf_tools.auth.settings import AuthSettings

logger = logging.getLogger(__name__)


class LdapInvalidCredentials(Exception):
    """Usuário inexistente ou senha incorreta (resposta genérica ao cliente)."""


class LdapServiceUnavailable(Exception):
    """Rede, servidor LDAP indisponível ou configuração inconsistente."""


class LdapAuthProvider(AuthProvider):
    def __init__(self, settings: AuthSettings) -> None:
        self._s = settings

    def _server(self) -> Server:
        return Server(
            self._s.ldap_host,
            port=self._s.ldap_port,
            use_ssl=self._s.ldap_use_ssl,
            connect_timeout=self._s.ldap_connect_timeout,
        )

    def _conn_common(self) -> dict:
        """Opções alinhadas a LDAP_TIMEOUT / LDAP_OPT_REFERRALS (Laravel)."""
        return {
            "receive_timeout": self._s.ldap_receive_timeout,
            "auto_referrals": self._s.ldap_auto_referrals,
            "version": 3,
        }

    def _effective_username(self, username: str) -> str:
        """Valor usado no filtro LDAP e como `sub` na sessão.

        Se `LDAP_DOMAIN` estiver definido e o login não contiver `@`,
        concatena `@domínio` (útil para filtros com userPrincipalName no AD).
        """
        u = username.strip()
        if not self._s.ldap_domain:
            return u
        if "@" in u:
            return u
        return f"{u}@{self._s.ldap_domain}"

    def _build_filter(self, username_for_filter: str) -> str:
        safe = escape_filter_chars(username_for_filter)
        return self._s.ldap_user_filter.replace("%(username)s", safe)

    def authenticate(self, username: str, password: str) -> AuthResult:
        u = username.strip()
        if not u or not password:
            raise LdapInvalidCredentials

        effective = self._effective_username(username)

        server = self._server()
        common = self._conn_common()

        search_filter = self._build_filter(effective)

        try:
            if self._s.ldap_bind_dn:
                conn = Connection(
                    server,
                    user=self._s.ldap_bind_dn,
                    password=self._s.ldap_bind_password or None,
                    auto_bind=True,
                    **common,
                )
            else:
                conn = Connection(server, auto_bind=True, **common)

            if self._s.ldap_start_tls and not self._s.ldap_use_ssl:
                if not conn.start_tls():
                    logger.warning("LDAP STARTTLS não foi aceito pelo servidor")
                    raise LdapServiceUnavailable

            conn.search(
                search_base=self._s.ldap_user_base_dn,
                search_filter=search_filter,
                search_scope=SUBTREE,
                attributes=["1.1"],
                size_limit=2,
            )
        except (LDAPSocketOpenError, LDAPException) as e:
            logger.exception("Falha de conexão ou pesquisa LDAP: %s", e)
            raise LdapServiceUnavailable from e

        if not conn.entries:
            try:
                conn.unbind()
            except LDAPException:
                pass
            raise LdapInvalidCredentials

        if len(conn.entries) > 1:
            logger.error("Filtro LDAP retornou mais de uma entrada para o usuário")
            try:
                conn.unbind()
            except LDAPException:
                pass
            raise LdapServiceUnavailable

        user_dn = str(conn.entries[0].entry_dn)
        try:
            conn.unbind()
        except LDAPException:
            pass

        try:
            user_conn = Connection(
                server,
                user=user_dn,
                password=password,
                auto_bind=False,
                **common,
            )
            if self._s.ldap_start_tls and not self._s.ldap_use_ssl:
                if not user_conn.start_tls():
                    logger.warning("LDAP STARTTLS (bind usuário) falhou")
                    raise LdapServiceUnavailable
            if not user_conn.bind():
                try:
                    user_conn.unbind()
                except LDAPException:
                    pass
                raise LdapInvalidCredentials
            user_conn.unbind()
        except LdapInvalidCredentials:
            raise
        except LdapServiceUnavailable:
            raise
        except LDAPSocketOpenError as e:
            logger.exception("Falha de rede no bind do usuário: %s", e)
            raise LdapServiceUnavailable from e
        except LDAPException as e:
            logger.exception("Erro LDAP no bind do usuário: %s", e)
            raise LdapServiceUnavailable from e

        return AuthResult(subject=effective, provider_id="ldap")
