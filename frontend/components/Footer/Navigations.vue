<script setup lang="ts">
const iconClass = "w-7 h-7"
const links = [
  {
    icon: 'heroicons-outline:home',
    to: '/',
    iconClass,
  },
  {
    icon: 'heroicons-outline:collection',
    to: '/store',
    iconClass,
  },
  {
    icon: 'heroicons-outline:server-stack',
    to: '/created',
    iconClass,
  },
  {
    icon:  'heroicons-outline:user-circle',
    to: "/profile",
    iconClass,
  }
]
const route = useRoute()
const linkClass  = (link: string) => {
  if (link !== '/') {
    return route.path.includes(link) ? 'text-primary' : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200'
  } else {
    return route.path === link ? 'text-primary' : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200'
  }
}
</script>

<template>
  <UContainer class="bg-white shadow ring-1 ring-gray-200
  dark:bg-gray-900 dark:ring-gray-800">
    <nav class="flex justify-evenly py-4">
      <ULink
        v-for="link in links"
        :key="link.to"
        :to="link.to"
        :class="linkClass(link.to)"
      >
        <UIcon :name="link.icon" class="w-8 h-8" />
      </ULink>
    </nav>
  </UContainer>
</template>

<style scoped>

</style>
<!--active-class="text-primary"-->
<!--inactive-class="text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200"-->