<script setup lang="ts">
import type {RoomRead, RoomReadList} from "~/types/room";

const $backend = useBackend()
// {
//   "name": "string",
//     "is_multiple_selection": false,
//     "duty_list": [
//   {
//     "duty_date": "2025-01-25",
//     "name": "string"
//   }
// ]
// } /room/

const {data: roomList, refresh} = await $backend.$get<RoomReadList>('/room')
// const createRoom = async () => {
//   const {data: room} = await $backend.$post('/room')
// }
</script>

<template>
  <UContainer>
    <UCard>
      <template #header>
        <h3 class="text-lg font-semibold flex flex-row">
          Созданные бронирования
          <RoomCreate class="ml-auto" @room-created="refresh" />
        </h3>
      </template>
      <div class="space-y-4">
        <UCard v-for="room in roomList" :key="room.identifier"
               class="hover:bg-gray-50 transition-colors">
          <NuxtLink
              class="block p-4"
              :to="`/store/${room.identifier}`"
          >
            <span class="text-primary-500 font-medium">{{ room.name }}</span>
          </NuxtLink>
        </UCard>
      </div>
    </UCard>
  </UContainer>
</template>

<style scoped>
</style>