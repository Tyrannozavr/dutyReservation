<script setup lang="ts">
import type {dutyWithUserType} from "~/types/duty";

defineProps<{
  duty: dutyWithUserType
}>()
</script>

<template>
 {{duty }}
</template>

<style scoped>

</style>