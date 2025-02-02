<script setup lang="ts">
import type {dutyWithUserType} from "~/types/duty";

const props = defineProps<{
  duty: dutyWithUserType
}>()
</script>

<template>
  <div>
    <div>{{duty.id}}</div>
    <div>{{duty.name}}</div>
    <div>{{duty.user}}</div>
    <div>{{duty.date}}</div>
  </div>
</template>

<style scoped>

</style>