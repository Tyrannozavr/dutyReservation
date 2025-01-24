<script setup lang="ts">

</script>

<template>
  <div class="auth_container p-8 h-full shadow-md">
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