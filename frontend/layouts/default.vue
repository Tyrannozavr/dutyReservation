<script setup lang="ts">
// import {useAuthStore} from "~/store/auth";

// onMounted(() => {
//   const tg = window.Telegram?.WebApp
//   const authStore = useAuthStore()
//   const route = useRoute()
//   if (tg && tg.initData && (!authStore.isAuthenticated) && route.path !== "/auth/telegram") {
//     navigateTo('/auth/telegram?redirect=' + route.fullPath)
//   }
// })
</script>
<template>
  <div>
    <UNotifications position="left-top" />
    <UContainer>
      <div class="container min-h-screen pt-4 pb-16">
        <slot/>
        <Footer class="fixed bottom-0 left-0 right-0" />
      </div>
    </UContainer>
  </div>
</template>
