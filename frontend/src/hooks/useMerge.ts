import { useCallback, useState } from 'react'

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

  const merge = useCallback(async (payload: MergePayload): Promise<Blob> => {
    setLoading(true)
    try {
      const res = await fetch('/api/merge', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })
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
      setLoading(false)
    }
  }, [])

  return { merge, loading }
}
