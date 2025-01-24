<script setup lang="ts">
import {useUserStore} from "~/store/user";

const userStore = useUserStore()
</script>
<template>
  <div class="profile_container p-8 bg-white dark:bg-gray-900 rounded-lg shadow-md">
    <h1 class="text-2xl font-bold mb-8 flex justify-between">Профиль <ProfileLogout class="ml-auto"/></h1>
    <p class="text-lg mb-4">Добро пожаловать, {{userStore.first_name}} {{userStore.last_name}}</p>
    <p class="text-lg mb-4">Юзернейм: {{userStore.username}}</p>
    <p class="text-lg mb-4 flex flex-row">Аватар:
      <UAvatar :src="userStore.photo_url" alt="avatar" size="md" class="ml-4" v-if="userStore.photo_url" />
    </p>
  </div>
</template>

<style scoped>

</style>