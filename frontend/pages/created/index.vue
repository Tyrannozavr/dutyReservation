<script setup lang="ts">
import type {RoomReadList} from "~/types/room";

const $backend = useBackend()
const {data: roomList, refresh} = await $backend.$get<RoomReadList>('/room')
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