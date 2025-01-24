<script setup lang="ts">
import {useUserStore} from "~/store/user";

const userStore = useUserStore()
</script>
<template>
  <div class="profile_container p-8 bg-white dark:bg-gray-900 rounded-lg shadow-md">
    <h1 class="text-2xl font-bold mb-4 flex justify-between">Профиль <ProfileLogout class="ml-auto"/></h1>

    <p class="text-lg">Добро пожаловать, {{userStore.first_name}}</p>
  </div>
</template>
<style scoped>

</style>