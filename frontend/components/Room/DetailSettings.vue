<script setup lang="ts">
import { ref, defineProps } from 'vue';

const props = defineProps<{
  dutyList: { name: string; duty_date: string }[];
}>();

const dutyListToShow = computed(() => props.dutyList.sort(
    (a, b) => new Date(a.duty_date).getDate() - new Date(b.duty_date).getDate()
    )
)
const emits = defineEmits(["onUpdateDutyList"])
const showDetailSettings = ref(false);

const toggleDetailSettings = () => {
  showDetailSettings.value = !showDetailSettings.value;
};

const doubleAllDuties = () => {
  const doubledDuties = dutyListToShow.value.map(duty => ({ ...duty }));
  emits('onUpdateDutyList', ([...props.dutyList, ...doubledDuties]));
};

const doubleSingleDuty = (index: number) => {
  const dutyToDouble = dutyListToShow.value[index];
  emits('onUpdateDutyList', ([...props.dutyList, { ...dutyToDouble }]))
};

const removeSingleDuty = (index: number) => {
  const updatedDutyList = [...props.dutyList];
  updatedDutyList.splice(index, 1);
  emits('onUpdateDutyList', updatedDutyList);
};
</script>

<template>
  <div>
    <UButton @click="toggleDetailSettings">
      {{ showDetailSettings ? 'Скрыть детальные настройки' : 'Показать детальные настройки' }}
    </UButton>
      <UCard class="mt-5" v-if="showDetailSettings">
        <div class="header flex flex-row pb-4">
          <UButton label="дублировать все" class="" @click="doubleAllDuties">
             дублировать все
          </UButton>
        </div>
          <ul class="space-y-4">
            <li v-for="(duty, index) in dutyListToShow" :key="index"
                class="flex flex-row justify-between"
            >
              <UInput
                  type="text"
                  class="h-4 w-2/4"
                  v-model="duty.name"
                  placeholder="задать название"
              />
              <span>{{ duty.duty_date }}</span>
              <UButton @click="doubleSingleDuty(index)" class="rounded-full ">
                <UIcon name="heroicons-outline:plus" />
              </UButton>
              <UIcon
                  name="heroicons-outline:trash"
                  class="text-red-500 cursor-pointer w-7 h-7"
                  @click="removeSingleDuty(index)"
              />
            </li>
          </ul>
      </UCard>
  </div>
</template>
