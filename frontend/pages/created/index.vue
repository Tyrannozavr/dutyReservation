<script setup lang="ts">
import type {RoomOwnerReadList} from "~/types/room";

const $backend = useBackend()
const {data: roomList, refresh} = await $backend.$get<RoomOwnerReadList>('/room')
</script>

<template>
  <UContainer>
    <UCard>
      <template #header>
        <h3 class="text-lg font-semibold flex flex-row">
          Созданные бронирования
          <RoomCreate class="ml-auto" @room-created="refresh"/>
        </h3>
      </template>
      <div class="space-y-4">
        <UCard v-if="!roomList">
          <div class="flex flex-row gap-4 items-center">
            <UIcon name="i-heroicons-arrow-path" class="animate-spin"/>
            <span>Загрузка...</span>
          </div>
        </UCard>
        <UCard v-else-if="roomList.length === 0">
          <div class="flex flex-row gap-4 items-center">
            <UIcon name="i-heroicons-exclamation-circle"/>
            <span>Нет доступных бронирований</span>
          </div>
        </UCard>
        <UCard v-for="room in roomList" :key="room.identifier"
               class="hover:bg-gray-50 transition-colors">
          <NuxtLink
              class="block p-4"
              :to="`/created/${room.identifier}`"
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