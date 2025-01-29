<script setup lang="ts">
import {useUserStore} from "~/store/user";

const userStore = useUserStore()
</script>
<template>
  <UContainer>
    <UCard>
      <template #header>
        <h1 class="text-2xl font-bold flex">Профиль
        <UAvatar :src="userStore.photo_url" alt="avatar" size="md" class="ml-auto" v-if="userStore.photo_url" />
          <ProfileLogout class="ml-6"/>
        </h1>
      </template>
    <UCard>
      <p class="text-lg mb-4">Добро пожаловать,&nbsp;&nbsp;{{userStore.first_name}} {{userStore.last_name}}</p>
      <p class="text-lg mb-4">Юзернейм:&nbsp;&nbsp;{{userStore.username}}</p>
    </UCard>
    </UCard>
  </UContainer>
</template>

<style scoped>

</style>