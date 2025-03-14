<script setup lang="ts">
import type {dutyUserDataType, groupedDutiesType} from "~/types/duty";
import {useUserStore} from "~/store/user";
const userStore = useUserStore()
const props = defineProps<{
  duty: groupedDutiesType
}>()
defineEmits(['reserveDuty', 'releaseDuty'])

const isOpen = ref(false)
const freeDutiesCount = computed(() => {
  if (!props.duty.duties) return 0
  return props.duty.duties.filter((duty: dutyUserDataType) => duty.user === null ).length
})

watch(freeDutiesCount, (value) => {
  if (value === 0 && !DutyTakenByUser.value) {
    isOpen.value = false
  }
}, { deep: true })

const dayDisabled = computed(() => {
  return freeDutiesCount.value === 0 && !DutyTakenByUser.value
})
const DutyTakenByUser = computed(() => {
  return props.duty.duties.some((duty: dutyUserDataType) => {
    return duty.user && duty.user.id === userStore.user_id
  })
})
const dayColor = computed(() => {
  if (DutyTakenByUser.value) {
    return 'amber'
  } else {
    if (freeDutiesCount.value === 0) {
      return 'gray'
    }
    return 'primary'
  }
})
</script>

<template>
  <template v-if="duty.date">
    <UChip :text="freeDutiesCount" :show="freeDutiesCount > 0" size="2xl">
      <UButton @click="isOpen = true" :disabled="dayDisabled" :color="dayColor" variant="solid" class="w-8 h-8">
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
            <DutiesCalendarDuty :duty="duty"
                                @reserveDuty="(id) => {$emit('reserveDuty', id); isOpen = false}"
                                @releaseDuty="(id) => {$emit('releaseDuty', id); isOpen = false}"
            />
          </div>
        </div>
      </UCard>
    </UModal>
  </template>
  <div v-else class="w-8 h-8 bg-transparent"></div>
</template>

<style scoped>

</style>
