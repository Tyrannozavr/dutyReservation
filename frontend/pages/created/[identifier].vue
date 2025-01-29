<script setup lang="ts">
import type { RoomOwnerRead } from "~/types/room";
import type {DutiesWithUserResponse, dutyWithUserTypeList} from "~/types/duty";

const route = useRoute();
const $backend = useBackend();

const roomIdentifier = route.params.identifier;

// Fetch room data
const { data: roomData } = await $backend.$get<RoomOwnerRead>(`/room/owner/${roomIdentifier}`);
const room = reactive({ ...roomData.value });
// console.log("room is", room, 2, room.value)
// console.log("room name is", roomData.value)
// Fetch duties data
const { data: dutiesData } = await $backend.$get<DutiesWithUserResponse>(`/duty/${roomIdentifier}`);
// console.log(dutiesData)
// console.log("Hello")
// console.log(dutiesData.value)
const duties = reactive([...dutiesData.value["duties"]]);

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
    id: duties.length + 1, // Temporary ID (replace with backend-generated ID)
    user: null,
    date: "2025-01-01", // Default date
    name: "", // Default name
  };
  duties.push(newDuty);
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
  console.log("remove", dutyId)
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
      <h1 class="text-2xl font-bold mb-4">Room Information</h1>
      <UInput v-model="room.name" label="Room Name" class="mb-4" />
      <UButton @click="updateRoomName" color="primary">Update Room Name</UButton>
    </div>

    <!-- Duties List -->
    <div class="mb-8">
      <h2 class="text-xl font-bold mb-4">Duties</h2>
      <div v-for="duty in duties" :key="duty.id" class="mb-4 p-4 border rounded">
        <UInput v-model="duty.name" label="Duty Name" class="mb-2" />
        <UInput v-model="duty.date" label="Date" type="date" class="mb-2" />
        <div class="flex gap-2">
          <UButton @click="updateDuty(duty)" color="primary">Update Duty</UButton>
          <UButton @click="removeDuty(duty.id)" color="red">Remove Duty</UButton>
        </div>
      </div>
      <UButton @click="addDuty" color="green">Add New Duty</UButton>
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