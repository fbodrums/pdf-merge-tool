/**
 * Copyright (C) 2026 Fabio Rafael Belliny
 *
 * SPDX-License-Identifier: GPL-3.0-only
 */

import { useCallback, useRef, useState } from 'react'

import { apiUrl } from '@/lib/apiBase'

export type UploadedFileInfo = {
  file_id: string
  filename: string
  total_pages: number | null
  size_bytes: number
  password_protected: boolean
}

export type UploadResult = {
  session_id: string
  files: UploadedFileInfo[]
}

/** `null` durante o envio quando o progresso não é computável (barra indeterminada). */
export type UploadProgress = number | null

export function useUpload() {
  const [loading, setLoading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState<UploadProgress>(0)
  const xhrRef = useRef<XMLHttpRequest | null>(null)

  const abortUpload = useCallback(() => {
    xhrRef.current?.abort()
    xhrRef.current = null
    setLoading(false)
    setUploadProgress(0)
  }, [])

  const uploadFiles = useCallback(async (files: File[]): Promise<UploadResult> => {
    xhrRef.current?.abort()
    setLoading(true)
    setUploadProgress(0)
    try {
      const fd = new FormData()
      files.forEach((f) => fd.append('files', f))

      const result = await new Promise<UploadResult>((resolve, reject) => {
        const xhr = new XMLHttpRequest()
        xhrRef.current = xhr
        xhr.open('POST', apiUrl('api/upload'))
        xhr.withCredentials = true
        xhr.responseType = 'text'
        xhr.onload = () => {
          xhrRef.current = null
          if (xhr.status >= 200 && xhr.status < 300) {
            try {
              resolve(JSON.parse(xhr.responseText) as UploadResult)
            } catch {
              reject(new Error('Resposta inválida do servidor'))
            }
          } else {
            let detail = xhr.responseText
            try {
              const j = JSON.parse(xhr.responseText) as { detail?: unknown }
              if (typeof j.detail === 'string') detail = j.detail
            } catch {
              /* ignore */
            }
            reject(new Error(detail || `Erro ${xhr.status}`))
          }
        }
        xhr.onerror = () => {
          xhrRef.current = null
          reject(new Error('Falha de rede ao enviar arquivos'))
        }
        xhr.onabort = () => {
          xhrRef.current = null
          reject(new DOMException('Upload cancelado', 'AbortError'))
        }
        xhr.upload.onprogress = (ev) => {
          if (ev.lengthComputable && ev.total > 0) {
            setUploadProgress(Math.round((ev.loaded / ev.total) * 100))
          } else {
            setUploadProgress(null)
          }
        }
        xhr.send(fd)
      })

      setUploadProgress(100)
      return result
    } finally {
      setLoading(false)
      setUploadProgress(0)
    }
  }, [])

  return { uploadFiles, loading, uploadProgress, abortUpload }
}
