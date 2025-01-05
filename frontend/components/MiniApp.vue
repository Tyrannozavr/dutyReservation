<script lang="ts" setup>
import { MainButton, useWebAppPopup } from 'vue-tg'
const { showAlert } = useWebAppPopup()
let tg = window.Telegram.WebApp

</script>

<template>
  telegram webapp {{tg.initDataUnsafe}}
  <MainButton text="Open alert" @click="() => showAlert('Hello!')" />
</template>