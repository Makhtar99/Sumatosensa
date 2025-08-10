<script setup lang="ts">
import { ref } from 'vue'

const username = ref('NomUtilisateur')
const email = ref('utilisateur@exemple.com')

const theme = ref('Clair')
const tempUnit = ref('Celsius')
const pressureUnit = ref('hPa')
const humidityUnit = ref('%')
const decimalDisplay = ref(true)
const lang = ref('fr')

const alertHumidite = ref(30)
const alertTemperature = ref(28)
const alertByEmail = ref(true)
const alertFrequency = ref('Une fois par heure')
</script>

<template>
  <div class="p-6">
    <h2 class="title">⚙️ Paramètres</h2>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6">

      <div class="md:col-span-2 space-y-6">

        <section class="bg-[var(--color-surface)] p-6 rounded-xl shadow border border-[var(--color-sumato-border)]">
          <h3 class="text-lg font-semibold mb-4 text-[var(--color-text)]">👤 Profil utilisateur</h3>
          <p class="mb-2 text-[var(--color-text)]"><span class="font-medium">Nom :</span> {{ username }}</p>
          <p class="mb-4 text-[var(--color-text)]"><span class="font-medium">Email :</span> {{ email }}</p>
          <div class="flex flex-col sm:flex-row gap-4 mt-4">
            <button class="px-4 py-2 bg-[var(--color-sumato-primary)] hover:bg-[var(--color-sumato-primary-hover)] text-white rounded-lg">
              Modifier le profil
            </button>
            <button class="px-4 py-2 bg-[var(--color-sumato-danger)] hover:bg-red-600 text-white rounded-lg">
              Modifier le mot de passe
            </button>
          </div>
        </section>

        <section class="bg-[var(--color-surface)] p-6 rounded-xl shadow border border-[var(--color-sumato-border)]">
          <h3 class="text-lg font-semibold mb-4 text-[var(--color-text)]">🌐 Préférences générales</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block font-medium mb-1">Thème :</label>
              <select v-model="theme" class="w-full px-3 py-2 rounded-lg bg-[var(--color-sumato-light)] border border-[var(--color-sumato-border)]">
                <option>Clair</option>
                <option>Sombre</option>
              </select>
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

        <section class="bg-[var(--color-surface)] p-6 rounded-xl shadow border border-[var(--color-sumato-border)]">
          <h3 class="text-lg font-semibold mb-4 text-[var(--color-text)]">📊 Affichage & données</h3>
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

        <section class="bg-[var(--color-surface)] p-6 rounded-xl shadow border border-[var(--color-sumato-border)]">
          <h3 class="text-lg font-semibold mb-4 text-[var(--color-text)]">🔔 Notifications & alertes</h3>
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

      <div class="hidden md:block">
        <img
          src="../assets/img/setting_boy.png"
          alt="Illustration"
          class="w-full h-auto rounded-xl object-cover border border-[var(--color-sumato-border)]"
        />
      </div>
    </div>
  </div>
</template>
