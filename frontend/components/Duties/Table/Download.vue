<script setup lang="ts">
import * as Excel from 'exceljs'

const props = defineProps<{
  rows: Array<{
    Date: string;
    Name: string;
    User: { label: string; href: string };
  }>;
  columns: Array<{ key: string; label: string }>;
}>();

// async function exportFile() {
//   const workbook = new Excel.Workbook()
//   // workbook.addImage()
//   // Sheet
//   const worksheet = workbook.addWorksheet('My Sheet')
//
//   // Header
//   worksheet.columns = [
//     {header: 'Название', key: 'name', width: 100},
//     {header: 'Цена', key: 'price'},
//     {header: 'Количество', key: 'count'},
//     {header: 'Сумма', key: 'totalPrice'}
//   ]
//
//   Basket().products.forEach((product) => {
//     let row = worksheet.addRow([product.name, product.price, product.count, product.price * product.count])
//   })
//   worksheet.addRow(['Итого:', null, null, Basket().totalPrice])
//
//   // workbook to Blob
//   const uint8Array = await workbook.xlsx.writeBuffer()
//   const blob = new Blob([uint8Array], {type: 'application/octet-binary'})
//
//   // Download
//   const url = URL.createObjectURL(blob)
//   const a = document.createElement('a')
//   document.body.appendChild(a)
//   a.download = `Корзина.xlsx`
//   a.href = url
//   a.click()
//   a.remove()
//   URL.revokeObjectURL(url)
// }
// Function to download data as Excel
// const downloadExcel = () => {
//   const worksheet = XLSX.utils.json_to_sheet(
//       props.rows.map((row) => ({
//         Дата: row.Date,
//         Название: row.Name,
//         Пользователь: row.User.label,
//       }))
//   );
//   const workbook = XLSX.utils.book_new();
//   XLSX.utils.book_append_sheet(workbook, worksheet, "Duties");
//   XLSX.writeFile(workbook, "duties.xlsx");
// };

// Function to download data as TXT

const content = computed(() => {
  return props.rows
      .map(
          (row) =>
              `${row.Date}\t${row.Name}\t${row.User.label}` // Tab-separated values
      )
      .join("\n");
})
</script>

<template>
  <div class="flex gap-2">
    <DownloadDocx :content="content" filename="duties"/>
    <!--    <UButton @click="downloadExcel" icon="i-heroicons-document-chart-bar">-->
    <!--      Скачать Excel-->
    <!--    </UButton>-->
    <DownloadText :content="content" filename="duties"/>
  </div>
</template>

<style scoped>
/* Add custom styles if needed */
</style>