<script setup lang="ts">
import {useAuthStore} from "~/store/auth";
import {useUserStore} from "~/store/user";

const authStore = useAuthStore()
const userStore = useUserStore()
const route = useRoute()

const nextPage = ref(null)
onMounted(async () => {
  const tg = window.Telegram?.WebApp
  tg.expand()
  nextPage.value = tg.initDataUnsafe || 'No start_param provided'
})
</script>

<template>
  <ProfileUser v-if="authStore.isAuthenticated"/>
  <ProfileLinks v-else/>
</template>

<style scoped>

</style>