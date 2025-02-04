<script setup lang="ts">
import {saveAs} from "file-saver";

const props = defineProps<{
  content: string,
  filename: string
}>();

const filename = computed(() => {
  return props.filename + ".txt";
});

const downloadTxt = () => {
  const blob = new Blob([props.content], {type: "text/plain;charset=utf-8"});
  saveAs(blob, filename.value);
};
</script>

<template>
  <UButton @click="downloadTxt" :disabled="!content" icon="i-heroicons-document-text">
    <slot>Скачать TXT</slot>
  </UButton>
</template>

<style scoped>

</style>