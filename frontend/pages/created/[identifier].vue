<script setup lang="ts">
import type {dutyListType, RoomOwnerRead} from "~/types/room";
import type {DutiesWithUserResponse, SuccessDeleteType} from "~/types/duty";
import {formatDateToYYYYMMDD} from "~/services/date";

const toast = useToast();
const route = useRoute();
const $backend = useBackend();
const $client = useClientFetch()

const roomIdentifier = route.params.identifier;
const newDuties = reactive<dutyListType>([]);
// Fetch room data
const {data: roomData} = await $backend.$get<RoomOwnerRead>(`/room/storage/${roomIdentifier}`);
const room: RoomOwnerRead = reactive({...roomData.value});
const {
  data: dutiesData,
  refresh: refreshDuties
} = await $backend.$get<DutiesWithUserResponse>(`/room/${roomIdentifier}/duties`);
const duties = computed(() => {
  let existingDuties = dutiesData.value["duties"]
  return [...newDuties, ...existingDuties]
})
const dutyUpdateData = computed(() => {
  return {
    ...room,
    extra_duties: Array.from(newDuties)
  }
})
// Function to update room name
const updateRoom = async () => {
  try {
    let response = await $client.$patch(`/room/${room.id}`, {
      body: dutyUpdateData.value
    })
    if (response) {
      toast.add({
        title: "Успешно",
        description: "Комната обновлена",
        color: "green"
      })
    }
  } catch (error) {
    console.error("Failed to update room:", error);
    toast.add({
      title: "Ошибка",
      description: "Не удалось обновить комнату",
      color: "red"
    })
  }
};

// Function to add a new duty
const addDuty = () => {
  const newDuty = {
    duty_date: "2025-01-01", // Default date
    name: "", // Default name
  };
  newDuties.push(newDuty);
};

const updateDuty = async (duty: any) => {
  try {
    let response = await $client.$put(`/duties/${duty.id}`, {
      body: duty
    });
    if (response) {
      toast.add({
        title: "Успешно",
        description: "Дежурство обновлено",
        color: "green"
      })
      await refreshDuties();
    } else {
      toast.add({
        title: "Ошибка",
        description: "Не удалось обновить дежурство",
        color: "red"
      })
    }
    refreshDuties();
  } catch (error) {
    console.error("Failed to update duty:", error);
    toast.add({
      title: "Ошибка",
      description: "Не удалось обновить дежурство",
      color: "red"
    })
  }
};

// Function to remove a duty
const removeDuty = async (dutyId: number) => {
  try {
    let response = await $client.$delete<SuccessDeleteType>(`/duties/${dutyId}`)
    if (response.status === "success") {
      await refreshDuties()
      toast.add({
        title: "Успешно",
        description: "Дежурство удалено",
        color: "green"
      })
    }
  } catch (error) {
    toast.add({
      title: "Ошибка",
      description: "Не удалось удалить дежурство",
      color: "red"
    })
  }
};
</script>

<template>
  <div class="p-8">
    <!-- Room Information -->
    <div class="mb-8">
      <div class="flex flex-row items-center gap-2 mb-4
       max-sm:flex-col">
        Чтобы пригласить кого нибудь в комнату просто поделитесь ссылкой
        <RoomShare :room-identifier="room.identifier" />
      </div>
      <h1 class="text-2xl font-bold mb-4 flex flex-row">
        Настройки
      </h1>
      <UInput v-model="room.name" label="Room Name" class="mb-4"/>
      <div class="flex flex-row max-sm:flex-col gap-2">
        <UButton @click="updateRoom" color="primary" class="w-auto max-w-fit">
          Обновить данные и сохранить новые дежурства
        </UButton>
        <RoomDelete :id="room.id" class="w-auto max-w-fit"/>
      </div>
    </div>
    <!-- Duties List -->
    <div class="mb-8">
      <h2 class="text-xl font-bold mb-4">Дежурства</h2>
      <UFormGroup label="Может ли один человек выбрать несколько дат" class="mb-2">
        <UToggle v-model="room.is_multiple_selection"/>
      </UFormGroup>
      <UButton @click="addDuty" color="green" class="mb-4">Добавить новое дежурство</UButton>

      <div v-for="duty in duties" :key="duty.id"
           class="mb-4 p-4 border rounded-xl flex flex-col gap-2">
        <UInput v-model="duty.name" label="Duty Name"/>
        <UPopover :popper="{ placement: 'bottom-start' }">
          <UButton icon="i-heroicons-calendar-days-20-solid" :label="duty.date"/>

          <template #panel="{ close }">
            <DatePicker @update:model-value="(value) => {
              duty.date = formatDateToYYYYMMDD(value)
            }" :model-value="new Date(duty.date)" is-required @close="close"/>
          </template>
        </UPopover>
        <div class="flex gap-2">
          <UButton @click="updateDuty(duty)" color="primary">Обновить</UButton>
          <UButton @click="removeDuty(duty.id)" color="red">Удалить</UButton>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Add custom styles if needed */
</style>