<script setup lang="ts">
import {object, string, type InferType} from 'yup'

// State management
import CalendarCreate from "~/components/Room/CalendarCreate.vue";
import type {dateRangeType, State} from "~/types/room";

const isOpen = ref(true); // Control modal visibility
const selectedDates = ref<string[]>([]);

const schema = object({
  name: string()
})
const state = reactive<State>({
  name: undefined,
  duty_list: undefined
})

function formatDateToYYYYMMDD(date: Date): string {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are zero-based
  const day = String(date.getDate()).padStart(2, '0');

  return `${year}-${month}-${day}`;
}


const updateListData = (dateRange: dateRangeType) => {
  const dateList: Date[] = []
  const currentDate = dateRange.start
  while (currentDate < dateRange.end) {
    dateList.push(currentDate)
    currentDate.setDate(currentDate.getDate() + 1)
  }
  state.duty_list = dateList.map((item) => {
    return {
      name: "",
      duty_date: formatDateToYYYYMMDD(item)
    }
  })
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
            <UInput v-model="state.name"/>
          </UFormGroup>
          <UFormGroup label="Даты">
            <CalendarCreate @update="updateListData"/>
          </UFormGroup>
        </UForm>
        result data is {{ state }}
      </UCard>
    </UModal>
  </div>
</template>

<style scoped>
.container {
  max-width: 600px;
}
</style>