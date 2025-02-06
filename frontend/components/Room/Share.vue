<script setup lang="ts">
const props = defineProps({
      roomIdentifier: {
        type: String,
        required: true
      }
    }
)
const toast = useToast()
const Link = `${window.location.origin}/store?roomIdentifier=${props.roomIdentifier}`
ф// const Link = `https://t.me/DutyReservationBot/reservationpage/auth/telegram?redirect=/store?roomIdentifier=${props.roomIdentifier}`

const copyLink = () => {
  navigator.clipboard.writeText(Link)
  toast.add({
    title: 'Ссылка приглашение скопирована',
    color: 'green',
    timeout: 2000
  })
}
const copyIdentifier = () => {
  navigator.clipboard.writeText(props.roomIdentifier)
  toast.add({
    title: 'Идентификатор скопирован',
    color: 'green',
    timeout: 2000
  })
}

</script>

<template>
  <UCard class="w-full">
    <template #header>
      Чтобы пригласить кого нибудь в комнату поделитесь ссылкой
      или сообщите ему идентификатор комнаты
    </template>
    <UButton icon="i-heroicons-clipboard-document-list-20-solid"
             :label="props.roomIdentifier" @click="copyIdentifier"
             class="mb-4"
    />
    <div class="flex gap-2">
      <UButton
          icon="i-heroicons-clipboard"
          color="gray"
          variant="ghost"
          size="xl"
          @click="copyLink"
      />
      <UButton
          icon="i-simple-icons-telegram"
          color="blue"
          variant="ghost"
          size="xl"
          :to="`https://t.me/share/url?url=${Link}`"
          target="_blank"
      />
      <UButton
          icon="i-simple-icons-whatsapp"
          color="green"
          variant="ghost"
          size="xl"
          :to="`https://api.whatsapp.com/send?text=${Link}`"
          target="_blank"
      />
      <UButton
          icon="i-simple-icons-vk"
          color="blue"
          variant="ghost"
          size="xl"
          :to="`https://vk.com/share.php?url=${Link}`"
          target="_blank"
      />
      <UButton
          icon="i-simple-icons-odnoklassniki"
          color="orange"
          variant="ghost"
          size="xl"
          :to="`https://connect.ok.ru/offer?url=${Link}`"
          target="_blank"
      />
    </div>
  </UCard>

</template>

<style scoped>

</style>