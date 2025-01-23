<template>
  <UVerticalNavigation :links="links" />
  <br>
  The tokens are {{tokens}}
</template>

<script setup lang="ts">
import {useAuthStore} from "~/store/auth";

const authStore = useAuthStore()
// const tokens = `access: ${authStore.accessToken}, refresh: ${authStore.refreshToken}`
const tokens = computed(() => `access: ${authStore.accessToken}, refresh: ${authStore.refreshToken}`)
const links = [
  {
    label: 'Auth',
    to: '/auth',
  },
  {
    label: 'Telegram',
    to: '/auth/telegram',
  },
  {
    label: 'Me',
    to: '/profile',
  },

  {
    label: 'Test',
    to: '/test',
  }
]
</script>