<script setup lang="ts">
import type {dutyWithUserType, groupedDutiesType} from "~/types/duty";

const props = defineProps<{
  duty: groupedDutiesType
}>()
defineEmits(['book'])

const isOpen = ref(false)
const freeDutiesCount = computed(() => {
  return props.duty.duties.filter((duty: dutyWithUserType) => duty.user === null ).length
})
</script>

<template>
  <template v-if="duty.date">
    <UChip :text="freeDutiesCount" :show="freeDutiesCount > 0" size="2xl">
      <UButton @click="isOpen = true" :disabled="freeDutiesCount === 0" color="primary" variant="solid" class="w-8 h-8">
        {{ duty.date.getDate() }}
      </UButton>
    </UChip>
    <UModal v-model="isOpen" :ui="{ container: 'flex items-start justify-center mt-12' }">
      <UCard>
        <template #header>
          <div class="flex justify-between">
            <div class="flex gap-2">
              <div class="text-2xl">{{ duty.date.getDate() }}</div>
              <div class="text-2xl">{{ duty.date.toLocaleString('default', { month: 'long' }) }}</div>
              <div class="text-2xl">{{ duty.date.getFullYear() }}</div>
            </div>
          </div>
        </template>
        <div class="flex flex-col gap-2">
          <div v-for="duty in duty.duties" class="flex gap-2">
            <DutiesCalendarDuty :duty="duty" @book="(id) => {$emit('book', id); isOpen = false}" />
          </div>
        </div>
      </UCard>
    </UModal>
  </template>
  <div v-else class="w-8 h-8 bg-transparent"></div>
</template>

<style scoped>

</style>
