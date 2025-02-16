<script setup lang="ts">
import {useAuthStore} from "~/store/auth";
import {useUserStore} from "~/store/user";
import {fetchUserData} from "~/services/authorization";
import type {TokenResponse} from "~/types/auth.js";

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const userStore = useUserStore()

const nextPage = route.query.redirect
const toast = useToast()
const $client = useClientFetch()

const state = reactive({
  username: '',
  password: '',
  passwordRepeat: '',
  firstName: '',
  lastName: ''
})

const passwordMatch = computed(() => state.password === state.passwordRepeat)

const validate = async (state: any) => {
  const errors = []
  if (!state.username) errors.push({path: 'username', message: 'Обязательное поле'})
  if (await isUsernameAlreadyTaken()) errors.push({path: 'username', message: 'Это имя уже занято'})
  if (!state.password) errors.push({path: 'password', message: 'Обязательное поле'})
  if (!state.passwordRepeat) errors.push({path: 'passwordRepeat', message: 'Обязательное поле'})
  if (!passwordMatch.value) errors.push({path: 'passwordRepeat', message: 'Пароли не совпадают'})
  if (!state.firstName) errors.push({path: 'firstName', message: 'Обязательное поле'})
  if (!state.lastName) errors.push({path: 'lastName', message: 'Обязательное поле'})
  return errors
}

const isUsernameAlreadyTaken = () => {

  return $client.get('users/check-username', {
    query: {
      username: state.username
    }
  }).then((response) => {
    return response
  }).catch((error) => {
    console.error('Error checking username:', error)
    return false
  })
}

const handleSubmit = async () => {
  try {
    let response = await $client.post<TokenResponse>('/auth/register', {
      body: {
        "username": state.username,
        "first_name": state.firstName,
        "last_name": state.lastName,
        "password": state.password
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
  }
}
</script>

<template>
  <NuxtLink to="/" class="text-blue-500 hover:text-blue-700 mb-4 inline-block">
    <UIcon name="i-heroicons-home" class="mr-1"/>
    Главная
  </NuxtLink>
  <div class="max-w-md mx-auto bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8">
    <h1 class="text-2xl font-bold text-center text-gray-800 dark:text-white mb-6">Регистрация</h1>
    <UForm :state="state" :validate="validate" @submit.prevent="handleSubmit" class="space-y-6">
      <UFormGroup label="Username" name="username">
        <UInput
            v-model="state.username"
            placeholder="Введите имя пользователя"
            icon="i-heroicons-user"
            required
        />
      </UFormGroup>
      <UFormGroup label="Имя" name="firstName">
        <UInput
            v-model="state.firstName"
            placeholder="Введите имя"
            icon="i-heroicons-user"
            required
        />
      </UFormGroup>
      <UFormGroup label="Фамилия" name="lastName">
        <UInput
            v-model="state.lastName"
            placeholder="Введите фамилию"
            icon="i-heroicons-user"
            required
        />
      </UFormGroup>

      <UFormGroup label="Пароль" name="password">
        <UInput
            v-model="state.password"
            type="password"
            placeholder="Введите пароль"
            icon="i-heroicons-lock-closed"
            required
        />
      </UFormGroup>
      <UFormGroup label="Повторите пароль" name="passwordRepeat">
        <UInput
            v-model="state.passwordRepeat"
            type="password"
            placeholder="Повторите пароль"
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
        Зарегистрироваться
      </UButton>
    </UForm>
  </div>
</template>

<style scoped>

</style>