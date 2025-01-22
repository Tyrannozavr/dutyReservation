<script setup lang="ts">
import {useUserStore} from "~/store/user";

// const $backend = Fetch()
// const store = useUserData()
// const store = {
//   accessToken: "Helloworld"
// }
// const {data: response} = await useFetch('http://localhost:8000/api/users/info', {
//   server: false,
//   onRequest({request, options}) {
//     // Set the request headers
//     // note that this relies on ofetch >= 1.4.0 - you may need to refresh your lockfile
//     options.headers.set('Authorization', `Bearer ${store.accessToken}`)
//   },
// })
// console.log('hello', response)
// const {data: response} = await useNuxtApp().$api('/users/info')
const $backend = useBackend()
const {data: response} = await $backend.$get('/auth/me', {
  server: false
})
const userStore = ref({getUserFio: null, username: "Hello, world"})
</script>

<template>
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