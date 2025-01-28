<script setup lang="ts">
import { sub, format, isSameDay } from 'date-fns';
import { ru } from 'date-fns/locale';

import type { dateRangeType } from '~/types/room';

const emits = defineEmits(['update']);

let today = new Date();

const ranges = [
  {
    label: format(today, 'LLLL', { locale: ru }),
    dateRange: {
      start: new Date(today.getFullYear(), today.getMonth(), 1),
      end: new Date(today.getFullYear(), today.getMonth() + 1, 0),
    },
  },
  {
    label: format(new Date(today.getFullYear(), today.getMonth() + 1, 1), 'LLLL', { locale: ru }),
    dateRange: {
      start: new Date(today.getFullYear(), today.getMonth() + 1, 1),
      end: new Date(today.getFullYear(), today.getMonth() + 2, 0),
    },
  },
];

const selected = ref({ start: sub(new Date(), { days: 14 }), end: new Date() });
const isMobileModalOpen = ref(false);

watch(
    selected,
    (value) => {
      emits('update', value);
    },
    {
      deep: true,
    },
);

function isRangeSelected(dateRange: dateRangeType) {
  return isSameDay(selected.value.start, dateRange.start) && isSameDay(selected.value.end, dateRange.end);
}

function selectRange(dateRange: dateRangeType) {
  selected.value = dateRange;
  isMobileModalOpen.value = false; // Close modal after selection on mobile
  close();
}
</script>

<template>
  <div>
    <!-- Button to open the date picker -->
    <UButton icon="i-heroicons-calendar-days-20-solid" @click="isMobileModalOpen = true">
      {{ format(selected.start, 'd MMM, yyy', { locale: ru }) }} - {{ format(selected.end, 'd MMM, yyy', { locale: ru }) }}
    </UButton>
    <!-- Desktop Popover -->
    <UPopover :popper="{ placement: 'bottom-start' }" class="hidden sm:block">
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
          <DatePicker v-model="selected" @close="close" />
        </div>
      </template>
    </UPopover>

<!--     Mobile Modal-->
    <UModal
        v-model="isMobileModalOpen"
        :ui="{ container: 'flex items-start justify-center mt-24' }"
    >
      <UCard>
        <template #header>
          Выберите диапазон дат или опцию слева от календаря
        </template>
        <div class="flex flex-row space-y-4 justify-center">
          <div class="flex flex-col space-y-2">
            <UButton
                v-for="(range, index) in ranges"
                :key="index"
                :label="range.label"
                color="gray"
                variant="ghost"
                class="text-left h-12"
                :class="[isRangeSelected(range.dateRange) ? 'bg-gray-100 dark:bg-gray-800' : 'hover:bg-gray-50 dark:hover:bg-gray-800/50']"
                truncate
                @click="selectRange(range.dateRange)"
            />
          </div>
          <DatePicker v-model="selected" @close="close" />
        </div>
      </UCard>
    </UModal>
  </div>
</template>
