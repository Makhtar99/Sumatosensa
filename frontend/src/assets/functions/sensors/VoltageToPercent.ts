export function voltageToPercent(voltage?: number): number {
  if (typeof voltage !== 'number') return 0
  const pct = Math.round(((voltage - 2.5) / (3.0 - 2.5)) * 100)
  return Math.max(0, Math.min(100, pct))
}