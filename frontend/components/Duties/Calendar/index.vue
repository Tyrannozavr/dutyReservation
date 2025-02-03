<script setup>
const props = defineProps({
  dutiesData: {
    type: Array,
    required: true,
    validator: (value) =>
        value.every((duty) => duty.date instanceof String && duty.id),
  },
});

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
          <DutiesCalendarDay :duty="duty" @book="(id) => $emit('book', id)" />
        </div>
        <div
            v-if="getDutiesForDay(dayIndex).length === 0"
            class="text-gray-500 text-sm"
        >
          Нет дежурств
        </div>
      </div>
    </div>
  </div>
</template>

