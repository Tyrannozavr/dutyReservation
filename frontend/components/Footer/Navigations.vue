<script setup lang="ts">
defineProps<{
  links: Array<{
    to: string
    icon: string
  }>
}>()
</script>

<template>
  <UContainer>
    <nav class="flex justify-evenly py-4">
      <NuxtLink
        v-for="link in links"
        :key="link.to"
        :to="link.to"
        class="text-gray-600 hover:text-primary-500 transition-colors"
      >
        <UIcon :name="link.icon" class="w-8 h-8" />
      </NuxtLink>
    </nav>
  </UContainer>
</template>

<style scoped>

</style>
