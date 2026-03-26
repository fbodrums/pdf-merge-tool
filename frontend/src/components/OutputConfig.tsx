import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

type Props = {
  value: string
  onChange: (v: string) => void
  disabled?: boolean
}

export function OutputConfig({ value, onChange, disabled }: Props) {
  return (
    <Card>
      <CardHeader className="pb-3">
        <CardTitle className="text-base">Arquivo de saída</CardTitle>
      </CardHeader>
      <CardContent className="space-y-2 pt-0">
        <Label htmlFor="output-name">Nome do arquivo final</Label>
        <Input
          id="output-name"
          disabled={disabled}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder="merged.pdf"
        />
        <p className="text-xs text-[hsl(var(--muted-foreground))]">
          A extensão .pdf é adicionada automaticamente se faltar.
        </p>
      </CardContent>
    </Card>
  )
}
