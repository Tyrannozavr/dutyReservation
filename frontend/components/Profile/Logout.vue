<script setup lang="ts">
import {useAuthStore} from "~/store/auth";

const authStore = useAuthStore()
const logout = () => authStore.logout()
</script>

<template>
<UIcon @click="logout" name="heroicons-outline:arrow-right-on-rectangle" class="w-8 h-8" />
</template>

<style scoped>

</style>