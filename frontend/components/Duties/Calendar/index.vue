<script setup lang="ts">
import type {dutyUserDataTypeList} from "~/types/duty.js";

const props = defineProps<{
  dutiesData: dutyUserDataTypeList
}>();
defineEmits(['reserveDuty', 'releaseDuty'])

const daysOfWeek = [
  [1, "Пн"],
  [2, "Вт"],
  [3, "Ср"],
  [4, "Чт"],
  [5, "Пт"],
  [6, "Сб"],
  [0, "Вс"],
];

// Precompute duties for each day to avoid filtering in the template
const dutiesByDay = computed(() => {
  const grouped = {};
  daysOfWeek.forEach(([dayIndex]) => {
    grouped[dayIndex] = props.dutiesData.filter(
        (duty) => duty.date.getDay() === dayIndex
    );
  });
  if (props.dutiesData.length !== 0) {
    let firstDayOfMonth = props.dutiesData[0].date.getDay()
    let daysEmptyToAdd = []
    switch (firstDayOfMonth) {
      case 0:
        // Sunday
        daysEmptyToAdd = [1, 2, 3, 4, 5, 6]
        break
      case 1:
        // Monday
        daysEmptyToAdd = []
        break
      case 2:
        daysEmptyToAdd = [1]
        break
      case 3:
        daysEmptyToAdd = [1, 2]
        break
      case 4:
        daysEmptyToAdd = [1, 2, 3]
        break
      case 5:
        daysEmptyToAdd = [1, 2, 3, 4]
        break
      case 6:
        daysEmptyToAdd = [1, 2, 3, 4, 5]
        break
    }
    for (let i = 0; i < daysEmptyToAdd.length; i++) {
      let day = daysEmptyToAdd[i]
      grouped[day].unshift({id: null, date: null})
    }
  }
  return grouped;
});

const getDutiesForDay = (dayIndex) => {
  return dutiesByDay.value[dayIndex] || [];
};
</script>

<template>
  <div class="p-4">
    <h2 class="text-2xl font-bold mb-2">Календарь дежурств</h2>
    <div class="grid grid-cols-7 gap-0">
      <!-- Days of the week header -->
      <div
          v-for="[dayIndex, day] in daysOfWeek"
          :key="dayIndex"
          class="font-semibold text-center flex flex-col gap-4"
      >
        <template v-if="[0, 6].includes(dayIndex)">
          <div class="text-red-500">{{ day }}</div>
        </template>
        <template v-else>
          <div class="text-gray-500">{{ day }}</div>
        </template>
        <div
            v-for="duty in getDutiesForDay(dayIndex)"
            :key="duty.id"
            class="text-sm"
        >
          <DutiesCalendarDay
              :duty="duty"
              @reserveDuty="(id) => $emit('reserveDuty', id)"
              @releaseDuty="(id) => $emit('releaseDuty', id)"
          />
        </div>
      </div>
    </div>
    <div class="mt-4">
      <span>Для бронирования выберите желаемую дату</span>
    </div>
  </div>
</template>

