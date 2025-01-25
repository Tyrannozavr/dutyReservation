<script setup lang="ts">
import type {RoomRead} from "~/types/room";

const clientFetch = useClientFetch()
const $toast = useToast()
const roomIdentifier = ref('')
const isOpen = ref(false)
const room = ref<RoomRead | null>(null)

const urlRequest = computed(() => `/room/storage/${roomIdentifier.value}`)



watch(roomIdentifier, async () => {
  if (roomIdentifier.value?.length > 16) {
      room.value = await clientFetch.get<RoomRead>(urlRequest.value).catch(() => null)
  }
})

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
            <UButton color="gray" variant="ghost" icon="i-heroicons-x-mark-20-solid" class="-my-1" @click="isOpen = false"/>
          </div>
        </template>
        <div class="flex flex-col gap-4">
          <div class="flex flex-col gap-2">
            <div class="text-sm font-medium leading-6 text-gray-900 dark:text-white">
              Идентификатор комнаты
            </div>
            <UInput v-model="roomIdentifier" />
            room data identifier is {{roomIdentifier}}
            <br>
            is {{room}}
            <USkeleton class="h-4 w-[250px]" />
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