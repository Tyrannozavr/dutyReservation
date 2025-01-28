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
            <li v-for="(duty, index) in dutyListToShow" :key="index" class="flex flex-row justify-between" >
              <UInput
                  type="text"
                  v-model="duty.name"
                  placeholder="задать название"
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
