import { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'

import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'

type Props = {
  onFilesSelected: (files: File[]) => void
  disabled?: boolean
}

export function UploadZone({ onFilesSelected, disabled }: Props) {
  const onDrop = useCallback(
    (accepted: File[]) => {
      const pdfs = accepted.filter(
        (f) => f.type === 'application/pdf' || f.name.toLowerCase().endsWith('.pdf'),
      )
      if (pdfs.length < accepted.length) {
        /* toast handled by parent if needed */
      }
      if (pdfs.length) onFilesSelected(pdfs)
    },
    [onFilesSelected],
  )

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'application/pdf': ['.pdf'] },
    disabled,
    multiple: true,
  })

  return (
    <div
      {...getRootProps()}
      className={cn(
        'flex cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed border-[hsl(var(--border))] bg-[hsl(var(--muted))]/30 px-6 py-12 text-center transition-colors',
        isDragActive && 'border-[hsl(var(--primary))] bg-[hsl(var(--primary))]/5',
        disabled && 'pointer-events-none opacity-50',
      )}
    >
      <input {...getInputProps()} />
      <p className="text-sm font-medium text-[hsl(var(--foreground))]">
        {isDragActive ? 'Solte os PDFs aqui' : 'Arraste PDFs ou clique para selecionar'}
      </p>
      <p className="mt-2 text-xs text-[hsl(var(--muted-foreground))]">
        Apenas arquivos .pdf — múltiplos permitidos
      </p>
      <Button type="button" variant="outline" className="mt-4" disabled={disabled}>
        Escolher arquivos
      </Button>
    </div>
  )
}
