<script setup lang="ts">
import {useAuthStore} from "~/store/auth";

const authStore = useAuthStore()
</script>

<template>
  <ProfileUser v-if="authStore.isAuthenticated"/>
  <ProfileLinks v-else/>
</template>

<style scoped>

</style>