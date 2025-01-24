<script setup lang="ts">

</script>
<template>
  <div>
    <UContainer>
      <div class="container min-h-screen">
        <slot/>
        <Footer class="fixed bottom-0 left-0 right-0" />
      </div>
    </UContainer>
    <UNotifications/>
  </div>
</template>
