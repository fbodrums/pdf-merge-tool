import { Loader2 } from 'lucide-react'

import { Button } from '@/components/ui/button'

type Props = {
  onClick: () => void
  loading: boolean
  disabled?: boolean
}

export function MergeButton({ onClick, loading, disabled }: Props) {
  return (
    <Button
      type="button"
      size="lg"
      className="w-full sm:w-auto"
      onClick={onClick}
      disabled={disabled || loading}
    >
      {loading ? (
        <>
          <Loader2 className="h-4 w-4 animate-spin" />
          Gerando PDF…
        </>
      ) : (
        'Gerar PDF'
      )}
    </Button>
  )
}
