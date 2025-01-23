<script setup lang="ts">

import {useAuthStore} from "~/store/auth";

const authStore = useAuthStore()
Store.setState("Test data in store ")
authStore.setTokens("123", "456")
</script>

<template>
  <NuxtLink to="/">Main</NuxtLink>
</template>

<style scoped>

</style>