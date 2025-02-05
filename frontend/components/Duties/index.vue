<script setup lang="ts">
import type {dutyWithUserType, dutyWithUserTypeList, groupedDutiesType} from "~/types/duty";

const props = withDefaults(defineProps<{
  duties: dutyWithUserTypeList
}>(), {
  duties: () => []
})
defineEmits(['reserveDuty', 'releaseDuty'])


const groupedDuties: groupedDutiesType[] = computed(() => {
  let result: { date: string, duties: dutyWithUserType[] }[] = [];
  if (Array.isArray(props.duties)) {
    // Your logic here
    props.duties.forEach(item => {
      item.date = new Date(item.date);
      const existingDateGroup = result.find(group =>
          group.date.toLocaleDateString() === item.date.toLocaleDateString()
      );

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
  <DutiesCalendar
      :duties-data="groupedDuties"
      @reserveDuty="(id) => $emit('reserveDuty', id)"
      @releaseDuty="(id) => $emit('releaseDuty', id)"
  />
  <DutiesTable :duties="props.duties" />
</template>

<style scoped>

</style>