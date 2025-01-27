<script setup lang="ts">
import {sub, format, isSameDay, type Duration} from 'date-fns'

const emits = defineEmits(['update'])

let today = new Date()
type dateRangeType = {
  start: Date,
  end: Date
}
const ranges = [
  {
    label: 'Выбрать текущий месяц', dateRange: {
      start: new Date(today.getFullYear(), today.getMonth(), 1),
      end: new Date(today.getFullYear(), today.getMonth() + 1, 0)
    }

  },
  {
    label: 'Выбрать следующий месяц', dateRange: {
      start: new Date(today.getFullYear(), today.getMonth() + 1, 1),
      end: new Date(today.getFullYear(), today.getMonth() + 2, 0)
    }
  },

]
// const selected = ref({ start: sub(new Date(), { days: 14 }), end: new Date() })
const selected = ref({start: sub(new Date(), {days: 14}), end: new Date()})

watch(
    selected,
    (value) => {
      emits('update', value)
    },
    {
      deep: true
    }
)

function isRangeSelected(dateRange: dateRangeType) {
  return isSameDay(selected.value.start, dateRange.start) && isSameDay(selected.value.end, dateRange.end)
}

function selectRange(dateRange: dateRangeType) {
  selected.value = dateRange
  // selected.value = { start: sub(new Date(), duration), end: new Date() }
}
</script>

<template>
  <UPopover :popper="{ placement: 'bottom-start' }">
    <UButton icon="i-heroicons-calendar-days-20-solid">
      {{ format(selected.start, 'd MMM, yyy') }} - {{ format(selected.end, 'd MMM, yyy') }}
    </UButton>

    <template #panel="{ close }">
      <div class="flex items-center sm:divide-x divide-gray-200 dark:divide-gray-800">
        <div class="hidden sm:flex flex-col py-4">
          <UButton
              v-for="(range, index) in ranges"
              :key="index"
              :label="range.label"
              color="gray"
              variant="ghost"
              class="rounded-none px-6"
              :class="[isRangeSelected(range.dateRange) ? 'bg-gray-100 dark:bg-gray-800' : 'hover:bg-gray-50 dark:hover:bg-gray-800/50']"
              truncate
              @click="selectRange(range.dateRange)"
          />
        </div>

        <DatePicker v-model="selected" @close="close"/>
      </div>
    </template>
  </UPopover>
</template>


