<script setup>
import { ref, onMounted } from 'vue';
import { RouterLink } from 'vue-router';
import { isAuthenticated, logout } from '@/services/AuthService';
import { apiService } from '@/services/api';

import { getFormattedDateTime } from '../assets/functions/FormatedDate';

const date = ref('');
const showDropdown = ref(false);
const isAdmin = ref(false);
const isMobile = ref(window.innerWidth < 768);

onMounted(async () => {
  date.value = getFormattedDateTime();
  setInterval(() => {
    date.value = getFormattedDateTime();
  }, 1000);
  isAdmin.value = await apiService.isAdmin();
});

window.addEventListener('resize', () => {
  isMobile.value = window.innerWidth < 768;
});
</script>

<template>
  <header class="p-4 flex items-center justify-between bg-white shadow-md max-w-screen">
    <div class="text-sm text-gray-600">{{ date }}</div>

    <div v-if="!isMobile" class="flex items-center gap-4">
      <template v-if="isAuthenticated()">
        <div class="flex items-center gap-2">
          <button @click="logout()" class="bg-red-500 text-white px-2 py-1">Déconnexion</button>
          <RouterLink v-if="isAdmin" to="/admin" class="bg-blue-500 text-white px-2 py-1 rounded-xl">Admin</RouterLink>
          <RouterLink to="/settings">
            <img src="../assets/img/avatar.png" alt="Avatar" class="rounded-full w-[40px] h-[40px]" />
          </RouterLink>
        </div>
      </template>

      <template v-else>
        <RouterLink to="/login" class="bg-green-500 text-white rounded px-2 py-1">Connexion</RouterLink>
        <RouterLink to="/register" class="bg-yellow-500 text-white rounded px-2 py-1">Inscription</RouterLink>
      </template>
    </div>

    <div v-else class="relative">
      <template v-if="isAuthenticated()">
        <button @click="showDropdown = !showDropdown">
          <img src="../assets/img/avatar.png" alt="Avatar" class="rounded-full w-[40px] h-[40px]" />
        </button>

        <transition name="fade">
          <div v-if="showDropdown" class="absolute right-0 mt-2 w-48 bg-white border rounded shadow-md z-50">
            <div class="px-4 py-2 text-sm text-gray-700">Connecté</div>
            <button @click="logout" class="w-full text-left px-4 py-2 hover:bg-red-100 text-red-500">Déconnexion</button>
            <RouterLink v-if="isAdmin" to="/admin" class="block px-4 py-2 hover:bg-gray-100">Admin</RouterLink>
            <div class="px-4 py-2">📧 Messages</div>
            <div class="px-4 py-2">🔔 Notifications</div>
          </div>
        </transition>
      </template>

      <template v-else>
        <RouterLink to="/login" class="bg-green-500 text-white rounded px-2 py-1 mr-2">Connexion</RouterLink>
        <RouterLink to="/register" class="bg-yellow-500 text-white rounded px-2 py-1">Inscription</RouterLink>
      </template>
    </div>
  </header>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s ease-in-out;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
