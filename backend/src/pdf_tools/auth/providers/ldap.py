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
        """Timeout e referrals (`LDAP_TIMEOUT`, `LDAP_OPT_REFERRALS`).

        `receive_timeout` deve ser inteiro: o ldap3 usa `struct.pack('LL', ...)` em Unix e
        falha com `struct.error` se for float (ex.: vindo de `float("5")`).
        """
        return {
            "receive_timeout": int(self._s.ldap_receive_timeout),
            "auto_referrals": self._s.ldap_auto_referrals,
            "version": 3,
        }

    @staticmethod
    def _short_login(raw: str) -> str:
        """Login curto para `sAMAccountName` etc.: parte antes de `@` se vier estilo e-mail."""
        u = raw.strip()
        if "@" in u:
            return u.split("@", 1)[0].strip()
        return u

    def _upn_login(self, raw: str) -> str:
        """UPN para filtros com `userPrincipalName`: usa domínio do env se o usuário não informou `@`."""
        u = raw.strip()
        short = self._short_login(raw)
        if "@" in u:
            return u
        if self._s.ldap_domain:
            return f"{short}@{self._s.ldap_domain}"
        return short

    def _build_filter(self, raw_username: str) -> str:
        """Substitui placeholders; `%(username)s` é sempre o login curto (ex.: sAMAccountName no AD)."""
        short = escape_filter_chars(self._short_login(raw_username))
        upn = escape_filter_chars(self._upn_login(raw_username))
        t = self._s.ldap_user_filter
        t = t.replace("%(username)s", short)
        t = t.replace("%(upn)s", upn)
        t = t.replace("%(user_principal_name)s", upn)
        return t

    def authenticate(self, username: str, password: str) -> AuthResult:
        u = username.strip()
        if not u or not password:
            raise LdapInvalidCredentials

        if self._s.ldap_auth_mode == "upn":
            return self._authenticate_upn(username, password)

        short = self._short_login(username)

        server = self._server()
        common = self._conn_common()

        search_filter = self._build_filter(username)

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
            logger.warning(
                "LDAP search retornou 0 entradas (filtro=%s, base=%s). "
                "Em Active Directory a busca anônima costuma ser bloqueada: configure "
                "LDAP_BIND_DN + LDAP_BIND_PASSWORD, ou use LDAP_AUTH_MODE=upn com LDAP_DOMAIN.",
                search_filter,
                self._s.ldap_user_base_dn,
            )
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

        return AuthResult(subject=short, provider_id="ldap")

    def _authenticate_upn(self, username: str, password: str) -> AuthResult:
        """Bind direto como `login@dominio` (UPN), sem busca — típico quando não há conta de serviço."""
        short = self._short_login(username)
        if not short or not password:
            raise LdapInvalidCredentials

        upn = f"{short}@{self._s.ldap_domain}"
        server = self._server()
        common = self._conn_common()

        try:
            conn = Connection(
                server,
                user=upn,
                password=password,
                auto_bind=False,
                **common,
            )
            conn.open()
            if self._s.ldap_start_tls and not self._s.ldap_use_ssl:
                if not conn.start_tls():
                    logger.warning("LDAP STARTTLS não foi aceito pelo servidor")
                    raise LdapServiceUnavailable
            if not conn.bind():
                try:
                    conn.unbind()
                except LDAPException:
                    pass
                raise LdapInvalidCredentials
            conn.unbind()
        except LdapInvalidCredentials:
            raise
        except LdapServiceUnavailable:
            raise
        except (LDAPSocketOpenError, LDAPException) as e:
            logger.exception("Falha no bind UPN LDAP: %s", e)
            raise LdapServiceUnavailable from e

        return AuthResult(subject=short, provider_id="ldap")
