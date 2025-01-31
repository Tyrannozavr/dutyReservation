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
const Link = `${window.location.origin}/store?roomIdentifier=${props.roomIdentifier}`

const copyLink = () => {
  const url = Link
  navigator.clipboard.writeText(url)
  toast.add({
    title: 'Ссылка приглашение скопирована',
    color: 'green',
    timeout: 2000
  })
}
</script>

<template>
<div class="flex gap-2">
  <UButton
    icon="i-heroicons-clipboard"
    color="gray"
    variant="ghost"
    size="sm"
    @click="copyLink"
  />
  <UButton
    icon="i-simple-icons-telegram"
    color="blue"
    variant="ghost"
    size="sm"
    :to="`https://t.me/share/url?url=${Link}`"
    target="_blank"
  />
  <UButton
    icon="i-simple-icons-whatsapp"
    color="green"
    variant="ghost"
    size="sm"
    :to="`https://api.whatsapp.com/send?text=${Link}`"
    target="_blank"
  />
  <UButton
    icon="i-simple-icons-vk"
    color="blue"
    variant="ghost"
    size="sm"
    :to="`https://vk.com/share.php?url=${Link}`"
    target="_blank"
  />
  <UButton
    icon="i-simple-icons-odnoklassniki"
    color="orange"
    variant="ghost"
    size="sm"
    :to="`https://connect.ok.ru/offer?url=${Link}`"
    target="_blank"
  />
</div>
</template>

<style scoped>

</style>