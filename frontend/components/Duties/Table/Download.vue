<script setup lang="ts">
import { saveAs } from "file-saver";
import Docxtemplater from "docxtemplater";
import PizZip from "pizzip";
import * as Excel from 'exceljs'

const props = defineProps<{
  rows: Array<{
    Date: string;
    Name: string;
    User: { label: string; href: string };
  }>;
  columns: Array<{ key: string; label: string }>;
}>();

// Function to download data as DOCX
const downloadDocx = () => {
  const content = `
    <table border="1">
      <thead>
        <tr>
          ${props.columns.map((col) => `<th>${col.label}</th>`).join("")}
        </tr>
      </thead>
      <tbody>
        ${props.rows
      .map(
          (row) => `
          <tr>
            <td>${row.Date}</td>
            <td>${row.Name}</td>
            <td>${row.User.label}</td>
          </tr>
        `
      )
      .join("")}
      </tbody>
    </table>
  `;

  const zip = new PizZip();
  const doc = new Docxtemplater(zip, {
    paragraphLoop: true,
    linebreaks: true,
  });

  doc.render({
    table: content,
  });

  const blob = doc.getZip().generate({ type: "blob" });
  saveAs(blob, "duties.docx");
};
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
const downloadTxt = () => {
  const content = props.rows
      .map(
          (row) =>
              `${row.Date}\t${row.Name}\t${row.User.label}` // Tab-separated values
      )
      .join("\n"); // Newline-separated rows

  const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
  saveAs(blob, "duties.txt");
};
</script>

<template>
  <div class="flex gap-2">
<!--    <UButton @click="downloadDocx" icon="i-heroicons-document-text">-->
<!--      Скачать DOCX-->
<!--    </UButton>-->
<!--    <UButton @click="downloadExcel" icon="i-heroicons-document-chart-bar">-->
<!--      Скачать Excel-->
<!--    </UButton>-->
    <UButton @click="downloadTxt" icon="i-heroicons-document-text">
      Скачать TXT
    </UButton>
  </div>
</template>

<style scoped>
/* Add custom styles if needed */
</style>