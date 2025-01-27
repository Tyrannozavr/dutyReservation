<script setup lang="ts">
import { ref, defineProps } from 'vue';

const props = defineProps<{
  dutyList: { name: string; duty_date: string }[];
}>();
const emits = defineEmits(["onUpdateDutyList"])
const showDetailSettings = ref(false);

const toggleDetailSettings = () => {
  showDetailSettings.value = !showDetailSettings.value;
};

const doubleAllDuties = () => {
  const doubledDuties = props.dutyList.map(duty => ({ ...duty }));
  emits('onUpdateDutyList', ([...props.dutyList, ...doubledDuties]));
};

const doubleSingleDuty = (index: number) => {
  const dutyToDouble = props.dutyList[index];
  emits('onUpdateDutyList', ([...props.dutyList, { ...dutyToDouble }]))
};
</script>

<template>
  <div>
    <UButton @click="toggleDetailSettings">
      {{ showDetailSettings ? 'Скрыть детальные настройки' : 'Показать детальные настройки' }}
    </UButton>

      <UCard class="mt-5" v-if="showDetailSettings">
        <div class="header flex flex-row pb-4">
          <UButton class="rounded-full ml-auto" @click="doubleAllDuties">
            <UIcon name="heroicons-outline:plus" />
          </UButton>
        </div>
          <ul class="space-y-2">
            <li v-for="(duty, index) in dutyList" :key="index" class="flex flex-row justify-between" >
              <UInput
                  type="text"
                  v-model="duty.name"
                  placeholder="Set Name"
              />
              <span>{{ duty.duty_date }}</span>
              <UButton @click="doubleSingleDuty(index)" class="rounded-full ">
                <UIcon name="heroicons-outline:plus" />
              </UButton>

            </li>
          </ul>
      </UCard>
  </div>
</template>
