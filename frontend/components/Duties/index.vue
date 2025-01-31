<script setup lang="ts">
import {useAuthStore} from "~/store/auth";

const props = defineProps({
  roomIdentifier: {
    type: String,
    required: true
  }
})
const config = useRuntimeConfig();
const baseUrl = config.public.baseURL
const authStore = useAuthStore();
const websocketsBaseUrl = baseUrl
    .replace('http://', 'ws://')
    .replace('https://', 'wss://')

const messages = ref([{id: 1, text: "Helloworld"}]);
const websocketsUrl = `${websocketsBaseUrl}/room/storage/${props.roomIdentifier}?token=${authStore.accessToken}`

let ws = null
const connect = () => {
  if (ws) {
    ws.close()
  }

  ws = new WebSocket(websocketsUrl);
// Handle incoming messages
  ws.onmessage = (event) => {
    const message = JSON.parse(event.data);
    messages.value.push(message);
  };
}

const sendMessage = () => {
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(messageText.value);
    messageText.value = ''; // Clear input after sending
  } else {
    console.error('WebSocket is not open. Ready state:', ws ? ws.readyState : 'Not Found');
  }
};

</script>

<template>
  <div class="messages">
    url is {{ websocketsUrl }}
    <div v-for="message in messages" :key="message.id" class="message">
      {{ message.text }}
    </div>
  </div>
</template>

<style scoped>

</style>