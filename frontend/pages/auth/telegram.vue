<script setup lang="ts">
import {UserData} from "~/store/user";
// import {useWebApp, useWebAppPopup} from "vue-tg";

const isLoading = ref(true);
const user = ref();
const showCard = ref(false);
const initData = ref("")
const $backend = Fetch()
const userStore = UserData()
const toast = useToast()



onMounted(() => {
  console.log("It is already mounted")
      initData.value = "user=%7B%22id%22%3A972834722%2C%22first_name%22%3A%22%D0%94%D0%BC%D0%B8%D1%82%D1%80%D0%B8%D0%B9%22%2C%22last_name%22%3A%22%D0%A1%D1%87%D0%B8%D1%81%D0%BB%D1%91%D0%BD%D0%BE%D0%BA%22%2C%22username%22%3A%22tyrannozavr%22%2C%22language_code%22%3A%22ru%22%2C%22allows_write_to_pm%22%3Atrue%2C%22photo_url%22%3A%22https%3A%5C%2F%5C%2Ft.me%5C%2Fi%5C%2Fuserpic%5C%2F320%5C%2FxJjYkAlqp7Mvl8tGiKvIH2Qvh2SEY2ZYE2gKivsD9qU.svg%22%7D&chat_instance=4863364313128253424&chat_type=private&auth_date=1736444468&signature=hj8WwV5k6T6yTvc-0u51FVE4OqUEg0CNZPTlxtdnsBLekC1zOoEqCtAfdRa7o_-rOR3r1vDkjGWtPheG19hvCQ&hash=fbbbdb68a6193d1e9dc3a484839c6bbf696e5c2746c6e6c03052659f344a60b1"
      user.value = {
        "id": 972834722,
        "first_name": "Дмитрий",
        "last_name": "Счислёнок",
        "username": "tyrannozavr",
        "language_code": "ru",
        "allows_write_to_pm": true,
        "photo_url": "https://t.me/i/userpic/320/xJjYkAlqp7Mvl8tGiKvIH2Qvh2SEY2ZYE2gKivsD9qU.svg"
      }
      isLoading.value = false;
       // Установить загрузку в false после инициализации данных пользователя

      setTimeout(() => {
        showCard.value = true; // Показываем карточку после задержки
      }, 100);

      authenticateUser(initData.value)
      console.log("Вы вошли в систему", userStore.getAccessToken)
      // showPopup("You are authenticated")
    }
)
// const { showPopup } = useWebAppPopup();
// const popup = () => showPopup({
//   title: 'Popup title',
//   message: 'Popup message',
//   buttons: [
//     { id: 'cancel', type: 'cancel', text: 'Cancel' },
//     { id: 'ok', type: 'ok', text: 'Ok' },
//     { id: 'close', type: 'close', text: 'Close' },
//   ],
// });


// useFetch('/auth/telegram', {
//   method: 'POST',
//   body: {
//     init_data: initData.value
//   }
// }
const authenticateUser = async (init_data: string) => {
  // const { data: Tokens } = $backend.post('/auth/telegram', { body: `"${init_data}"` })
  const response = await $fetch(
      `${useRuntimeConfig().public.baseURL}/auth/telegram`,
      {
        method: 'POST',
        body: JSON.stringify(init_data)
      })
  // console.log("Got data", Tokens, Tokens.value)
  // console.log("Hello", Tokens.value.access_token, Tokens.value.refresh_token )
  userStore.authenticateUser(response.access_token, response.refresh_token)
}

// onMounted(() => {
//   setTimeout(() => {
//     user.value = {
//       first_name: "Дмитрий",
//       photo_url: "https://t.me/i/userpic/320/xJjYkAlqp7Mvl8tGiKvIH2Qvh2SEY2ZYE2gKivsD9qU.svg"
//     };
//     isLoading.value = false; // Установить загрузку в false после инициализации данных пользователя
//
//     setTimeout(() => {
//       showCard.value = true; // Показываем карточку после задержки
//     }, 100); // Задержка перед показом карточки
//   }, 1000); // Симуляция задержки загрузки
// });
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
