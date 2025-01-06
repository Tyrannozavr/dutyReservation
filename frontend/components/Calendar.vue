<!-- components/ExpandedCalendar.vue -->
<template>
  <div class="calendar-container">
    <h3>{{ months[selectedMonth] }} {{ currentYear }}</h3>
    <div class="calendar">
      <div class="calendar-header">
        <div v-for="(day, index) in weekDays" :key="index" class="calendar-weekday">{{ day }}</div>
      </div>
      <div class="calendar-body">
        <!-- Fill empty slots for days before the first day of the month -->
        <div v-for="n in firstDayOffset" :key="'empty-' + n" class="calendar-day empty"></div>
        <div
            v-for="day in daysInMonth"
            :key="day.date"
            :class="['calendar-day', { disabled: day.disabled }]"
            @click="day.disabled ? null : selectDate(day.date)"
        >
          {{ day.date.getDate() }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const currentYear = new Date().getFullYear();
const months = [
  'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
  'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
];
const weekDays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'];

const selectedMonth = ref(new Date().getMonth());
// const disabledDates = ref([new Date(currentYear, selectedMonth.value, 5), new Date(currentYear, selectedMonth.value, 10)]); // Example disabled dates
// const disabledDates = ref([new Date(currentYear, selectedMonth.value, 5)]); // Example disabled dates
const daysInMonth = ref([]);
const disabledDates = computed(() => {
  return selectedDay.value ? [
    selectedDay.value
  ] : [];
})
// Calculate the first day offset for proper alignment
const firstDayOffset = computed(() => {
  const firstDay = new Date(currentYear, selectedMonth.value, 1).getDay() - 1;
  return firstDay; // This gives the number of empty slots before the first day of the month
});
const selectedDay = ref(null)

const updateDaysInMonth = () => {
  const date = new Date(currentYear, selectedMonth.value, 1);
  const lastDay = new Date(currentYear, selectedMonth.value + 1, 0).getDate();

  daysInMonth.value = Array.from({length: lastDay}, (_, i) => {
    const dayDate = new Date(currentYear, selectedMonth.value, i + 1);
    return {
      date: dayDate,
      disabled: disabledDates.value.some(disabledDate =>
          disabledDate.getDate() === dayDate.getDate() &&
          disabledDate.getMonth() === dayDate.getMonth() &&
          disabledDate.getFullYear() === dayDate.getFullYear()
      )
    };
  });
};

// Handle date selection logic
const selectDate = (date) => {
  // disabledDates.value.push(date)
  // updateDaysInMonth()
  selectedDay.value = date
  updateDaysInMonth()
};

// Initialize days in month on component mount
updateDaysInMonth();
</script>

<style scoped>
.calendar-container {
  max-width: 400px;
  margin-left: 10px;
}

.calendar {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 3px; /* Space between days */
}

.calendar-header {
  display: contents; /* Use contents to not affect grid layout */
}

.calendar-weekday {
  font-weight: bold;
  text-align: center;
}

.calendar-body {
  display: contents; /* Use contents to not affect grid layout */
}

.calendar-day {
  border: 1px solid #ccc;
  padding: 15px;
  text-align: center;
  cursor: pointer;
}

.calendar-day.empty {
  background-color: transparent; /* Empty slots have no background */
}

.calendar-day.disabled {
  background-color: #f0f0f0;
  cursor: not-allowed;
}
</style>
