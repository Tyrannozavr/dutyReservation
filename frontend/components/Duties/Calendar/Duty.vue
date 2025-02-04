<script setup lang="ts">
import type {dutyWithUserType} from "~/types/duty";

defineProps<{
  duty: dutyWithUserType
}>()
defineEmits(['book'])

</script>

<template>
  <div class="flex flex-row gap-5">
    <div>{{ duty.name ? duty.name : "Без имени" }}</div>
    <div class="ml-auto">
      <UButton @click="$emit('book', duty.id)">Бронировать</UButton>
    </div>
  </div>
</template>

<style scoped>

</style>