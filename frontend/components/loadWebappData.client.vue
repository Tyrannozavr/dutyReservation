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
<div>

</div>
</template>

<style scoped>

</style>