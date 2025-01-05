<template>
  <NuxtPage />
  <ClientOnly>
    <MiniApp />
  </ClientOnly>
</template>

<script setup lang="ts">
import MiniApp from '~/components/MiniApp.vue'
</script>