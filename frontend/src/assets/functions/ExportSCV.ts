import { saveAs } from 'file-saver';
import * as XLSX from 'xlsx';

export function exportToCSV(dataset: any[], name: string) {
  if (!dataset.length) return
  const csv = [
    Object.keys(dataset[0]).join(','),
    ...dataset.map(row => Object.values(row).join(','))
  ].join('\n')

  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8' })
  saveAs(blob, `${name}.csv`)
}
