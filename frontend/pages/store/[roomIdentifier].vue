<script setup lang="ts">
import type {dutyWithUserType, dutyWithUserTypeList} from "~/types/duty";
import {useAuthStore} from "~/store/auth";
import type {RoomRead} from "~/types/room";
const $backend = useBackend()
const $client = useClientFetch()
const route = useRoute()
const roomIdentifier = String(route.params.roomIdentifier)
const {data: room} = await $backend.$get<RoomRead>(`/room/storage/${roomIdentifier}`)

const config = useRuntimeConfig();
const baseUrl = config.public.baseURL
const authStore = useAuthStore();
const webSocketsBaseUrl = baseUrl
    .replace('http://', 'ws://')
    .replace('https://', 'wss://')

const webSocketsUrl = `${webSocketsBaseUrl}/duties/ws/${roomIdentifier}/duties?access_token=${authStore.accessToken}`
const duties: Ref<dutyWithUserTypeList> = ref([])
let ws: WebSocket | null = null

const connect = () => {
  if (ws) {
    ws.close()
  }
  ws = new WebSocket(webSocketsUrl);
  ws.onmessage = (event) => {
    duties.value = JSON.parse(event.data).duties
  };
}

const reserveDuty = async (dutyId: number) => {
  await $client.$patch(`/room/${roomIdentifier}/duties/${dutyId}`)
}
const releaseDuty = async (dutyId: number) => {
  await $client.$delete(`/room/${roomIdentifier}/duties/${dutyId}`)
}

onMounted(() => {
  connect()
})
console.log("room connected is", room)
</script>

<template>
  <h1 class="text-xl mb-4" v-if="room && room.name">{{ room.name }}</h1>
  <Duties
      :duties="duties"
      @reserveDuty="reserveDuty"
      @releaseDuty="releaseDuty"
  />
</template>

<style scoped>

</style>