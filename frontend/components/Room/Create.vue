
<script setup lang="ts">
import { object, string, type InferType } from 'yup'

// State management
import CalendarCreate from "~/components/Room/CalendarCreate.vue";

const isOpen = ref(true); // Control modal visibility
const showCalendar = ref(false);
const selectedDates = ref<string[]>([]);

const schema = object({
  name: string()
})
const state = reactive({
  name: undefined,
  dateList: undefined
})

// Toggle calendar visibility
const toggleCalendar = () => {
  showCalendar.value = !showCalendar.value;
};

// Handle date changes
const onDateChange = (dates: string[]) => {
  selectedDates.value = dates;
};

const updateListData = (dateRange: {start: string, end: string}) => {
  console.log(dateRange, "helloworld")
}

// Submit selected dates
const submitDates = () => {
  const payload = {
    name: "string", // Replace with actual name or input field value
    is_multiple_selection: true, // Set to true if multiple selection is allowed
    duty_list: selectedDates.value.map(date => ({
      duty_date: date,
      name: "string" // Replace with actual duty name or input field value
    })),
  };

  console.log('Payload for creation:', payload);
  alert('Payload for creation: ' + JSON.stringify(payload));
};
</script>


<template>
<div>
  <UButton @click="isOpen  = true">Создать</UButton>
  <UModal v-model="isOpen">
    <UCard>
      <template #header>
        Создание комнаты
      </template>
      <UForm class="space-y-4" :schema="schema" :state="state">
        <UFormGroup label="Название комнаты">
          <UInput v-model="state.name" />
        </UFormGroup>
        <UFormGroup label="Даты">
          <CalendarCreate  @update="updateListData" />
        </UFormGroup>
      </UForm>
    </UCard>
  </UModal>
</div>
</template>

<style scoped>
.container {
  max-width: 600px;
}
</style>