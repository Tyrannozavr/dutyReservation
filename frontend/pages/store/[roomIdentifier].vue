<script setup lang="ts">
import type {dutyWithUserTypeList} from "~/types/duty";
import {useAuthStore} from "~/store/auth";
import type {RoomRead} from "~/types/room";
const $backend = useBackend()
const route = useRoute()
const roomIdentifier = String(route.params.roomIdentifier)

const {data: room} = await $backend.$get<RoomRead>(`/room/storage/${roomIdentifier}`)

const config = useRuntimeConfig();
const baseUrl = config.public.baseURL
const authStore = useAuthStore();
const webSocketsBaseUrl = baseUrl
    .replace('http://', 'ws://')
    .replace('https://', 'wss://')

const webSocketsUrl = `${webSocketsBaseUrl}/room/${roomIdentifier}/ws/duties?access_token=${authStore.accessToken}`
const duties: Ref<{duties: dutyWithUserTypeList}> = ref([])

let ws: WebSocket | null = null

const connect = () => {
  if (ws) {
    ws.close()
  }
  ws = new WebSocket(webSocketsUrl);
  ws.onmessage = (event) => {
    duties.value = JSON.parse(event.data)
  };
}
onMounted(() => {
  connect()
})
</script>

<template>
  <h1 class="text-xl mb-4">{{ room.name }}</h1>
  <Duties :duties="duties.duties"/>
</template>

<style scoped>

</style>