<script setup lang="ts">
import type {dutyWithUserTypeList} from "~/types/duty";

const props = defineProps<{
  duties: dutyWithUserTypeList
}>()

const columns = [
  {
    key: 'Date',
    label: 'Дата'
  },
  {
    key: 'Name',
    label: 'Название'
  },
  {
    key: 'User',
    label: 'Пользователь'
  }
]

const rows = computed(() => {
  return props.duties.map((duty) => {
    return {
      Date: new Date(duty.date).toLocaleString('default', {month: 'short', day: 'numeric'}),
      Name: duty.name,
      User: duty.user ? {
            label: duty.user.first_name + ' ' + duty.user.last_name,
            href: duty.user.link
          } :
          {
            label: 'Не назначен',
            href: "#"
          }
    }
  })
})

</script>

<template>
  <UTable :columns="columns" :rows="rows">
    <template #User-data="{ row }">
      <div class="flex items-center gap-2">
        <ULink :to="row.User.href" target="_blank" class="text-blue-500 hover:text-blue-600">
          {{ row.User.label }}
        </ULink>
      </div>
    </template>
  </UTable>
</template>

<style scoped>

</style>