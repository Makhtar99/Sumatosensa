<template>
     <header class="p-4 flex items-center justify-between">
      <div>
        <span>{{ date }}</span>
      </div>
    <div class="flex items-center gap-4">
      <!-- bouton avec une icone de mail -->
      <div class="flex justify-center items-center rounded-full w-[30px] h-[30px] bg-color-avatar">
        <button title="Messages" class="relative">
        📧
        <span class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full px-1">5</span>
      </button>
      </div>
      <button title="Notifications" class="relative">
        🔔
        <span class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full px-1">3</span>
      </button>
      <button title="Profil">
        <img src="../assets/img/avatar.png" alt="Avatar" class="rounded-full" style="height: 50px; width: 50px;" />
      </button>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { RouterLink } from 'vue-router';

function getFormattedDateTime() {
  const now = new Date();

  const date = now.toLocaleDateString('fr-FR', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });

  const time = now.toLocaleTimeString('fr-FR', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  });

  return `${date.replace(/^\w/, c => c.toUpperCase())} - ${time}`;
}
onMounted(() => {
  date.value = getFormattedDateTime();
  const interval = setInterval(() => {
    date.value = getFormattedDateTime();
  }, 1000);
})

const date = ref(getFormattedDateTime());

</script>

<style>
.btn {
    background-color: #fff;
    color: #000;
    padding: 10px 20px;
    border-radius: 5px;
    text-decoration: none;
    height: 50px;
    width: 150px;
    border: 2px solid black;
}
</style>