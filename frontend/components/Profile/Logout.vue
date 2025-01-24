<script setup lang="ts">
import {useAuthStore} from "~/store/auth";

const authStore = useAuthStore()
const logout = () => authStore.logout()
</script>

<template>
<UIcon @click="logout" name="heroicons-outline:arrow-right-on-rectangle" class="w-10 h-10" />
</template>

<style scoped>

</style>