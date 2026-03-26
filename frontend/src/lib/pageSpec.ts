export function validatePageSpec(raw: string): string | null {
  const s = raw.trim()
  if (!s) return null
  const parts = s.split(',')
  for (const part of parts) {
    const p = part.trim()
    if (!p) return 'Remova vírgulas duplicadas ou espaços inválidos.'
    const range = /^(\d+)\s*-\s*(\d+)$/.exec(p)
    if (range) {
      const a = Number(range[1])
      const b = Number(range[2])
      if (a > b) return 'Intervalo inválido: o início deve ser menor ou igual ao fim.'
      continue
    }
    if (!/^\d+$/.test(p)) return `Trecho inválido: ${p}`
  }
  return null
}

export function isPageSpecValid(value: string): boolean {
  return validatePageSpec(value) === null
}
