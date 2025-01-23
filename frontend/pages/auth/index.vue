<template>
  <NuxtLink to="/">Main</NuxtLink>
    <div class="auth-container">
      <h1 class="auth-title">Login</h1>
      <form @submit.prevent="handleSubmit" class="auth-form">
        <div class="form-group">
          <label for="username">Username</label>
          <input type="text" id="username" v-model="username" required/>
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="password" required/>
        </div>
        <button type="submit" class="auth-button">Login</button>
      </form>
    </div>
</template>

<script setup>
import {useAuthStore} from "~/store/auth";
import {useUserStore} from "~/store/user";
import {fetchUserData} from "~/services/authorization";

const toast = useToast()
const $backend = useBackend()
const username = ref('');
const password = ref('');
const authStore = useAuthStore()
const userStore = useUserStore()
const handleSubmit = async () => {
  const { data: tokens, error, status } = await $backend.post('/auth/login', {
    body: {
      username: username.value,
      password: password.value,
    },
  })
  if (status.value === 'success') {
    const { access_token, refresh_token } = tokens.value;
    authStore.setTokens(access_token, refresh_token)
    userStore.setOrigin("web")
    await fetchUserData()
    navigateTo('/profile')
  } else {
    console.error('Login failed:', error.value);
    if (error.value.statusCode === 401) {
      error.value = "Неверный логин или пароль"
    }
    toast.add({
      title: "Ошибка авторизации",
      description: error.value,
      color: "red",
      icon: "i-heroicons-x-circle",
      life: 3000
    })
  }
}
// const handleSubmit = async () => {
//   const payload = {
//     username: username.value,
//     password: password.value,
//   };
//   try {
//     // Send the payload to your backend API
//     // const response = await fetch('/api/auth/login', {
//     //   method: 'POST',
//     //   headers: {
//     //     'Content-Type': 'application/json',
//     //   },
//     //   body: JSON.stringify(payload),
//     // });
//
//     if (response.ok) {
//       const data = await response.json();
//       // Handle successful login (e.g., redirect, store token)
//       console.log('Login successful:', data);
//     } else {
//       // Handle login error
//       console.error('Login failed:', response.statusText);
//     }
//   } catch (error) {
//     console.error('Error during login:', error);
//   }
// };
</script>

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
