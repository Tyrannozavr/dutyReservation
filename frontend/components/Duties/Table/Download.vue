<script setup lang="ts">
import {useUserStore} from "~/store/user";

const props = defineProps<{
  rows: Array<{
    Date: string;
    Name: string;
    User: { label: string; href: string };
  }>;
  columns: Array<{ key: string; label: string }>;
}>();

const content = computed(() => {
  return props.rows
      .map(
          (row) =>
              `${row.Date}\t${row.Name}\t${row.User.label}` // Tab-separated values
      )
      .join("\n");
})
const excelColumns = [
  {header: "Дата", key: "Date", width: 20},
  {header: "Название", key: "Name", width: 30},
  {header: "Пользователь", key: "User", width: 40},
]
const excelRows = computed(() => props.rows.map((row) => {
  return [
    row.Date,
    row.Name,
    row.User.label,
  ]
}))
const userStore = useUserStore()
const toast = useToast()
const copyContent = () => {

  navigator.clipboard.writeText(content.value)
  toast.add({
    title: "Скопировано успешно",
    timeout: 1000,
    color: "green",
  })
}
</script>

<template>
  <template v-if="userStore.origin == 'web'">
    <div class="font-bold mb-4 text-2xl">Загрузить результаты</div>
    <div class="flex gap-2" >
      <DownloadDocx :content="content" filename="duties">docx</DownloadDocx>
      <DownloadExcel :rows="excelRows" :columns="excelColumns" filename="duties">excel</DownloadExcel>
      <DownloadText :content="content" filename="duties">txt</DownloadText>
    </div>
  </template>
  <template v-else>
    <div class="font-bold mb-4 text-2xl">Скопировать результаты</div>
    <div class="flex gap-2" >
      <UButton @click="copyContent" icon="i-heroicons-document-duplicate" />
      <!--    <UButton icon="i-heroicons-document-arrow-down" />-->
    </div>
  </template>

</template>

<style scoped>
/* Add custom styles if needed */
</style>