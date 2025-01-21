<script setup lang="ts">
const isLoading = ref(true);
const user = ref(null);

onMounted(() => {
  setTimeout(() => {
    user.value = {
      first_name: "Дмитрий",
      photo_url: "https://t.me/i/userpic/320/xJjYkAlqp7Mvl8tGiKvIH2Qvh2SEY2ZYE2gKivsD9qU.svg"
    };
    isLoading.value = false; // Set loading to false after user data is initialized
  }, 100); // Simulate a loading delay
});
</script>

<template>
  <LoadingSpinner :is-loading="isLoading" />
  <div v-if="!isLoading" class="card-container">
      <div class="user-card flex flex-row" v-if="user"> <!-- Added v-if here -->
        <img :src="user.photo_url" alt="User Profile Image" class="profile-image" />
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
  height: 100vh; /* Full height of the viewport */
  padding: 16px; /* Add some padding for mobile responsiveness */

}

.user-card {
  background-color: black; /* Card background color */
  border-radius: 12px; /* Rounded corners */
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); /* Subtle shadow */
  text-align: center; /* Center text inside the card */
  padding: 20px; /* Padding inside the card */
  max-width: 400px; /* Max width for larger screens */
  width: 100%; /* Full width for smaller screens */
}

.profile-image {
  width: 80px; /* Set a fixed width for the profile image */
  height: 80px; /* Set a fixed height for the profile image */
  border-radius: 50%; /* Make the image circular */
  object-fit: cover; /* Cover the area without distortion */
  margin-bottom: 10px; /* Space between image and text */
}

.greeting {
  font-size: 1.5rem; /* Adjust font size */
  font-weight: bold; /* Make the text bold */
}

</style>
