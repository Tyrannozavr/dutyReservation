<script setup lang="ts">
import {useAuthStore} from "~/store/auth";
import  {useUserStore} from "~/store/user";
const authStore = useAuthStore()
const userStore = useUserStore()
</script>

<template>
  <ProfileUser v-if="authStore.isAuthenticated"/>
  <ProfileLinks v-else/>
</template>

<style scoped>

</style>