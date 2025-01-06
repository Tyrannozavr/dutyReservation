<!-- components/ExpandedCalendar.vue -->
<template>
  <div class="calendar-container">
    <h2>Select a Month</h2>
    <select v-model="selectedMonth" @change="updateDaysInMonth">
      <option v-for="(month, index) in months" :key="index" :value="index">
        {{ month }}
      </option>
    </select>

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
import { ref, computed } from 'vue';

const currentYear = new Date().getFullYear();
const months = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December'
];
const weekDays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

const selectedMonth = ref(new Date().getMonth());
const disabledDates = ref([new Date(currentYear, selectedMonth.value, 5), new Date(currentYear, selectedMonth.value, 10)]); // Example disabled dates
const daysInMonth = ref([]);

// Calculate the first day offset for proper alignment
const firstDayOffset = computed(() => {
  const firstDay = new Date(currentYear, selectedMonth.value, 1).getDay();
  return firstDay; // This gives the number of empty slots before the first day of the month
});

const updateDaysInMonth = () => {
  const date = new Date(currentYear, selectedMonth.value, 1);
  const lastDay = new Date(currentYear, selectedMonth.value + 1, 0).getDate();

  daysInMonth.value = Array.from({ length: lastDay }, (_, i) => {
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
  console.log('Selected date:', date);
};

// Initialize days in month on component mount
updateDaysInMonth();
</script>

<style scoped>
.calendar-container {
  max-width: 400px;
  margin: auto;
}

.calendar {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 5px; /* Space between days */
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
