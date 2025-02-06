<script setup lang="ts">
import {useAuthStore} from "~/store/auth";
import {useUserStore} from "~/store/user";
import {fetchUserData} from "~/services/authorization";
import type {TokenResponse} from "~/types/auth.js";
const route = useRoute()
const router = useRouter()

const nextPage = route.query.redirect
const toast = useToast()
const $client = useClientFetch()
const username = ref('');
const password = ref('');
const authStore = useAuthStore()
const userStore = useUserStore()
const handleSubmit = async () => {
  try {
    let response = await $client.post<TokenResponse>('/auth/login', {
      body: {
        username: username.value,
        password: password.value,
      },
    })
    if (response.access_token) {
      let access_token = response.access_token
      let refresh_token = response.refresh_token
      authStore.login(access_token, refresh_token)
      userStore.setOrigin("web")
      await fetchUserData()
      if (nextPage) {
        await router.push(nextPage.toString())
      } else {
        await router.push("/profile")
      }
    } else {
      console.error('Login failed:', response);
      if (response.status === 401) {
      toast.add({
        title: "Ошибка авторизации",
        description: "Неверный логин или пароль",
        color: "red",
        icon: "i-heroicons-x-circle",
        life: 3000
      })
      }

    }

  } catch (e) {
    toast.add({
      title: "Ошибка авторизации",
      description: `Error auth ${e}`,
      color: "red",
      icon: "i-heroicons-x-circle",
      life: 3000
    })
    console.error("error", e)
  }}
</script>
<template>
  <NuxtLink to="/" class="text-blue-500 hover:text-blue-700 mb-4 inline-block">
    <UIcon name="i-heroicons-home" class="mr-1" />
    Main
  </NuxtLink>
  <div class="max-w-md mx-auto bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8">
    <h1 class="text-2xl font-bold text-center text-gray-800 dark:text-white mb-6">Вход</h1>
    <form @submit.prevent="handleSubmit" class="space-y-6">
      <UFormGroup label="Username">
        <UInput
          v-model="username"
          placeholder="Enter your username"
          icon="i-heroicons-user"
          required
        />
      </UFormGroup>
      <UFormGroup label="Пароль">
        <UInput
          v-model="password"
          type="password"
          placeholder="Enter your password"
          icon="i-heroicons-lock-closed"
          required
        />
      </UFormGroup>
      <UButton
        type="submit"
        color="primary"
        block
        class="mt-4"
      >
        <UIcon name="i-heroicons-arrow-right-on-rectangle" class="mr-1" />
        Войти
      </UButton>
    </form>
  </div>
</template>
<style scoped>
.auth-container {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.auth-title {
  text-align: center;
  margin-bottom: 20px;
}

.auth-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  margin-bottom: 5px;
}

.form-group input {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.auth-button {
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.auth-button:hover {
  background-color: #0056b3;
}
</style>
