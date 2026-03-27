/**
 * Copyright (C) 2026 Fabio Rafael Belliny
 *
 * SPDX-License-Identifier: GPL-3.0-only
 */

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from 'react'

import { apiFetch } from '@/lib/apiClient'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

type AuthConfig = {
  auth_required: boolean
  provider: string | null
}

type MeResponse = {
  sub: string | null
  provider: string | null
}

export type AppAuthContextValue = {
  username: string
  logout: () => Promise<void>
}

const AppAuthContext = createContext<AppAuthContextValue | null>(null)

export function useAppAuth(): AppAuthContextValue | null {
  return useContext(AppAuthContext)
}

export function AuthGate({ children }: { children: ReactNode }) {
  const [loading, setLoading] = useState(true)
  const [config, setConfig] = useState<AuthConfig | null>(null)
  const [username, setUsername] = useState<string | null>(null)
  const [user, setUser] = useState('')
  const [password, setPassword] = useState('')
  const [loginError, setLoginError] = useState<string | null>(null)
  const [loginLoading, setLoginLoading] = useState(false)

  const load = useCallback(async () => {
    setLoading(true)
    try {
      const r = await apiFetch('api/auth/config')
      if (!r.ok) throw new Error('Falha ao carregar configuração de acesso')
      const c = (await r.json()) as AuthConfig
      setConfig(c)
      if (!c.auth_required) {
        setUsername(null)
        setLoading(false)
        return
      }
      const me = await apiFetch('api/auth/me')
      if (me.ok) {
        const body = (await me.json()) as MeResponse
        if (body.sub) {
          setUsername(body.sub)
        } else {
          setUsername(null)
        }
      } else {
        setUsername(null)
      }
    } catch {
      setConfig({ auth_required: false, provider: null })
      setUsername(null)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    void load()
  }, [load])

  const logout = useCallback(async () => {
    await apiFetch('api/auth/logout', { method: 'POST' })
    setUsername(null)
    setUser('')
    setPassword('')
  }, [])

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoginError(null)
    setLoginLoading(true)
    try {
      const r = await apiFetch('api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: user.trim(), password }),
      })
      if (!r.ok) {
        let msg = 'Não foi possível entrar.'
        try {
          const j = (await r.json()) as { detail?: unknown }
          if (typeof j.detail === 'string') msg = j.detail
        } catch {
          if (r.status === 503) msg = 'Serviço de autenticação indisponível. Tente novamente mais tarde.'
        }
        setLoginError(msg)
        return
      }
      setPassword('')
      const me = await apiFetch('api/auth/me')
      if (me.ok) {
        const body = (await me.json()) as MeResponse
        if (body.sub) setUsername(body.sub)
      }
    } catch {
      setLoginError('Falha de rede. Tente novamente.')
    } finally {
      setLoginLoading(false)
    }
  }

  if (loading || !config) {
    return (
      <div className="flex min-h-screen items-center justify-center text-sm text-[hsl(var(--muted-foreground))]">
        Carregando…
      </div>
    )
  }

  if (!config.auth_required) {
    return <>{children}</>
  }

  if (!username) {
    return (
      <div className="flex min-h-screen items-center justify-center p-4">
        <Card className="w-full max-w-md">
          <CardHeader>
            <CardTitle>Entrar</CardTitle>
            <p className="text-sm text-[hsl(var(--muted-foreground))]">
              É necessário fazer login
              {config.provider ? ` (${config.provider})` : ''}.
            </p>
          </CardHeader>
          <CardContent>
            <form className="space-y-4" onSubmit={(e) => void handleLogin(e)}>
              {loginError ? (
                <p className="text-sm text-destructive" role="alert">
                  {loginError}
                </p>
              ) : null}
              <div className="space-y-2">
                <Label htmlFor="auth-user">Usuário</Label>
                <Input
                  id="auth-user"
                  name="username"
                  autoComplete="username"
                  value={user}
                  onChange={(e) => setUser(e.target.value)}
                  disabled={loginLoading}
                  required
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="auth-pass">Senha</Label>
                <Input
                  id="auth-pass"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  disabled={loginLoading}
                  required
                />
              </div>
              <Button type="submit" className="w-full" disabled={loginLoading}>
                {loginLoading ? 'Entrando…' : 'Entrar'}
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <AppAuthContext.Provider value={{ username, logout }}>
      {children}
    </AppAuthContext.Provider>
  )
}
