/**
 * Copyright (C) 2026 Fabio Rafael Belliny
 *
 * SPDX-License-Identifier: GPL-3.0-only
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, version 3 of the License.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see https://www.gnu.org/licenses/.
 */

import { useCallback, useEffect, useRef, useState } from 'react'
import { toast } from 'sonner'

import { ChangelogSheet } from '@/components/ChangelogSheet'
import { FileList, type FileRow } from '@/components/FileList'
import { AppLayout } from '@/components/layout/AppLayout'
import { MergeButton } from '@/components/MergeButton'
import { OutputConfig } from '@/components/OutputConfig'
import { UploadZone } from '@/components/UploadZone'
import { WizardStepper } from '@/components/WizardStepper'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Progress } from '@/components/ui/progress'
import { Separator } from '@/components/ui/separator'
import { useMerge } from '@/hooks/useMerge'
import { useUpload } from '@/hooks/useUpload'
import { isPageSpecValid } from '@/lib/pageSpec'
import type { WizardStep } from '@/lib/wizardSteps'

function normalizeOutputName(name: string): string {
  const t = name.trim() || 'merged.pdf'
  return t.toLowerCase().endsWith('.pdf') ? t : `${t}.pdf`
}

export default function App() {
  const [wizardStep, setWizardStep] = useState<WizardStep>('select')
  const [pendingFiles, setPendingFiles] = useState<File[]>([])
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [rows, setRows] = useState<FileRow[]>([])
  const [outputName, setOutputName] = useState('merged.pdf')
  const [unlockPwd, setUnlockPwd] = useState<Record<string, string>>({})
  const [resultBlobUrl, setResultBlobUrl] = useState<string | null>(null)
  const [resultFilename, setResultFilename] = useState('merged.pdf')

  const resultBlobUrlRef = useRef<string | null>(null)
  useEffect(() => {
    resultBlobUrlRef.current = resultBlobUrl
  }, [resultBlobUrl])
  useEffect(() => {
    return () => {
      if (resultBlobUrlRef.current) URL.revokeObjectURL(resultBlobUrlRef.current)
    }
  }, [])

  const { uploadFiles, loading: uploadLoading, uploadProgress } = useUpload()
  const { merge, loading: mergeLoading } = useMerge()

  const busy = uploadLoading || mergeLoading

  const onFilesSelected = useCallback((files: File[]) => {
    setPendingFiles((prev) => [...prev, ...files])
    toast.success(`${files.length} arquivo(s) adicionado(s) à fila.`)
  }, [])

  const handleNextFromSelect = useCallback(async () => {
    if (!pendingFiles.length) {
      toast.error('Adicione ao menos um PDF.')
      return
    }
    setWizardStep('uploading')
    try {
      const res = await uploadFiles(pendingFiles)
      setSessionId(res.session_id)
      setRows(
        res.files.map((f) => ({
          file_id: f.file_id,
          filename: f.filename,
          total_pages: f.total_pages,
          password_protected: f.password_protected,
          pages: '1,2',
        })),
      )
      setPendingFiles([])
      toast.success('PDFs carregados com sucesso.')
      setWizardStep('configure')
    } catch (e) {
      toast.error(e instanceof Error ? e.message : 'Falha no upload.')
      setWizardStep('select')
    }
  }, [pendingFiles, uploadFiles])

  const handleUnlock = async (fileId: string) => {
    const pwd = unlockPwd[fileId]?.trim()
    if (!pwd || !sessionId) {
      toast.error('Informe a senha.')
      return
    }
    try {
      const res = await fetch('/api/unlock', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId, file_id: fileId, password: pwd }),
      })
      const text = await res.text()
      if (!res.ok) {
        let detail = text
        try {
          const j = JSON.parse(text) as { detail?: string }
          if (j.detail) detail = j.detail
        } catch {
          /* ignore */
        }
        throw new Error(detail)
      }
      const data = JSON.parse(text) as { total_pages: number }
      setRows((prev) =>
        prev.map((r) =>
          r.file_id === fileId
            ? {
                ...r,
                password_protected: false,
                total_pages: data.total_pages,
              }
            : r,
        ),
      )
      toast.success('PDF desbloqueado.')
    } catch (e) {
      toast.error(e instanceof Error ? e.message : 'Não foi possível desbloquear.')
    }
  }

  const handleMerge = async () => {
    if (!sessionId || !rows.length) {
      toast.error('Carregue os PDFs antes.')
      return
    }
    if (rows.some((r) => r.password_protected)) {
      toast.error('Desbloqueie os PDFs protegidos antes de gerar.')
      return
    }
    if (rows.some((r) => !isPageSpecValid(r.pages))) {
      toast.error('Corrija a sintaxe das páginas.')
      return
    }
    try {
      const blob = await merge({
        session_id: sessionId,
        items: rows.map((r) => ({
          file_id: r.file_id,
          pages: r.pages.trim() ? r.pages.trim() : null,
        })),
        output_filename: normalizeOutputName(outputName),
      })
      const name = normalizeOutputName(outputName)
      setResultFilename(name)
      setResultBlobUrl((prev) => {
        if (prev) URL.revokeObjectURL(prev)
        return URL.createObjectURL(blob)
      })
      setWizardStep('result')
      toast.success('PDF gerado. Use o botão abaixo para baixar.')
    } catch (e) {
      toast.error(e instanceof Error ? e.message : 'Erro ao mesclar.')
    }
  }

  const handleBackToConfigure = useCallback(() => {
    setResultBlobUrl((prev) => {
      if (prev) URL.revokeObjectURL(prev)
      return null
    })
    setWizardStep('configure')
  }, [])

  const protectedRows = rows.filter((r) => r.password_protected)

  const canMerge =
    !!sessionId &&
    rows.length > 0 &&
    !rows.some((r) => r.password_protected) &&
    !rows.some((r) => !isPageSpecValid(r.pages))

  return (
    <AppLayout
      title="PDF Merge Tool"
      description="Extraia páginas de vários PDFs e gere um único arquivo."
      headerActions={<ChangelogSheet />}
    >
      <div className="mx-auto flex w-full max-w-3xl flex-col gap-6 lg:max-w-3xl">
        <WizardStepper currentStep={wizardStep} />

        {wizardStep === 'select' && (
          <Card>
            <CardHeader>
              <CardTitle>1. Selecionar PDFs</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <UploadZone onFilesSelected={onFilesSelected} disabled={busy} />
              {pendingFiles.length > 0 ? (
                <p className="text-sm text-[hsl(var(--muted-foreground))]">
                  {pendingFiles.length} arquivo(s) na fila. Clique em &quot;Próximo&quot; para enviar ao
                  servidor.
                </p>
              ) : (
                <p className="text-sm text-[hsl(var(--muted-foreground))]">
                  Escolha um ou mais PDFs para continuar.
                </p>
              )}
              <Button
                type="button"
                className="w-full"
                onClick={handleNextFromSelect}
                disabled={busy || !pendingFiles.length}
                aria-label="Avançar para envio dos arquivos ao servidor"
              >
                Próximo
              </Button>
            </CardContent>
          </Card>
        )}

        {wizardStep === 'uploading' && (
          <Card>
            <CardHeader>
              <CardTitle>2. Enviando</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-sm text-[hsl(var(--muted-foreground))]">
                Aguarde enquanto seus arquivos são enviados.
              </p>
              <Progress value={uploadProgress} />
              <p className="text-xs text-[hsl(var(--muted-foreground))]" aria-live="polite">
                {uploadProgress === null
                  ? 'Calculando progresso…'
                  : `Enviado: ${uploadProgress}%`}
              </p>
            </CardContent>
          </Card>
        )}

        {wizardStep === 'configure' && (
          <>
            <OutputConfig value={outputName} onChange={setOutputName} disabled={busy} />

            {protectedRows.length > 0 && sessionId && (
              <Alert variant="warning">
                <AlertTitle>PDFs protegidos</AlertTitle>
                <AlertDescription>
                  Informe a senha para cada arquivo antes de gerar o PDF final.
                </AlertDescription>
                <Separator className="my-2 bg-amber-500/20" />
                <div className="space-y-4">
                  {protectedRows.map((r) => (
                    <Card key={r.file_id}>
                      <CardContent className="flex flex-col gap-3 pt-6 sm:flex-row sm:items-end">
                        <div className="min-w-0 flex-1 space-y-2">
                          <p className="truncate text-sm font-medium">{r.filename}</p>
                          <div className="space-y-2">
                            <Label htmlFor={`unlock-${r.file_id}`}>Senha do PDF</Label>
                            <Input
                              id={`unlock-${r.file_id}`}
                              type="password"
                              placeholder="Senha"
                              value={unlockPwd[r.file_id] ?? ''}
                              onChange={(e) =>
                                setUnlockPwd((prev) => ({ ...prev, [r.file_id]: e.target.value }))
                              }
                            />
                          </div>
                        </div>
                        <Button type="button" onClick={() => handleUnlock(r.file_id)}>
                          Desbloquear
                        </Button>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </Alert>
            )}

            {rows.length > 0 ? (
              <FileList
                rows={rows}
                onReorder={setRows}
                onPagesChange={(id, pages) =>
                  setRows((prev) => prev.map((r) => (r.file_id === id ? { ...r, pages } : r)))
                }
                onRemove={(id) => setRows((prev) => prev.filter((r) => r.file_id !== id))}
                disabled={busy}
              />
            ) : (
              <Card>
                <CardContent className="py-12 text-center text-sm text-[hsl(var(--muted-foreground))]">
                  Nenhum arquivo na sessão. Volte e envie PDFs novamente.
                </CardContent>
              </Card>
            )}

            <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <MergeButton
                onClick={handleMerge}
                loading={mergeLoading}
                disabled={busy || !canMerge}
              />
            </div>
          </>
        )}

        {wizardStep === 'result' && resultBlobUrl && (
          <Card>
            <CardHeader>
              <CardTitle>4. Download</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-sm text-[hsl(var(--muted-foreground))]">
                Seu PDF foi gerado. Baixe o arquivo ou volte para ajustar páginas e gerar de novo.
              </p>
              <div className="flex flex-col gap-3 sm:flex-row sm:flex-wrap">
                <Button type="button" size="lg" className="w-full sm:w-auto" asChild>
                  <a href={resultBlobUrl} download={resultFilename}>
                    Baixar PDF
                  </a>
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  size="lg"
                  className="w-full sm:w-auto"
                  onClick={handleBackToConfigure}
                  disabled={busy}
                  aria-label="Voltar para edição de páginas e ordem dos arquivos"
                >
                  Voltar para edição
                </Button>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </AppLayout>
  )
}
