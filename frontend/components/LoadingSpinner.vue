<template>
  <div class="loading-spinner" v-if="isLoading">
    <img src="@/assets/img/loading3.png" alt="Loading..." class="spinner" />
<!--    <img src="@/assets/img/loading2.gif" alt="Loading..." class="spinner" />-->
  </div>
</template>

<script setup>
const props = defineProps({
  isLoading: {
    type: Boolean,
    required: true,
  },
});
</script>

<style scoped>
.loading-spinner {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(255, 255, 255, 1); /* Optional background */
}

.spinner {
  width: 100px; /* Adjust size as needed */
  animation: spin 3s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
