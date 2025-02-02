<script setup lang="ts">
import type {dutyWithUserType, groupedDutiesType} from "~/types/duty";

const props = defineProps<{
  duty: groupedDutiesType
}>()
</script>

<template>
 <UButton>
   {{duty.date}}
   - {{duty.duties.length}}
 </UButton>
</template>

<style scoped>

</style>
