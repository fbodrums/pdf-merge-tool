/**
 * Prefixo da app (Vite `base`), sempre com barra final.
 * Usar em chamadas à API quando a UI roda em subpath (ex.: /pdf-merge-tools/).
 */
export function apiUrl(path: string): string {
  const p = path.startsWith('/') ? path.slice(1) : path
  return `${import.meta.env.BASE_URL}${p}`
}
