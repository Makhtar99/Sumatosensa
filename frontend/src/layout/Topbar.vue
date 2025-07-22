<script setup>
import { ref, onMounted } from 'vue';
import { RouterLink } from 'vue-router';
import { isAuthenticated, logout } from '@/services/AuthService'
import { apiService } from '@/services/api';


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
const isAdmin = ref(false);
onMounted(async () => {
  isAdmin.value = await apiService.isAdmin();
  // console.log("État de l'admin :", isAdmin.value);
});

</script>

<template>
     <header class="p-4 flex items-center justify-between">
      <div>
        <span>{{ date }}</span>
      </div>
    <div class="flex justify-center items-center gap-4">
      <div class="flex justify-center items-center rounded-full w-[30px] h-[30px] bg-[#F9E0BD]">
        <button title="Messages" class="relative">
        📧
        <!-- <span class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full px-1">5</span> -->
      </button>
      </div>
      <div class="flex justify-center items-center rounded-full w-[30px] h-[30px] bg-[#F9E0BD]">
        <button title="Notifications" class="relative">
          🔔
          <!-- <span class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full px-1">3</span> -->
        </button>
      </div>  
      <button title="Profil">
        <RouterLink to="/settings">
          <img src="../assets/img/avatar.png" alt="Avatar" class="rounded-full" style="height: 50px; width: 50px;" />
        </RouterLink>
      </button>
      <span v-if="isAuthenticated()">Connecté</span>
      <button v-if="isAuthenticated()" @click="logout()" class="bg-red-500 text-white rounded px-2 py-1 cursor-pointer">Déconnexion</button>
      <RouterLink v-if="isAuthenticated() && isAdmin" to="/admin" class="bg-blue-500 text-white rounded px-2 py-1 cursor-pointer">Admin</RouterLink>
      <RouterLink v-if="!isAuthenticated()" to="/login" class="bg-green-500 text-white rounded px-2 py-1 cursor-pointer">Connexion</RouterLink>
      <RouterLink v-if="!isAuthenticated()" to="/register" class="bg-yellow-500 text-white rounded px-2 py-1 cursor-pointer">Inscription</RouterLink>
    </div>
  </header>
</template>
