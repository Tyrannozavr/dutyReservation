<script setup lang="ts">
import type {RoomRead} from "~/types/room";

const emits = defineEmits(["addRoom"])

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

const addRoom = async () => {
  try {
    const response = await clientFetch.$post<RoomRead>(urlRequest.value)
    if (response.identifier) {
      emits('addRoom')
      isOpen.value = false
      $toast.add({
        title: 'Добавление комнаты',
        description: 'Комната добавлена',
        color: 'green'
      })
    }
  } catch (e) {
    $toast.add({
      title: 'Добавление комнаты',
      description: 'Ошибка при добавлении комнаты',
      color: 'red'
    })
  }


}
</script>

<template>
  <div>
    <UButton @click="isOpen = true">Добавить</UButton>
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
            <UInput v-model="roomIdentifier" />
            <div class="text-sm text-gray-500 dark:text-gray-400 mb-2">
              Идентификатор комнаты должен быть длиннее 16 символов
            </div>
            <div class="room" v-if="roomIdentifier.length > 16">
              <UCard>
                <template #header>
                  <div class="text-base font-semibold leading-6 text-gray-900 dark:text-white">
                    Предпросмотр
                  </div>
                </template>
                <div class="flex flex-col gap-2">
                  <div class="room_name flex flex-row items-center">
                    <span class="mr-2 whitespace-nowrap">Название комнаты:</span>
                    <span class="flex-grow truncate">
                      <template v-if="room">
                        {{ room.name }}
                      </template>
                      <template v-else>
                        <USkeleton class="h-4 w-[250px]"/>
                      </template>
                    </span>
                  </div>
                  <div class="room_is_multiple_selection flex flex-row gap-2">
                    <span class="">Возможность бронирования нескольких дат:</span>
                    <span>
                      <template v-if="room">
                        <UIcon v-if="room.is_multiple_selection" name="i-heroicons-check-circle" class="text-green-500 -mb-1"/>
                        <UIcon v-else name="i-heroicons-x-circle" class="text-red-500 -mb-1"/>
                      </template>
                      <template v-else>
                        <USkeleton class="h-5 w-5 rounded-full"/>
                      </template>

                    </span>
                  </div>
                  <div class="room_identifier">
                    <div class="mb-1">Идентификатор комнаты:</div>
                    <template v-if="room">
                      {{ room.identifier }}
                    </template>
                    <template v-else>
                      <USkeleton class="h-4 w-[250px]"/>
                    </template>
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