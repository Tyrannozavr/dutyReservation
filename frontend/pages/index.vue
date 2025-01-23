<template>
  <UVerticalNavigation :links="links" />

</template>

<script setup lang="ts">
const links = [
  {
    label: 'Auth',
    to: '/auth',
  },
  {
    label: 'Telegram',
    to: '/auth/telegram',
  },
  {
    label: 'Me',
    to: '/profile',
  },
  {
    label: 'Test',
    to: '/test',
  },
]
</script>