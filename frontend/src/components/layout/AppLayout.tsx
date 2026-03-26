import type { ReactNode } from 'react'

type AppLayoutProps = {
  title: string
  description?: string
  /** Ações à direita do título (ex.: changelog), alinhadas ao shell responsivo */
  headerActions?: ReactNode
  children: ReactNode
}

export function AppLayout({ title, description, headerActions, children }: AppLayoutProps) {
  return (
    <div className="flex min-h-screen flex-col">
      <header className="border-b border-[hsl(var(--border))] bg-[hsl(var(--card))]">
        <div className="mx-auto flex max-w-6xl flex-col gap-3 px-4 py-6 sm:flex-row sm:items-center sm:justify-between sm:gap-4">
          <div className="min-w-0">
            <h1 className="text-2xl font-semibold tracking-tight">{title}</h1>
            {description ? (
              <p className="text-sm text-[hsl(var(--muted-foreground))]">{description}</p>
            ) : null}
          </div>
          {headerActions ? (
            <div className="flex shrink-0 flex-wrap items-center gap-2 sm:justify-end">{headerActions}</div>
          ) : null}
        </div>
      </header>

      <main className="mx-auto flex w-full max-w-6xl flex-1 flex-col gap-8 px-4 py-8 lg:flex-row lg:items-start">
        {children}
      </main>

      <footer className="border-t border-[hsl(var(--border))] py-6 text-center text-xs text-[hsl(var(--muted-foreground))]">
        Processamento no servidor — arquivos não são armazenados permanentemente.
      </footer>
    </div>
  )
}
