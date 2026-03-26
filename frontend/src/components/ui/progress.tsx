/**
 * Copyright (C) 2026 Fabio Rafael Belliny
 *
 * SPDX-License-Identifier: GPL-3.0-only
 */

import { cn } from '@/lib/utils'

type ProgressProps = {
  /** 0–100, ou `null` para barra indeterminada */
  value: number | null
  className?: string
}

export function Progress({ value, className }: ProgressProps) {
  const indeterminate = value === null

  return (
    <div
      role="progressbar"
      aria-valuemin={0}
      aria-valuemax={100}
      aria-valuenow={indeterminate ? undefined : value}
      aria-label={indeterminate ? 'Envio em andamento' : `Envio ${value}% concluído`}
      className={cn(
        'relative h-2 w-full overflow-hidden rounded-full bg-[hsl(var(--muted))]',
        className,
      )}
    >
      {indeterminate ? (
        <div
          className="absolute inset-y-0 left-0 w-[40%] rounded-full bg-[hsl(var(--primary))]"
          style={{
            animation: 'progress-indeterminate 1.2s ease-in-out infinite',
          }}
        />
      ) : (
        <div
          className="h-full rounded-full bg-[hsl(var(--primary))] transition-[width] duration-150 ease-out"
          style={{ width: `${Math.min(100, Math.max(0, value))}%` }}
        />
      )}
    </div>
  )
}
