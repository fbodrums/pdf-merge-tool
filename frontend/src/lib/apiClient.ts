/**
 * Copyright (C) 2026 Fabio Rafael Belliny
 *
 * SPDX-License-Identifier: GPL-3.0-only
 */

import { apiUrl } from '@/lib/apiBase'

/** Fetch à API com cookies (sessão JWT em cookie HTTP-only). */
export function apiFetch(path: string, init?: RequestInit): Promise<Response> {
  const p = path.startsWith('/') ? path.slice(1) : path
  return fetch(apiUrl(p), { ...init, credentials: 'include' })
}
