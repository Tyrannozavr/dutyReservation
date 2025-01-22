<script setup lang="ts">
import { useUserStore } from "~/store/user";
// import {useWebAppPopup} from "vue-tg";

const userStore = useUserStore()
// userStore.set_telegram_data(initData)

// const tg = window.Telegram?.WebApp
//
// const init = () => {
//   tg.ready()
//   tg.expand()
//   tg.enableClosingConfirmation()
//   tg.MainButton.hide()
//   tg.BackButton.hide()
// }
// if (tg) {
//   const user = tg.initDataUnsafe
//   const { id: telegram_id, first_name, last_name, username, language_code } = user;
//   userStore.set_telegram_data(telegram_id, first_name, last_name, username, language_code);
//   console.log("tg is", tg)
//   console.log("user data is", user)
//
// }
// const user = tg.initDataUnsafe.user
// const initData =  tg.initData
// const initData = `user=%7B%22id%22%3A972834722%2C%22first_name%22%3A%22%D0%94%D0%BC%D0%B8%D1%82%D1%80%D0%B8%D0%B9%22%2C%22last_name%22%3A%22%D0%A1%D1%87%D0%B8%D1%81%D0%BB%D1%91%D0%BD%D0%BE%D0%BA%22%2C%22username%22%3A%22tyrannozavr%22%2C%22language_code%22%3A%22ru%22%2C%22allows_write_to_pm%22%3Atrue%2C%22photo_url%22%3A%22https%3A%5C%2F%5C%2Ft.me%5C%2Fi%5C%2Fuserpic%5C%2F320%5C%2FxJjYkAlqp7Mvl8tGiKvIH2Qvh2SEY2ZYE2gKivsD9qU.svg%22%7D&chat_instance=5919894213088809580&chat_type=private&auth_date=1736280453&signature=ru-H3ccFkx-Z1bBwBQ98MW38-3C02T2cAUbf0yP94VbJEKp0kcWI2VWVs_4U4vJm2_Zilxj6BDIFTH54uI8jBA&hash=93063c75042cb6076876c9d7b4540e409c6e71338454e9dcb93dfeb1`
// const user = { "id": 972834722, "first_name": "Дмитрий", "last_name": "Счислёнок", "username": "tyrannozavr", "language_code": "ru", "allows_write_to_pm": true, "photo_url": "https://t.me/i/userpic/320/xJjYkAlqp7Mvl8tGiKvIH2Qvh2SEY2ZYE2gKivsD9qU.svg" }
// const { showAlert } = useWebAppPopup()

</script>

<template>
<!--  tg {{tg}}-->
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