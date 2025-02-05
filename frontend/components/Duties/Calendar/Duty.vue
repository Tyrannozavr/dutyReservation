<script setup lang="ts">
import type {dutyUserDataType} from "~/types/duty";
import {useUserStore} from "~/store/user";

const props = defineProps<{
  duty: dutyUserDataType
}>()
defineEmits(['reserveDuty', 'releaseDuty'])
const userStore = useUserStore()
const DutyTakenByUser = computed(() => props.duty.user && props.duty.user.id === userStore.user_id)
</script>

<template>
  <div class="flex flex-row gap-5">
    <div>{{ duty.name ? duty.name : "Без имени" }}</div>
    <div class="ml-auto" v-if="!DutyTakenByUser">
      <UButton
          @click="$emit('reserveDuty', duty.id)"
          icon="heroicons-outline:arrow-up-on-square"
          color="green"
      >Бронировать</UButton>
    </div>
    <div class="ml-auto" v-else>
      <UButton
          @click="$emit('releaseDuty', duty.id)"
          icon="heroicons-outline:archive-box-x-mark"
          color="red"
      >Отменить дежурство</UButton>
    </div>
  </div>
</template>

<style scoped>

</style>