<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'
import { useMediaQuery } from '@vueuse/core'

import DarkModeButton from '../views/Components/DarkModeButton.vue'

const date = ref('')
const showDropdown = ref(false)
const isTelephone = useMediaQuery('(max-width: 768px)')
const router = useRouter()

const auth = useAuthStore()
const { isAuthenticated, isAdmin } = storeToRefs(auth)

function getFormattedDateTime() {
  const now = new Date();
  const date = now.toLocaleDateString('fr-FR', {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
  });
  const time = now.toLocaleTimeString('fr-FR', {
    hour: '2-digit', minute: '2-digit', hour12: false
  });
  return `${date.replace(/^\w/, c => c.toUpperCase())} - ${time}`;
}


onMounted(async () => {
  await auth.initializeAuth().catch(() => {})

  date.value = getFormattedDateTime()
  setInterval(() => {
    date.value = getFormattedDateTime()
  }, 1000)
})

const goback = () => router.go(-1)
const onLogout = async () => {
  await auth.logout()
  showDropdown.value = false
  window.location.reload()
}
</script>


<template>
  <header class="p-6 flex items-center justify-between max-w-screen">
    <button
      v-if="!isTelephone"
      @click="goback"
      class="flex items-center gap-1 text-gray-500 hover:text-gray-700">
      <img src="../assets/svg/arrow-left.svg" alt="Back" class="w-4 h-4 sidebarIcon" />
      <span>Retour</span>
    </button>

    <div class="text-sm text-[var(--color-sumato-text)]">{{ date }}</div>

    <div v-if="!isTelephone" class="flex items-center gap-4">
      <template v-if="isAuthenticated">
        <div class="flex items-center gap-2">
          <DarkModeButton />
          <RouterLink to="/settings">
            <img src="../assets/img/avatar.png" alt="Avatar" class="rounded-full w-[40px] h-[40px]" />
          </RouterLink>
          <RouterLink v-if="isAdmin" to="/admin" class="bg-[var(--color-primary)] px-2 py-1 rounded-xl">
            Admin
          </RouterLink>
          <button @click="onLogout" class="bg-[var(--color-sumato-danger)] px-2 py-1">
            Déconnexion
          </button>
        </div>
      </template>

      <template v-else>
        <RouterLink to="/login" class="rounded px-2 py-1 button">Connexion</RouterLink>
        <RouterLink to="/register" class="rounded px-2 py-1 button">Inscription</RouterLink>
        <DarkModeButton />
      </template>
    </div>

    <div v-else>
      <template v-if="isAuthenticated">
        <div class="flex items-center gap-3">
          <button @click="showDropdown = !showDropdown">
            <img src="../assets/img/avatar.png" alt="Avatar" class="rounded-full w-[40px] h-[40px]" />
          </button>
        </div>

        <transition>
          <div
            v-if="showDropdown"
            class="fixed top-0 right-0 mt-14 mr-4 w-56 bg-[var(--color-sumato-surface)] border rounded shadow-lg z-50">
          <div class="flex flex-col gap-3 p-3 m-auto">
            <DarkModeButton />
            <router-link v-if="isAdmin" to="/admin" class="bg-[var(--color-primary)] px-2 py-1 rounded-xl">
              Admin
            </router-link>
            <button @click="onLogout" class="w-full text-left px-4 py-2 hover:bg-red-100 text-[var(--color-sumato-danger)]">
              Déconnexion
            </button>
            <RouterLink v-if="isAdmin" to="/admin" class="block px-4 py-2 hover:bg-gray-100">
              Admin
            </RouterLink>
          </div>
          </div>
        </transition>
      </template>

      <template v-else>
        <button @click="showDropdown = !showDropdown">
          <img src="../assets/img/avatar.png" alt="Avatar" class="rounded-full w-[40px] h-[40px]" />
        </button>

        <transition>
          <div
            v-if="showDropdown"
            class="flex flex-col items-start justify-center gap-3 fixed top-0 right-0 mt-14 mr-4 p-3 w-30 bg-[var(--color-sumato-surface)] border rounded shadow-lg z-50">
            <RouterLink to="/login" class="rounded px-2 py-1 mr-2 button">Connexion</RouterLink>
            <RouterLink to="/register" class="rounded px-2 py-1 button">Inscription</RouterLink>
            <DarkModeButton />
          </div>
        </transition>
      </template>
    </div>
  </header>
</template>
