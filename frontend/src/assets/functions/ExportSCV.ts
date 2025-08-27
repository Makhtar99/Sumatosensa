import { saveAs } from 'file-saver';

export function exportToCSV(dataset: Record<string, unknown>[], name: string) {
  if (!dataset.length) return
  const csv = [
    Object.keys(dataset[0]).join(','),
    ...dataset.map(row => Object.values(row).join(','))
  ].join('\n')

  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8' })
  saveAs(blob, `${name}.csv`)
}
