<template>
  <div>
    <h1>WebSocket Chat</h1>
    <form @submit.prevent="sendMessage">
      <label>Item ID:
        <input type="text" v-model="itemId" autocomplete="off" />
      </label>
      <label>Token:
        <input type="text" v-model="token" autocomplete="off" />
      </label>
      <button @click="connect">Connect</button>
      <hr>
      <label>Message:
        <input type="text" v-model="messageText" autocomplete="off" />
      </label>
      <button type="submit">Send</button>
    </form>
    <ul id='messages'>
      <li v-for="(message, index) in messages" :key="index">{{ message }}</li>
    </ul>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import {useAuthStore} from "~/store/auth";
const props = defineProps({
  roomIdentifier: {
    type: String,
    required: true
  }
})
const itemId = ref('foo');
const token = ref('some-key-token');
const messageText = ref('');
const messages = ref([]);
let ws = null;

const connect = () => {
  if (ws) {
    ws.close(); // Close existing connection if there is one
  }

  // const url = `ws://localhost:8000/items/${itemId.value}/ws?token=${token.value}`;
  const config = useRuntimeConfig();
  const baseUrl = config.public.baseURL
  const authStore = useAuthStore();
  const websocketsBaseUrl = baseUrl
      .replace('http://', 'ws://')
      .replace('https://', 'wss://')

      // /room/{room_identifier}/ws/duties
  const url = `${websocketsBaseUrl}/room/${props.roomIdentifier}/ws/duties?token=${authStore.accessToken}`
  ws = new WebSocket(url);

  ws.onmessage = (event) => {
    console.log("Got message", event.data)
    messages.value.push(event.data);
  };

  ws.onclose = () => {
    console.log('WebSocket connection closed');
  };

  ws.onerror = (error) => {
    console.error('WebSocket error:', error);
  };
};

const sendMessage = () => {
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(messageText.value);
    messageText.value = ''; // Clear input after sending
  } else {
    console.error('WebSocket is not open. Ready state:', ws ? ws.readyState : 'Not Found');
  }
};
// onMounted(() => {
//   connect();
// });
</script>

<style scoped>
/* Add any necessary styles here */
</style>
