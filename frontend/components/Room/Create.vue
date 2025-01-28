<script setup lang="ts">
import {object, string, type InferType} from 'yup'
import type {dateRangeType, dutyListType, RoomOwnerRead, State} from "~/types/room";
import CalendarCreate from "~/components/Room/CalendarCreate.vue";
import DetailSettings from "~/components/Room/DetailSettings.vue";
const toast = useToast()
const $client = useClientFetch()
const emits = defineEmits(["roomCreated"])
const isOpen = ref(false);

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
const updateDutyList = (dutyListValue: dutyListType) => {
  state.duty_list = dutyListValue
}

const updateListData = (dateRange: dateRangeType) => {
  const dateList: Date[] = []
  const currentDate = new Date(dateRange.start)
  while (currentDate < dateRange.end) {
    dateList.push(new Date(currentDate))
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
const submitForm = async () => {
  const response = await $client.$post<RoomOwnerRead>("/room",  {
    body: state
  })
  if (response.identifier) {
    toast.add({
      id: 'success',
      title: 'Успешно',
      description: 'Комната успешно создана',
      color: 'green',
    });
    emits("roomCreated")
    isOpen.value = false
  }

};
</script>

<template>
  <div>
    <UButton @click="isOpen  = true">Создать</UButton>
    <UModal v-model="isOpen" :ui="{ container: 'flex items-start justify-center mt-12' }">
      <UCard>
        <template #header>
          Создание комнаты
        </template>
        <UForm class="space-y-4" :schema="schema" :state="state" @submit="submitForm">
          <UFormGroup label="Название комнаты" name="name">
            <UInput v-model="state.name" is-required/>
          </UFormGroup>
          <UFormGroup label="Даты">
            <CalendarCreate @update="updateListData"/>
          </UFormGroup>
          <UFormGroup label="Может ли один человек выбрать несколько дат">
            <UToggle v-model="state.is_multiple_selection"/>
          </UFormGroup>
          <DetailSettings
              v-if="state.duty_list"
              :dutyList="state.duty_list"
              @onUpdateDutyList="updateDutyList"
          />
          <UButton type="submit">Создать</UButton>
        </UForm>
      </UCard>
    </UModal>
  </div>
</template>