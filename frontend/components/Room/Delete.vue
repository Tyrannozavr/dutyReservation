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
</script>

<template>
  <UButton @click="deleteRoom" color="red">Удалить дежурство</UButton>
</template>

<style scoped>

</style>