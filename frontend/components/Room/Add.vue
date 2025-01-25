<script setup lang="ts">
const $backend = useBackend()
const $toast = useToast()
const roomIdentifier = ref()
const isOpen = ref(false)
const getRoomToAdd = async () => {
  isOpen.value = true
  try {
    // if (room) {
      // navigateTo(`/rooms/${room.identifier}`)
    // }
  } catch (error) {
  }
}
const addRoom = async () => {
  isOpen.value = false
  $toast.add({
    title: 'Добавление комнаты',
    description: 'Комната добавлена',
    color: 'green'
  })
}
</script>

<template>
  <div>
    <UButton @click="getRoomToAdd">Добавить</UButton>
    <UModal v-model="isOpen">
      <UCard>
        <template #header>
          <div class="flex justify-between">
            <div class="text-base font-semibold leading-6 text-gray-900 dark:text-white">
              Добавить комнату
            </div>
            <UButton color="gray" variant="ghost" icon="i-heroicons-x-mark-20-solid" class="-my-1" @click="getRoomToAdd" />
          </div>
        </template>
        <div class="flex flex-col gap-4">
          <div class="flex flex-col gap-2">
            <div class="text-sm font-medium leading-6 text-gray-900 dark:text-white">
              Идентификатор комнаты
            </div>
            <UInput v-model="roomIdentifier" />
          </div>
          <div class="flex justify-end">
            <UButton @click="addRoom">Добавить</UButton>
          </div>
        </div>
      </UCard>
    </UModal>
  </div>
</template>

<style scoped>

</style>