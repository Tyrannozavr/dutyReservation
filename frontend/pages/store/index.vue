<script setup lang="ts">
const $backend = useBackend()
const {data: roomList, refresh} = await $backend.$get('/room/storage')
</script>

<template>
  <UContainer>
    <UCard>
      <template #header>
        <h3 class="text-lg font-semibold flex flex-row">
          Доступные бронирования
          <RoomAdd class="ml-auto" @add-room="refresh" />
        </h3>
      </template>

      <div class="space-y-4">
        <UCard v-if="!roomList">
          <div class="flex flex-row gap-4 items-center">
            <UIcon name="i-heroicons-arrow-path" class="animate-spin" />
            <span>Загрузка...</span>
          </div>
        </UCard>
        <UCard v-else-if="roomList.length === 0">
          <div class="flex flex-row gap-4 items-center">
            <UIcon name="i-heroicons-exclamation-circle" />
            <span>Нет доступных бронирований</span>
          </div>
        </UCard>
        <RoomUserLine
            v-for="room in roomList" :key="room.identifier" :room="room"
            @delete-room="refresh"
        />
      </div>
    </UCard>
  </UContainer>
</template>

<style scoped>
</style>