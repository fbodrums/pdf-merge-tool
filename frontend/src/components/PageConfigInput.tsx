import { useMemo } from 'react'

import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { validatePageSpec } from '@/lib/pageSpec'
import { cn } from '@/lib/utils'

type Props = {
  value: string
  onChange: (v: string) => void
  disabled?: boolean
  id?: string
  label?: string
}

export function PageConfigInput({
  value,
  onChange,
  disabled,
  id,
  label = 'Páginas a extrair',
}: Props) {
  const error = useMemo(() => validatePageSpec(value), [value])

  return (
    <div className="flex min-w-0 flex-1 flex-col gap-2">
      {id ? (
        <Label htmlFor={id} className={cn(disabled && 'opacity-70')}>
          {label}
        </Label>
      ) : null}
      <Input
        id={id}
        disabled={disabled}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="1,2 ou 1-3 ou 1,3-5"
        className={cn(error && 'border-[hsl(var(--destructive))]')}
        aria-invalid={Boolean(error)}
      />
      {error ? (
        <p className="text-xs text-[hsl(var(--destructive))]">{error}</p>
      ) : (
        <p className="text-xs text-[hsl(var(--muted-foreground))]">
          Vazio = páginas 1 e 2 (padrão)
        </p>
      )}
    </div>
  )
}
