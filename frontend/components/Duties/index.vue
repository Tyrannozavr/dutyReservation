<script setup lang="ts">
import {useAuthStore} from "~/store/auth";
import type {dutyWithUserTypeList} from "~/types/duty";

const props = defineProps({
  roomIdentifier: {
    type: String,
    required: true
  }
})
const config = useRuntimeConfig();
const baseUrl = config.public.baseURL
const authStore = useAuthStore();
const webSocketsBaseUrl = baseUrl
    .replace('http://', 'ws://')
    .replace('https://', 'wss://')
const duties: Ref<dutyWithUserTypeList> = ref([])
const webSocketsUrl = `${webSocketsBaseUrl}/room/${props.roomIdentifier}/ws/duties?access_token=${authStore.accessToken}`

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
  <div class="messages">
    <div v-for="duty in duties" :key="duty.id">
      {{ duty }}
    </div>
  </div>
</template>

<style scoped>

</style>