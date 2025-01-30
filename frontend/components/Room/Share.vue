<script setup lang="ts">
const props = defineProps({
      roomIdentifier: {
        type: String,
        required: true
      }
    }
)
const route = useRoute()
const toast = useToast()
const copyLink = () => {
  const url = `${window.location.origin}/store?roomIdentifier=${props.roomIdentifier}`
  navigator.clipboard.writeText(url)
  toast.add({
    title: 'Ссылка приглашение скопирована',
    color: 'green',
    timeout: 2000
  })
}
</script>

<template>
  <div>
    <UButton icon="i-heroicons-share" color="primary" variant="ghost" size="sm" @click="copyLink"></UButton>
  </div>
</template>

<style scoped>

</style>