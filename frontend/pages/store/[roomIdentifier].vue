<script setup lang="ts">
const route = useRoute()
const roomIdentifier = String(route.params.roomIdentifier)
</script>

<template>
Конкретное голосование {{ roomIdentifier }}
  <Duties :roomIdentifier="roomIdentifier" />
<!--  <DutiesTest :roomIdentifier="roomIdentifier" />-->
</template>

<style scoped>

</style>