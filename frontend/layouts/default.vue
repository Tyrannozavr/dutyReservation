<script setup lang="ts">
const links = [
  {
    icon: 'heroicons-outline:home',
    to: '/'
  },
  {
    icon: 'heroicons-outline:collection',
    to: '/voyting'
  },
  {
    icon:  'heroicons-outline:user-circle',
    to: "/profile"
  }
]
</script>
<template>
  <div>
    <UContainer>
      <div class="container min-h-screen">
        <slot/>
        <FooterNavigations :links="links" class="fixed bottom-0 left-0 right-0"/>
      </div>

    </UContainer>
    <UNotifications/>
  </div>
</template>
