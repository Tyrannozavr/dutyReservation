<script setup lang="ts">
import type {dutyWithUserType, dutyWithUserTypeList} from "~/types/duty";

const props = withDefaults(defineProps<{
  duties: dutyWithUserTypeList
}>(), {
  duties: () => []
})


const groupedDuties = computed(() => {
  let result: { date: string, duties: dutyWithUserType[] }[] = [];
  if (Array.isArray(props.duties)) {
    // Your logic here
    props.duties.forEach(item => {
      // item.date = item.date.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' })
      const existingDateGroup = result.find(group => group.date === item.date);

      if (existingDateGroup) {
        existingDateGroup.duties.push(item);
      } else {
        result.push({date: item.date, duties: [item]});
      }
    });
  } else {
    console.error("props.duties is not an array:", props.duties);
  }
  return result;
});

</script>

<template>
  <DutiesCalendar :duties-data="groupedDuties" />
</template>

<style scoped>

</style>