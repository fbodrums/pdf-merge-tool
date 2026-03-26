# Copyright (C) 2026 Fabio Rafael Belliny
#
# SPDX-License-Identifier: GPL-3.0-only

"""Usuário da sessão HTTP (JWT) ou modo aberto quando auth está desligada."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SessionUser:
    sub: str
    provider: str | None = None


OPEN_SESSION = SessionUser(sub="__open__", provider=None)
