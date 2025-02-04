<script setup lang="ts">
import PizZip from "pizzip";
import Docxtemplater from "docxtemplater";
import {saveAs} from "file-saver";

const props = defineProps<{
  content: string,
  filename: string
}>();

const filename = computed(() => {
  return props.filename + ".docx";
});

const downloadDocx = async () => {
  try {
    // Load the DOCX template from the public folder
    const response = await fetch("/template.docx");
    const template = await response.arrayBuffer();

    // Initialize PizZip with the template
    const zip = new PizZip(template);

    // Initialize docxtemplater
    const doc = new Docxtemplater(zip, {
      paragraphLoop: true,
      linebreaks: true,
    });
    // Replace the placeholder in the template with the table content
    doc.render({
      table: props.content,
    });

    // Generate the DOCX file
    const blob = doc.getZip().generate({type: "blob"});

    // Save the file
    saveAs(blob, filename.value);
  } catch (error) {
    console.error("Error generating DOCX file:", error);
  }
};
</script>

<template>
  <UButton @click="downloadDocx" icon="i-heroicons-document-text">
    <slot>Скачать DOCX</slot>
  </UButton>
</template>

<style scoped>

</style>