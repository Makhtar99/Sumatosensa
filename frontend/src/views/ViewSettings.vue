<script setup lang="ts">
import { reactive, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useMediaQuery } from '@vueuse/core'
import DarkModeButton from './Components/DarkModeButton.vue'

import { useUserPrefStore } from '@/stores/userpref'

const auth = useAuthStore()
const userPref = useUserPrefStore()

const user = reactive({ username: '', email: '' })
const isTelephone = useMediaQuery('(max-width: 768px)')

onMounted(async () => {
  if (!auth.user) {
    try {
      await auth.getCurrentUser()
    } catch {}
  }
  user.username = auth.user?.username ?? ''
  user.email = auth.user?.email ?? ''
})

const isDirty = computed(
  () => user.username !== (auth.user?.username ?? '') || user.email !== (auth.user?.email ?? ''),
)
</script>

<template>
  <div class="p-6">
    <h1 class="title !mt-0 mb-6" :class="[isTelephone ? 'flex justify-center' : '']">
      Paramètres
    </h1>

    <div class="grid grid-cols-1 gap-6 mt-6">
      <div class="md:col-span-2 space-y-6">
        <!-- 👤 Profil utilisateur -->
        <section class="bg-[var(--color-sumato-surface)] p-6 rounded-xl shadow border border-[var(--color-sumato-border)]">
          <h3 class="text-lg font-semibold mb-4 text-[var(--color-sumato-text)]">👤 Profil utilisateur</h3>
          <div class="flex flex-col sm:flex-row gap-4 mt-4">
            <input v-model="user.username" type="text" class="w-full p-2 rounded-xl border" placeholder="Nom d’utilisateur" />
            <input v-model="user.email" type="email" class="w-full p-2 rounded-xl border" placeholder="Email" />
          </div>
          <button :disabled="!isDirty || auth.isLoading" class="mt-4 w-full px-4 py-2 bg-[var(--color-sumato-accent)] text-white rounded-lg disabled:opacity-50">
            {{ auth.isLoading ? 'Enregistrement…' : 'Enregistrer les modifications' }}
          </button>
        </section>

        <!-- 🌐 Préférences générales -->
        <section class="bg-[var(--color-sumato-surface)] p-6 rounded-xl shadow border border-[var(--color-sumato-border)]">
          <h3 class="text-lg font-semibold mb-4 text-[var(--color-sumato-text)]">🌐 Préférences générales</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block font-medium mb-1">Thème :</label>
              <dark-mode-button class="w-full" />
            </div>
            <div>
              <label class="block font-medium mb-1">Langue :</label>
              <select v-model="userPref.lang" class="w-full px-3 py-2 rounded-lg border">
                <option value="fr">Français</option>
                <option value="en">Anglais</option>
              </select>
            </div>
          </div>
        </section>

        <!-- 📟 Nom des capteurs -->
        <section class="bg-[var(--color-sumato-surface)] p-6 rounded-xl shadow border border-[var(--color-sumato-border)]">
          <h3 class="text-lg font-semibold mb-4 text-[var(--color-sumato-text)]">📟 Nom des capteurs</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div><label class="block font-medium mb-1">Capteur 1 :</label><input v-model="userPref.sensor1name" type="text" class="w-full p-2 rounded-xl border" /></div>
            <div><label class="block font-medium mb-1">Capteur 2 :</label><input v-model="userPref.sensor2name" type="text" class="w-full p-2 rounded-xl border" /></div>
            <div><label class="block font-medium mb-1">Capteur 3 :</label><input v-model="userPref.sensor3name" type="text" class="w-full p-2 rounded-xl border" /></div>
          </div>
        </section>

        <!-- 📊 Affichage & données -->
        <section class="bg-[var(--color-sumato-surface)] p-6 rounded-xl shadow border border-[var(--color-sumato-border)]">
          <h3 class="text-lg font-semibold mb-4 text-[var(--color-sumato-text)]">📊 Affichage & données</h3>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label class="block font-medium mb-1">Unité de température :</label>
              <select v-model="userPref.tempUnit" class="w-full px-3 py-2 rounded-lg border">
                <option value="Celsius">Celsius</option>
                <option value="Fahrenheit">Fahrenheit</option>
              </select>
            </div>
            <div>
              <label class="block font-medium mb-1">Unité de pression :</label>
              <select v-model="userPref.pressureUnit" class="w-full px-3 py-2 rounded-lg border">
                <option value="hPa">hPa</option>
                <option value="bar">bar</option>
              </select>
            </div>
            <div>
              <label class="block font-medium mb-1">Unité d’humidité :</label>
              <select v-model="userPref.humidityUnit" class="w-full px-3 py-2 rounded-lg border">
                <option value="%">%</option>
                <option value="g/m³">g/m³</option>
              </select>
            </div>
          </div>
        </section>

        <!-- 🔔 Notifications -->
        <section class="bg-[var(--color-sumato-surface)] p-6 rounded-xl shadow border border-[var(--color-sumato-border)]">
          <h3 class="text-lg font-semibold mb-4 text-[var(--color-sumato-text)]">🔔 Notifications & alertes</h3>
          <div class="space-y-4">
            <div>
              <label class="block font-medium mb-1">Recevoir des alertes par email :</label>
              <select v-model="userPref.alertByEmail" class="w-full px-3 py-2 rounded-lg border">
                <option :value="true">Oui</option>
                <option :value="false">Non</option>
              </select>
            </div>
            <div>
              <label class="block font-medium mb-1">Seuil humidité (%):</label>
              <input type="number" v-model="userPref.alertHumidite" class="w-full px-3 py-2 rounded-lg border" />
            </div>
            <div>
              <label class="block font-medium mb-1">Seuil température (°C):</label>
              <input type="number" v-model="userPref.alertTemperature" class="w-full px-3 py-2 rounded-lg border" />
            </div>
            <div>
              <label class="block font-medium mb-1">Fréquence des alertes :</label>
              <select v-model="userPref.alertFrequency" class="w-full px-3 py-2 rounded-lg border">
                <option>En temps réel</option>
                <option>Une fois par heure</option>
                <option>Une fois par jour</option>
              </select>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>
