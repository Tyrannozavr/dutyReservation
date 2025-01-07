<script setup lang="ts">
// const people = []
const props = defineProps({
  people: {
    type: Array as PropType<object[]>,
    required: true,
  },
});
const people = computed(() => props.people)
</script>

<template>
  <UTable :rows="people" />
</template>

