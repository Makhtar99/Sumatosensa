import { saveAs } from 'file-saver';
import * as XLSX from 'xlsx';

export function exportToExcel(dataset: Record<string, unknown>[], name: string) {
  const worksheet = XLSX.utils.json_to_sheet(dataset)
  const workbook = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(workbook, worksheet, 'Sheet1')
  const blob = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' })
  saveAs(new Blob([blob]), `${name}.xlsx`)
}