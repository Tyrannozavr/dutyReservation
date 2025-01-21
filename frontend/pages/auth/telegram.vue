<script setup lang="ts">
import { ref, onMounted } from 'vue';

const user = ref(null);
let tg = null;

onMounted(() => {
  tg = window.Telegram?.WebApp;
  if (tg) {
    // Accessing user information safely
    const initDataUnsafe = tg.initDataUnsafe;
    user.value = initDataUnsafe.user; // Assuming initDataUnsafe has user property
  }
});
</script>

<template>
   Hello, {{ user?.first_name }}
<!--  tg is {{ tg }}-->
</template>

<style scoped>
</style>
   
