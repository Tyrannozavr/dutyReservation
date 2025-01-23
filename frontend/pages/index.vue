<template>
  <div class="index_page">
<!--    <UVerticalNavigation :links="links" />-->
  Hello, world!
    <br>
    <UButton>test</UButton>
  </div>
</template>

<script setup lang="ts">
import {useAuthStore} from "~/store/auth";

const authStore = useAuthStore()
const tokens = computed(() => `access: ${authStore.accessToken}, refresh: ${authStore.refreshToken}`)
// const links = [
//   {
//     label: 'Auth',
//     to: '/auth',
//   },
//   {
//     label: 'Telegram',
//     to: '/auth/telegram',
//   },
//   {
//     label: 'Me',
//     to: '/profile',
//   },
//
//   {
//     label: 'Test',
//     to: '/test',
//   }
// ]
</script>