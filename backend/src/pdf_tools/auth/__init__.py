# Copyright (C) 2026 Fabio Rafael Belliny
#
# SPDX-License-Identifier: GPL-3.0-only

"""Autenticação opcional com provedores plugáveis (LDAP na primeira versão)."""

from pdf_tools.auth.dependencies import require_session_user
from pdf_tools.auth.routes import router as auth_router
from pdf_tools.auth.session_user import SessionUser
from pdf_tools.auth.settings import AuthSettings

__all__ = ["AuthSettings", "SessionUser", "auth_router", "require_session_user"]
