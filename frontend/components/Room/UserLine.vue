<script setup lang="ts">
defineProps({
  room: {
    type: Object,
    required: true
  }
})
const emits = defineEmits(["deleteRoom"])
const isModelActive = ref(false)
const clientFetch = useClientFetch()
const deleteRoom = async (identifier: string) => {
  await clientFetch.$delete(`/room/storage/${identifier}`, )
  isModelActive.value = false
  emits("deleteRoom")
}
</script>

<template>
  <UCard :key="room.identifier"
         class="hover:bg-gray-50 transition-colors">
    <div class="flex flex-row justify-between">
      <NuxtLink
          class="block p-4"
          :to="`/store/${room.identifier}`"
      >
        <span class="text-primary-500 font-medium">{{ room.name }}</span>
      </NuxtLink>
      <UIcon name="heroicons-outline:trash" class="text-red-500 w-8 h-8 mt-2 hover:cursor-pointer"
             @click="isModelActive = true"

      />
      <UModal v-model="isModelActive">
        <template #activator>
          <UIcon name="heroicons-outline:trash" class="text-red-500 w-8 h-8 mt-2 hover:cursor-pointer"/>
        </template>
        <UCard>
          <template #header>
            <h1 class="text-xl font-bold">Delete Room</h1>
          </template>
          <p>Are you sure you want to delete this room?</p>
          <template #footer>
            <div class="flex flex-row justify-end">
              <UButton color="red" variant="solid" @click="deleteRoom(room.identifier)">Delete</UButton>
            </div>
          </template>
        </UCard>
      </UModal>
    </div>
  </UCard>
</template>

<style scoped>

</style>