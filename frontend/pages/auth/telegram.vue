<script setup lang="ts">
import {useUserStore} from "~/store/user";
import {useAuthStore} from "~/store/auth";
import type {TokenResponse} from "~/types/auth";
import {fetchUserData} from "~/services/authorization";


const isLoading = ref(true);
const user = ref();
const showCard = ref(false);
const initData = ref("")
const userStore = useUserStore()
const authStore = useAuthStore()

const route = useRoute()
const router = useRouter()
const toast = useToast()
const nextPage = route.query.redirect


onMounted(async () => {
      const tg = window.Telegram?.WebApp
      if (tg.initData) {
        initData.value = tg.initData
        user.value = tg.initDataUnsafe?.user
        isLoading.value = false;
        
      }

      // initData.value = useRuntimeConfig().public.telegramInitData
      // user.value = {
      //   "id": 972834722,
      //   "first_name": "Дмитрий",
      //   "last_name": "Счислёнок",
      //   "username": "tyrannozavr",
      //   "language_code": "ru",
      //   "allows_write_to_pm": true,
      //   "photo_url": "https://t.me/i/userpic/320/xJjYkAlqp7Mvl8tGiKvIH2Qvh2SEY2ZYE2gKivsD9qU.svg"
      // }

      setTimeout(() => {
        showCard.value = true; // Показываем карточку после задержки
      }, 100);
      try {
        await authenticateUser(initData.value)
      } catch (e) {
        console.log("error is", e)
        toast.add({
          title: 'Ошибка',
          description: 'Сервер временно недоступен',
          color: 'red',
          timeout: 5000,
        })
      }

    }
)
const authenticateUser = async (init_data: string) => {
  const response = await $fetch<TokenResponse>(
      `${useRuntimeConfig().public.baseURL}/auth/telegram`,
      {
        method: 'POST',
        body: JSON.stringify(init_data),
        onResponse({response}) {
          if (response.status !== 200 && response.status !== 201) {
            toast.add({
              title: 'Ошибка',
              description: 'Ошибка входа через телеграм',
              color: 'red',
              timeout: 5000,
            })
            navigateTo('/auth')
          }
        }
      })

  authStore.login(
      response.access_token,
      response.refresh_token,
  )
  userStore.setOrigin("telegram")
  toast.add({
    title: 'Успешный вход',
    description: 'Вы успешно вошли через телеграм',
    color: 'green',
    timeout: 5000,
  })

  await fetchUserData()
  if (nextPage) {
    await router.push(nextPage.toString())
  } else {
    await router.push("/profile")
  }
}
</script>

<template>
  <LoadingSpinner :is-loading="isLoading"/>
  <div v-if="!isLoading && showCard" class="card-container">
    <div class="user-card flex flex-row" v-if="user">
      <img :src="user.photo_url" alt="User Profile Image" class="profile-image"/>
      <div class="greeting w-full">
        Привет,&nbsp {{ user.first_name }}
      </div>
    </div>
  </div>
  <div class="card-container">
  </div>
</template>

<style scoped>
.card-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; /* Полная высота окна просмотра */
  padding: 8px; /* Добавить немного отступа для мобильной адаптации */
  opacity: 0; /* Начальная непрозрачность для анимации */
  animation: fadeInDown 3s forwards; /* Анимация на 3 секунды */
}

.user-card {
  background-color: black; /* Цвет фона карточки */
  border-radius: 12px; /* Закругленные углы */
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); /* Легкая тень */
  text-align: center; /* Центрировать текст внутри карточки */
  padding: 20px; /* Отступ внутри карточки */
  max-width: 400px; /* Максимальная ширина для больших экранов */
  width: 100%; /* Полная ширина для маленьких экранов */
}

.profile-image {
  width: 80px; /* Фиксированная ширина для изображения профиля */
  height: 80px; /* Фиксированная высота для изображения профиля */
  border-radius: 50%; /* Сделать изображение круглым */
  object-fit: cover; /* Заполнить область без искажений */
  margin-bottom: 10px; /* Пробел между изображением и текстом */
}

.greeting {
  font-size: 1.5rem; /* Настроить размер шрифта */
  font-weight: bold; /* Сделать текст жирным */
}

/* Анимация выплывания сверху */
@keyframes fadeInDown {
  from {
    transform: translateY(-50px); /* Начальное положение выше */
    opacity: 0; /* Начальная непрозрачность */
  }

  to {
    transform: translateY(0); /* Конечное положение */
    opacity: 1; /* Конечная непрозрачность */
  }
}
</style>
