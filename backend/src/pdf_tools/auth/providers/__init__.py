# Copyright (C) 2026 Fabio Rafael Belliny
#
# SPDX-License-Identifier: GPL-3.0-only

from pdf_tools.auth.providers.base import AuthProvider, AuthResult
from pdf_tools.auth.providers.registry import get_auth_provider

__all__ = ["AuthProvider", "AuthResult", "get_auth_provider"]
