<script setup lang="ts">
const $backend = useBackend()
const {data: response} = await $backend.$get('/auth/me', {
  server: false
})
const userStore = ref({getUserFio: null, username: "Hello, world"})
</script>

<template>
  <NuxtLink to="/">Home</NuxtLink>
  <div class="flex flex-col items-center justify-center p-4 bg-white rounded-lg shadow-md">
    <div class="text-xl font-semibold text-gray-800 mb-2">
      User is {{ userStore.getUserFio }}
    </div>
    <div class="text-gray-600 mb-1">
      username is {{ userStore.username }}
    </div>
    <div class="text-sm text-gray-500">
      reached data is {{ response }}
    </div>
  </div>
</template>

<style scoped>

</style>