<script setup lang="ts">
const $backend = useBackend()
import  type {RoomList} from "~/types/room";
const {data: roomList} = await $backend.$get<RoomList>('/room/storage')

</script>

<template>
  <UContainer>
    <UCard>
      <template #header>
        <h3 class="text-lg font-semibold flex flex-row">
          Доступные бронирования
          <RoomAdd class="ml-auto"/>
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