<script setup>
import { ref, onMounted } from 'vue';

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

<template>
     <header class="p-4 flex items-center justify-between">
      <div>
        <span>{{ date }}</span>
      </div>
    <div class="flex items-center gap-4">
      <div class="flex justify-center items-center rounded-full w-[30px] h-[30px] bg-[#F9E0BD]">
        <button title="Messages" class="relative">
        📧
        <span class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full px-1">5</span>
      </button>
      </div>
      <div class="flex justify-center items-center rounded-full w-[30px] h-[30px] bg-[#F9E0BD]">
        <button title="Notifications" class="relative">
          🔔
          <span class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full px-1">3</span>
        </button>
      </div>  
      <button title="Profil">
        <img src="../assets/img/avatar.png" alt="Avatar" class="rounded-full" style="height: 50px; width: 50px;" />
      </button>
    </div>
  </header>
</template>
