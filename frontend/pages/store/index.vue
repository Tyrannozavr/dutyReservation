<script setup lang="ts">
const voytingList = ref([
  {number: "234234", name: "test"}
])
</script>

<template>
  <UContainer>
    <UCard>
      <template #header>
        <h3 class="text-lg font-semibold">
          Доступные бронирования
        </h3>
      </template>

      <div class="space-y-4">
        <UCard v-for="voting in voytingList" :key="voting.number"
               class="hover:bg-gray-50 transition-colors">
          <NuxtLink
            class="block p-4"
            :to="`/store/${voting.number}`"
          >
            <span class="text-primary-500 font-medium">{{ voting.name }}</span>
          </NuxtLink>
        </UCard>
      </div>
    </UCard>
  </UContainer>
</template>

<style scoped>
</style>