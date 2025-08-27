<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { isAuthenticated, logout } from '@/services/AuthService'
// import { apiService } from '@/services/api';

// import { getFormattedDateTime } from '../assets/functions/FormatedDate';
import DarkModeButton from '../views/Components/DarkModeButton.vue'
const date = ref('')
const showDropdown = ref(false)
const isAdmin = ref(false)
const isMobile = ref(window.innerWidth < 768)
const router = useRouter()

// onMounted(async () => {
//   date.value = getFormattedDateTime();
//   setInterval(() => {
//     date.value = getFormattedDateTime();
//   }, 1000);
//   isAdmin.value = await apiServicscriptmin();
// });

const goback = () => {
  router.go(-1)
}

window.addEventListener('resize', () => {
  isMobile.value = window.innerWidth < 768
})
</script>

<template>
  <header class="p-4 flex items-center justify-between max-w-screen">
    <button
      v-if="!isMobile"
      @click="goback"
      class="flex items-center gap-1 text-gray-500 hover:text-gray-700"
    >
      <img src="../assets/svg/arrow-left.svg" alt="Back" class="w-4 h-4" />
      <span>Retour</span>
    </button>
    <div class="text-sm text-gray-600">{{ date }}</div>

    <div v-if="!isMobile" class="flex items-center gap-4">
      <template v-if="isAuthenticated()">
        <div class="flex items-center gap-2">
          <DarkModeButton />
          <RouterLink to="/settings">
            <img
              src="../assets/img/avatar.png"
              alt="Avatar"
              class="rounded-full w-[40px] h-[40px]"
            />
          </RouterLink>
          <RouterLink v-if="isAdmin" to="/admin" class="bg-blue-500 px-2 py-1 rounded-xl">
            Admin
          </RouterLink>
          <button @click="logout()" class="bg-red-500 px-2 py-1">Déconnexion</button>
        </div>
      </template>

      <template v-else>
        <RouterLink to="/login" class="bg-green-500 rounded px-2 py-1"
          >Connexion</RouterLink
        >
        <RouterLink to="/register" class="bg-yellow-500 rounded px-2 py-1"
          >Inscription</RouterLink
        >
      </template>
    </div>

    <div v-else class="relative">
      <template v-if="isAuthenticated()">
        <button @click="showDropdown = !showDropdown">
          <img src="../assets/img/avatar.png" alt="Avatar" class="rounded-full w-[40px] h-[40px]" />
        </button>

        <transition>
          <div
            v-if="showDropdown"
            class="absolute right-0 mt-2 w-48 bg-sumato-background border rounded shadow-md z-50"
          >
            <div class="px-4 py-2 text-sm text-gray-700">Connecté</div>
            <button
              @click="logout"
              class="w-full text-left px-4 py-2 hover:bg-red-100 text-red-500"
            >
              Déconnexion
            </button>
            <RouterLink v-if="isAdmin" to="/admin" class="block px-4 py-2 hover:bg-gray-100"
              >Admin</RouterLink
            >
            <div class="px-4 py-2">📧 Messages</div>
            <div class="px-4 py-2">🔔 Notifications</div>
          </div>
        </transition>
      </template>

      <template v-else>
        <RouterLink to="/login" class="bg-green-500 rounded px-2 py-1 mr-2"
          >Connexion</RouterLink
        >
        <RouterLink to="/register" class="bg-yellow-500 rounded px-2 py-1"
          >Inscription</RouterLink
        >
      </template>
    </div>
  </header>
</template>
