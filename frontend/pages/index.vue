<template>
  <UContainer class="mx-auto p-4">
    <UCard class="shadow-md rounded-lg">
      <UCard>
        <template #header>
          <!--            <img src="/logo.png" alt="Logo" class="w-32 h-32 mx-auto mb-4">-->
          <h1 class="text-2xl font-bold mb-4">Добро пожаловать в Duty Reservation!</h1>

        </template>
        <p class="mb-6">
          Duty Reservation - это веб-приложение, которое позволяет создавать дежурства и управлять ими,
          делиться доступом с людьми, которые могут бронировать заданные вами даты
        </p>
      </UCard>

      <h2 class="text-xl font-semibold mb-2 mt-2">Как использовать Duty Reservation?</h2>
      <p class="mb-4">
        Для начала работы с Duty Reservation, вам необходимо создать аккаунт или войти в существующий.
      </p>
      <p class="mb-4">
        После этого вы можете
        <NuxtLink to="/created" class="text-blue-500 hover:text-blue-700 font-medium">
          Создать
        </NuxtLink>
        свое дежурство или
        <NuxtLink to="/store" class="text-blue-500 hover:text-blue-700 font-medium">
          присоединиться
        </NuxtLink>
        к существующему
      </p>
      Кстати, если вы откроете этот сайт через приложение
      <NuxtLink to="https://t.me/DutyReservationBot/reservationpage"
                class="font-medium text-blue-500 hover:text-blue-700">
        Telegram
      </NuxtLink>
      по этой ссылке

      , то сможете пользоваться приложением без дополнительной авторизации.
    </UCard>
  </UContainer>
</template>
<script setup lang="ts">
</script>