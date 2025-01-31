<script setup lang="ts">
const props = defineProps<{
  id: number
}>()
const $client = useClientFetch()
const toast = useToast()

const deleteRoom = async () => {
  try {
    const response = await $client.$delete(`/room/${props.id}`)
    if (response) {
      toast.add({
        title: 'Успешно',
        description: 'Дежурство удалено',
        color: 'green'
      })
      navigateTo('/created')
    }
  } catch (e) {
    console.error(e)
    toast.add({
      title: 'Ошибка',
      description: 'Не удалось удалить дежурство',
      color: 'red'
    })
  }
}
const isOpen = ref(false)
</script>

<template>
  <div>
    <UButton @click="isOpen = true" color="red">Удалить комнату</UButton>
    <UModal v-model="isOpen">
      <UCard>
        <template #header>
          <h1 class="text-center">Вы уверены?</h1>
        </template>
        <div class="flex flex-row justify-evenly">
          <UButton @click="isOpen = false" color="gray">Отмена</UButton>
          <UButton @click="deleteRoom" color="red">Удалить
          </UButton>
        </div>
      </UCard>
    </UModal>
  </div>
</template>

<style scoped>

</style>