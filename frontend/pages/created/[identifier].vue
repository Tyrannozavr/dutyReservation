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
const {data: roomData} = await $backend.$get<RoomOwnerRead>(`/room/owner/${roomIdentifier}`);
const room: RoomOwnerRead = reactive({...roomData.value});
const {data: dutiesData, refresh: refreshDuties} = await $backend.$get<DutiesWithUserResponse>(`/duty/${roomIdentifier}`);
// const duties = reactive([...dutiesData.value["duties"]]);
const duties = computed(() => {
  let existingDuties = dutiesData.value["duties"]
  existingDuties.sort((a, b) => {
    const dateA = new Date(a.date);
    const dateB = new Date(b.date);
    return dateA.getTime() - dateB.getTime();
  })
  return [...existingDuties, ...newDuties]
      // .sort((a, b) => {
    // const dateA = new Date(a.date);
    // const dateB = new Date(b.date);
    // return dateA.getTime() - dateB.getTime();
  // })
})
// Function to update room name
const updateRoomName = async () => {
  // console.log("change to", room.value.name)
  // try {
  //   await $backend.$patch(`/room/owner/${roomIdentifier}`, { name: room.name });
  //   alert("Room name updated successfully!");
  // } catch (error) {
  //   console.error("Failed to update room name:", error);
  // }
};

// Function to add a new duty
const addDuty = () => {
  const newDuty = {
    duty_date: "2025-01-01", // Default date
    name: "", // Default name
  };
  newDuties.push(newDuty);
};

// Function to update a duty
const updateDuty = async (duty: any) => {
  console.log("change to", duty)
  // try {
  //   await $backend.$patch(`/duty/${duty.id}`, { name: duty.name, date: duty.date });
  //   alert("Duty updated successfully!");
  // } catch (error) {
  //   console.error("Failed to update duty:", error);
  // }
};

// Function to remove a duty
const removeDuty = async (dutyId: number) => {
  try {
    let response = await $client.$delete<SuccessDeleteType>(`/duty/${dutyId}`)
    // console.log(response)
    // console.log("Hello,", response.status)
    if (response.status === "success") {
      console.log("success refresh")
      await refreshDuties()
      toast.add({
        title: "Успешно",
        description: "Дежурство удалено",
        color: "green"
      })
    }
  } catch (error) {
    console.error("Failed to remove duty:", error);
    toast.add({
      title: "Ошибка",
      description: "Не удалось удалить дежурство",
      color: "red"
    })
  }
  // try {
  //   await $backend.$delete(`/duty/${dutyId}`);
  //   duties.splice(duties.findIndex((d) => d.id === dutyId), 1);
  //   alert("Duty removed successfully!");
  // } catch (error) {
  //   console.error("Failed to remove duty:", error);
  // }
};
</script>

<template>
  <div class="p-8">
    <!-- Room Information -->
    <div class="mb-8">
      <h1 class="text-2xl font-bold mb-4">Настройки комнаты</h1>
      <UInput v-model="room.name" label="Room Name" class="mb-4"/>
      <UButton @click="updateRoomName" color="primary">Обновить название и сохранить новые дежурства</UButton>
    </div>

    <!-- Duties List -->
    <div class="mb-8">
      <h2 class="text-xl font-bold mb-4">Дежурства</h2>
      <div v-for="duty in duties" :key="duty.id" class="mb-4 p-4 border rounded-xl flex flex-col gap-2">
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
      <UButton @click="addDuty" color="green">Добавить новое дежурство</UButton>
    </div>

    <!-- Debugging: Display raw data -->
    <div class="mt-8">
      <h2 class="text-xl font-bold mb-4">Debug Data</h2>
      <pre>Room: {{ room }}</pre>
      <pre>Duties: {{ duties }}</pre>
    </div>
  </div>
</template>

<style scoped>
/* Add custom styles if needed */
</style>