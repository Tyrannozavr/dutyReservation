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
  } else {
    room.value = null
  }
})

const getRoomToAdd = async () => {
  isOpen.value = true
  try {

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
            <UButton color="gray" variant="ghost" icon="i-heroicons-x-mark-20-solid" class="-my-1"
                     @click="isOpen = false"/>
          </div>
        </template>
        <div class="flex flex-col gap-4">
          <div class="flex flex-col gap-2">
            <div class="text-sm font-medium leading-6 text-gray-900 dark:text-white">
              Идентификатор комнаты
            </div>
            <UInput v-model="roomIdentifier"/>
            <div class="room-skeletons" v-if="!room && roomIdentifier.length > 16">
              <UCard>
                <template #header>
                  <div class="text-base font-semibold leading-6 text-gray-900 dark:text-white">
                    Предпросмотр
                  </div>
                </template>
                <div class="flex flex-col gap-2">
                  <div class="room_name flex flex-row items-center">
                    <span class="mr-2 whitespace-nowrap">Название комнаты:</span>
                    <span class="flex-grow truncate"><USkeleton class="h-4 w-[250px]"/></span>
                  </div>
                  <div class="room_is_multiple_selection flex flex-row gap-2">
                    <span class="">Возможность бронирования нескольких дат:</span>
                    <span>
                      <USkeleton class="h-5 w-5 rounded-full"/>
                    </span>
                  </div>
                  <div class="room_identifier">
                    <div class="mb-1">Идентификатор комнаты:</div>
                    <div><USkeleton class="h-4 w-[250px]"/></div>
                  </div>
                </div>
              </UCard>
            </div>
            <div class="room" v-if="room">
              <UCard>
                <template #header>
                  <div class="text-base font-semibold leading-6 text-gray-900 dark:text-white">
                    Предпросмотр
                  </div>
                </template>
                <div class="flex flex-col gap-2">
                  <div class="room_name flex flex-row items-center">
                    <span class="mr-2 whitespace-nowrap">Название комнаты:</span>
                    <span class="flex-grow truncate">{{ room.name }}</span>
                  </div>
                  <div class="room_is_multiple_selection flex flex-row gap-2">
                    <span class="">Возможность бронирования нескольких дат:</span>
                    <span>
                      <UIcon v-if="room.is_multiple_selection" name="i-heroicons-check-circle" class="text-green-500 -mb-1"/>
                      <UIcon v-else name="i-heroicons-x-circle" class="text-red-500 -mb-1"/>
                    </span>
                  </div>
                  <div class="room_identifier">
                    <div class="mb-1">Идентификатор комнаты:</div>
                    <div>{{ room.identifier }}</div>
                  </div>
                </div>
              </UCard>
            </div>
          </div>
          <div class="flex justify-end">
            <UButton @click="addRoom" :disabled="!room">Добавить</UButton>
          </div>
        </div>
      </UCard>
    </UModal>
  </div>
</template>

<style scoped>

</style>