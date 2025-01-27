<script setup lang="ts">
import {object, string, type InferType} from 'yup'
import type {dateRangeType, State} from "~/types/room";
import CalendarCreate from "~/components/Room/CalendarCreate.vue";

const isOpen = ref(true); // Control modal visibility
const selectedDates = ref<string[]>([]);

const schema = object({
  name: string().required("Длина должна быть больше нуля"),
})
const state = reactive<State>({
  name: undefined,
  duty_list: undefined,
  is_multiple_selection: false
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

const submitForm = () => {
  console.log("submit form", state)
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
        <UForm class="space-y-4" :schema="schema" :state="state" @submit="submitForm">
          <UFormGroup label="Название комнаты" name="name">
            <UInput v-model="state.name" is-required />
          </UFormGroup>
            <UFormGroup label="Даты">
              <CalendarCreate @update="updateListData"/>
            </UFormGroup>
            <UFormGroup label="Может ли один человек выбрать несколько дат">
              <UToggle v-model="state.is_multiple_selection" />
            </UFormGroup>
          <UButton type="submit">Создать</UButton>

        </UForm>
        result data is {{ state }}
      </UCard>
    </UModal>
  </div>
</template>