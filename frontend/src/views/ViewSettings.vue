<script setup lang="ts">
import { ref, onMounted, reactive, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import DarkModeButton from './Components/DarkModeButton.vue'

const tempUnit = ref('Celsius')
const pressureUnit = ref('hPa')
const humidityUnit = ref('%')
const decimalDisplay = ref(true)
const lang = ref('fr')

const alertHumidite = ref(30)
const alertTemperature = ref(28)
const alertByEmail = ref(false)
const alertFrequency = ref('En temps réel')

const auth = useAuthStore()
const user = reactive({ username: '', email: '' })

onMounted(async () => {
  if (!auth.user) {
    try { await auth.getCurrentUser() } catch {}
  }
  user.username = auth.user?.username ?? ''
  user.email = auth.user?.email ?? ''
})

const username = computed(() => user.username)
const email = computed(() => user.email)

const isDirty = computed(() =>
  user.username !== (auth.user?.username ?? '') ||
  user.email    !== (auth.user?.email ?? '')
)

// const onSubmit = async () => {
//   try {
//     await auth.putCurrentUser({ username: user.username, email: user.email })
//   } catch (e) {
//     console.error("Erreur lors de la mise à jour du profil :", e)
//   }
// }

</script>

<template>
  <div class="p-6">
    <h1 class="title !mt-0 mb-6">Paramètres</h1>

    <div class="grid grid-cols-1 gap-6 mt-6">

      <div class="md:col-span-2 space-y-6">

        <section class="bg-[var(--color-sumato-surface)] p-6 rounded-xl shadow border border-[var(--color-sumato-border)]">
  <h3 class="text-lg font-semibold mb-4 text-[var(--color-sumato-text)]">👤 Profil utilisateur</h3>

  <p class="mb-2 text-[var(--color-sumato-text)]"><span class="font-medium">Nom :</span> {{ username }}</p>
  <p class="mb-4 text-[var(--color-sumato-text)]"><span class="font-medium">Email :</span> {{ email }}</p>

  <div class="flex flex-col sm:flex-row gap-4 mt-4">
    <input
      id="username"
      name="username"
      v-model="user.username"
      type="text"
      autocomplete="username"
      class="w-full p-2 rounded-xl !text-[var(--color-sumato-text)]"
      style="border: 1px solid lightgray"
      placeholder="Modifier votre nom d’utilisateur"
    />
    <input
      id="email"
      name="email"
      v-model="user.email"
      type="email"
      autocomplete="email"
      class="w-full p-2 rounded-xl !text-[var(--color-sumato-text)]"
      style="border: 1px solid lightgray"
      placeholder="Modifier votre email"
    />
  </div>

  <button
    @click="onSubmit"
    :disabled="!isDirty || auth.isLoading"
    class="mt-4 w-full px-4 py-2 bg-[var(--color-sumato-accent)] text-white rounded-lg disabled:opacity-50"
  >
    {{ auth.isLoading ? 'Enregistrement…' : 'Enregistrer les modifications' }}
  </button>
</section>

        <section class="bg-[var(--color-sumato-surface)] p-6 rounded-xl shadow border border-[var(--color-sumato-border)]">
          <h3 class="text-lg font-semibold mb-4 text-[var(--color-sumato-text)]">🌐 Préférences générales</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block font-medium mb-1">Thème :</label>
                <dark-mode-button class="w-full" />
            </div>
            <div>
              <label class="block font-medium mb-1">Langue :</label>
              <select v-model="lang" class="w-full px-3 py-2 rounded-lg bg-[var(--color-sumato-light)] border border-[var(--color-sumato-border)]">
                <option value="fr">Français</option>
                <option value="en">Anglais</option>
              </select>
            </div>
          </div>
        </section>

        <section class="bg-[var(--color-sumato-surface)] p-6 rounded-xl shadow border border-[var(--color-sumato-border)]">
          <h3 class="text-lg font-semibold mb-4 text-[var(--color-sumato-text)]">📊 Affichage & données</h3>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label class="block font-medium mb-1">Unité de température :</label>
              <select v-model="tempUnit" class="w-full px-3 py-2 rounded-lg bg-[var(--color-sumato-light)] border border-[var(--color-sumato-border)]">
                <option>Celsius</option>
                <option>Fahrenheit</option>
              </select>
            </div>
            <div>
              <label class="block font-medium mb-1">Unité de pression :</label>
              <select v-model="pressureUnit" class="w-full px-3 py-2 rounded-lg bg-[var(--color-sumato-light)] border border-[var(--color-sumato-border)]">
                <option>hPa</option>
                <option>bar</option>
              </select>
            </div>
            <div>
              <label class="block font-medium mb-1">Unité d’humidité :</label>
              <select v-model="humidityUnit" class="w-full px-3 py-2 rounded-lg bg-[var(--color-sumato-light)] border border-[var(--color-sumato-border)]">
                <option>%</option>
                <option>g/m³</option>
              </select>
            </div>
            <div>
              <label class="block font-medium mb-1">Afficher les décimales :</label>
              <select v-model="decimalDisplay" class="w-full px-3 py-2 rounded-lg bg-[var(--color-sumato-light)] border border-[var(--color-sumato-border)]">
                <option :value="true">Oui</option>
                <option :value="false">Non</option>
              </select>
            </div>
          </div>
        </section>

        <section class="bg-[var(--color-sumato-surface)] p-6 rounded-xl shadow border border-[var(--color-sumato-border)]">
          <h3 class="text-lg font-semibold mb-4 text-[var(--color-sumato-text)]">🔔 Notifications & alertes</h3>
          <div class="space-y-4">
            <div>
              <label class="block font-medium mb-1">Recevoir des alertes par email :</label>
              <select v-model="alertByEmail" class="w-full px-3 py-2 rounded-lg bg-[var(--color-sumato-light)] border border-[var(--color-sumato-border)]">
                <option :value="true">Oui</option>
                <option :value="false">Non</option>
              </select>
            </div>

            <div>
              <label class="block font-medium mb-1">Seuil d’alerte pour l’humidité (%):</label>
              <input
                type="number"
                min="0"
                max="100"
                v-model="alertHumidite"
                class="w-full px-3 py-2 rounded-lg border border-[var(--color-sumato-border)] bg-[var(--color-sumato-light)]"
              />
            </div>
            
            <div>
              <label class="block font-medium mb-1">Seuil d’alerte pour la température (°C):</label>
              <input
                type="number"
                min="0"
                max="100"
                v-model="alertTemperature"
                class="w-full px-3 py-2 rounded-lg border border-[var(--color-sumato-border)] bg-[var(--color-sumato-light)]"
              />
            </div>

            <div>
              <label class="block font-medium mb-1">Fréquence des alertes :</label>
              <select v-model="alertFrequency" class="w-full px-3 py-2 rounded-lg border border-[var(--color-sumato-border)] bg-[var(--color-sumato-light)]">
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
