<script setup lang="ts">
import { UserData } from "~/store/user";

const userStore = UserData()
// userStore.set_telegram_data(initData)

const tg = window.Telegram.WebApp

const init = () => {
  tg.ready()
  tg.expand()
  tg.enableClosingConfirmation()
  tg.MainButton.hide()
  tg.BackButton.hide()
}
// const user = tg.initDataUnsafe.user
// const initData =  tg.initData
const user = { "id": 972834722, "first_name": "Дмитрий", "last_name": "Счислёнок", "username": "tyrannozavr", "language_code": "ru", "allows_write_to_pm": true, "photo_url": "https://t.me/i/userpic/320/xJjYkAlqp7Mvl8tGiKvIH2Qvh2SEY2ZYE2gKivsD9qU.svg" }

const { id: telegram_id, first_name, last_name, username, language_code } = user;

userStore.set_telegram_data(telegram_id, first_name, last_name, username, language_code);
// userStore.set_telegram_data(**user)
</script>

<template>
<!--<div>-->
<!--  <div class="mb-4">platform {{tg.platform}}</div>-->
<!--  <div class="mb-4">scheme {{tg.colorScheme}}</div>-->
<!--  <div class="mb-4">theme  {{tg.themeParams}}</div>-->
<!--  <div class="mb-4">header color {{tg.headerColor}}</div>-->
<!--  <div class="mb-4">background color {{tg.backgroundColor}}</div>-->
<!--  <div class="mb-4">is expanded {{tg.isExpanded}}</div>-->
<!--</div>-->
</template>

<style scoped>

</style>
<!--scheme dark-->
<!--theme { "accent_text_color": "#6ab2f2", "bg_color": "#17212b", "bottom_bar_bg_color": "#17212b", "button_color": "#5288c1", "button_text_color": "#ffffff", "destructive_text_color": "#ec3942", "header_bg_color": "#17212b", "hint_color": "#708499", "link_color": "#6ab3f3", "secondary_bg_color": "#232e3c", "section_bg_color": "#17212b", "section_header_text_color": "#6ab3f3", "section_separator_color": "#111921", "subtitle_text_color": "#708499", "text_color": "#f5f5f5" }-->
<!--header color #17212b-->
<!--background color #17212b-->
<!--is expanded true-->