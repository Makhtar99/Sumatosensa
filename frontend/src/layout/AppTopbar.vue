<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'
import { useMediaQuery } from '@vueuse/core'

import DarkModeButton from '../views/Components/DarkModeButton.vue'
import Notif from '../assets/svg/ph_bell.svg'

const date = ref('')
const isTelephone = useMediaQuery('(max-width: 768px)')
const router = useRouter()

const auth = useAuthStore()
const { isAuthenticated, isAdmin } = storeToRefs(auth)

const toNotif = () => router.push('/notifications')

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
</script>


<template>
  <header class="p-6 flex items-center justify-between max-w-screen">
    <button
      v-if="!isTelephone"
      @click="goback"
      class="flex items-center gap-1 text-gray-500 hover:text-gray-700">
      <img src="../assets/svg/arrow-left.svg" alt="Back" class="w-4 h-4 SumatoIcon" />
      <span>Retour</span>
    </button>

    <div class="text-sm">{{ date }}</div>

    <div v-if="!isTelephone" class="flex items-center gap-4">
      <template v-if="isAuthenticated">
        <div class="flex items-center gap-2">
          <DarkModeButton />
          <!-- <RouterLink to="/settings">
            <img :src="Avatar" alt="Avatar" class="w-5 h-5" />
          </RouterLink> -->
          <RouterLink v-if="isAdmin" to="/admin" class="bg-[var(--color-primary)] px-2 py-1 rounded-xl">
            Admin
          </RouterLink>
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
          <button @click="toNotif" class="relative">
            <img :src="Notif" alt="Notifications" class="w-6 h-6 SumatoIcon" />
            <div class="absolute -top-1 -right-1 w-4 h-4 bg-red-600 text-white text-xs font-bold rounded-full flex items-center justify-center">
              6
            </div>
          </button>
          <DarkModeButton/>
        </div>

      </template>
    </div>
  </header>
</template>
