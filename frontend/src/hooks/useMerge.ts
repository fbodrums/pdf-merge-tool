import { useCallback, useRef, useState } from 'react'

import { apiUrl } from '@/lib/apiBase'

export type MergeItem = {
  file_id: string
  pages?: string | null
}

export type MergePayload = {
  session_id: string
  items: MergeItem[]
  output_filename?: string | null
}

export function useMerge() {
  const [loading, setLoading] = useState(false)
  const abortControllerRef = useRef<AbortController | null>(null)

  const abortMerge = useCallback(() => {
    abortControllerRef.current?.abort()
    abortControllerRef.current = null
    setLoading(false)
  }, [])

  const merge = useCallback(async (payload: MergePayload): Promise<Blob> => {
    abortControllerRef.current?.abort()
    const ac = new AbortController()
    abortControllerRef.current = ac
    setLoading(true)
    try {
      const res = await fetch(apiUrl('api/merge'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
        signal: ac.signal,
        credentials: 'include',
      })
      abortControllerRef.current = null
      if (!res.ok) {
        const text = await res.text()
        let detail = text
        try {
          const j = JSON.parse(text) as { detail?: unknown }
          if (typeof j.detail === 'string') detail = j.detail
        } catch {
          /* ignore */
        }
        throw new Error(detail || `Erro ${res.status}`)
      }
      return res.blob()
    } finally {
      abortControllerRef.current = null
      setLoading(false)
    }
  }, [])

  return { merge, loading, abortMerge }
}
