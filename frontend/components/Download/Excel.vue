<script setup lang="ts">
const props = defineProps<{
  columns: {
    header: string,
    key: string,
    width?: number
  }[],
  rows: any[],
  filename: string
}>()
import * as Excel from "exceljs";


const filename = computed (() => {
  return `${props.filename}.xlsx`
})
async function downloadExcel() {
  const workbook = new Excel.Workbook()
  // workbook.addImage()
  // Sheet
  const worksheet = workbook.addWorksheet('1')

  // Header
  worksheet.columns = props.columns
  props.rows.forEach((row) => {
    worksheet.addRow(row)
  })
  // workbook to Blob
  const uint8Array = await workbook.xlsx.writeBuffer()
  const blob = new Blob([uint8Array], {type: 'application/octet-binary'})

  // Download
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  document.body.appendChild(a)
  a.download = filename.value
  a.href = url
  a.click()
  a.remove()
  URL.revokeObjectURL(url)
}
</script>

<template>
  <UButton @click="downloadExcel" :disabled="!rows.length" icon="i-heroicons-document-chart-bar">
    <slot>Скачать Excel</slot>
  </UButton>
</template>

<style scoped>

</style>