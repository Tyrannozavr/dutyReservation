<script setup lang="ts">
import {useAuthStore} from "~/store/auth";
import {useUserStore} from "~/store/user";

const $backend = useBackend()
// const {data: response} = await $backend.$get('/auth/me', {
//   server: false
// })
const authStore = useAuthStore()
const userStore = useUserStore()
// if (!authStore.isAuthenticated)
</script>

<template>
  <div class="profile_container p-8 bg-white rounded-lg shadow-md" v-if="authStore.isAuthenticated">
    <h1 class="text-2xl font-bold text-gray-800 mb-4">User Profile</h1>
    <p class="text-lg text-gray-600">Welcome, {{userStore.username}}</p>
  </div>
  <div class="auth_container p-8 h-full shadow-md" v-else>
    <h2 class="text-2xl font-bold  mb-6">Пожалуйста авторизуйтесь</h2>
    <p class="mb-8">Выберите предпочитаемый метод</p>
    <div class="auth_buttons flex flex-col gap-4 max-w-sm mx-auto">
      <NuxtLink to="/auth" class="w-full">
        <UButton block color="primary" variant="solid" class="w-full">
          <template #leading>
            <UIcon name="i-heroicons-user" />
          </template>
          Вход
        </UButton>
      </NuxtLink>
      <NuxtLink to="/auth/register" class="w-full">
        <UButton block color="gray" variant="solid" class="w-full">
          <template #leading>
            <UIcon name="i-heroicons-user-plus" />
          </template>
          Регистрация
        </UButton>
      </NuxtLink>
      <NuxtLink to="/auth/telegram" class="w-full">
        <UButton block color="blue" variant="outline" class="w-full">
          <template #leading>
            <UIcon name="i-mdi-telegram" />
          </template>
          Войти через телеграм
        </UButton>
      </NuxtLink>
    </div>
  </div>
</template>

<style scoped>

</style>