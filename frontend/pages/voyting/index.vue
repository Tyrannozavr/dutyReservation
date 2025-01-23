<script setup lang="ts">
const voytingList = ref([
  {number: "234234", name: "test"}
])
</script>

<template>
Список голосований пользователя
  <div class="voyting-container">
    <div class="voyte_contaner" v-for="voyting in voytingList">
      <NuxtLink class="py-3" :to="`/voyting/${voyting.number}`">{{voyting.name}}</NuxtLink>
    </div>
  </div>
</template>

<style scoped>

</style>