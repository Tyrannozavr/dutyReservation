<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  dutiesData: {
    type: Array,
    required: true,
    default: () => []
  }
});

// Method to handle duty click
const handleDutyClick = (duty) => {
  // Handle the click event (e.g., navigate to a detail page or show a modal)
  console.log('Duty clicked:', duty);
};
</script>

<template>
  <div class="p-4">
    <div v-for="duty in dutiesData">{{duty.date}} {{new Date(duty.date).getDay()}}</div>
    <h2 class="text-2xl font-bold mb-4">Duties Calendar</h2>
    <div class="grid grid-cols-8 gap-2">
      <!-- Days of the week header -->
      <div class="font-semibold text-center"
           v-for="(day, index) in ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']"
           :key="index">
        {{ day }}
      </div>

      <!-- Duties for each day -->
      <div v-for="dayIndex in [0, 1, 2, 3, 4, 5, 6]" :key="dayIndex" class="text-center">
        <div class="font-semibold">
          {{ dutiesData.find(d => new Date(d.date).getDay() === dayIndex)?.date || '' }}
        </div>
        <div v-for="duty in dutiesData.find(d => new Date(d.date).getDay() === dayIndex)?.duties || []" :key="duty.id">
          <button
              @click="handleDutyClick(duty)"
              class="block bg-blue-500 text-white py-1 px-2 rounded hover:bg-blue-600 transition"
          >
            {{ duty.name || '__' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
