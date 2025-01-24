<script setup lang="ts">
const tg = ref(null)
const user = ref(null)

onMounted(() => {
   // tg.value = window.Telegram?.WebApp
   // user.value = tg.value?.initDataUnsafe?.user
})
</script>
<template>
  tg is {{tg}}
</template>
<style scoped>
</style>
