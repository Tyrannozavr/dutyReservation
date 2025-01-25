<script setup lang="ts">
const isOpen = ref(false)

</script>

<template>
<div>
  <UButton @click="isOpen  = true">Создать</UButton>
  <UModal v-model="isOpen">
    <div class="p-4">
      <!--          <Placeholder class="h-48" />-->
      Hello, creation
    </div>
  </UModal>
</div>
</template>

<style scoped>

</style>