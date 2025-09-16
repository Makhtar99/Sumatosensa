<script setup lang="ts">
import { reactive, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useMediaQuery } from '@vueuse/core'
import { useUserPrefStore } from '@/stores/userpref'
import { onLogout, toLogin, onDeleteAccount } from '@/assets/functions/auth'

import LogOut from '../assets/svg/logout.svg'
import UserSwitch from '../assets/svg/user-switch.svg'
import Trash from '../assets/svg/trash.svg'

const isTelephone = useMediaQuery('(max-width: 768px)')
const auth = useAuthStore()
const userPref = useUserPrefStore()
const user = reactive({ username: '', email: '' })

const generalPref = reactive({
  lang: userPref.lang,
  decimalDisplay: userPref.decimalDisplay
})

const sensors = reactive({
  sensor1: userPref.sensor1name,
  sensor2: userPref.sensor2name,
  sensor3: userPref.sensor3name
})

const units = reactive({
  temp: userPref.tempUnit,
  pressure: userPref.pressureUnit,
  humidity: userPref.humidityUnit
})

const alerts = reactive({
  alertByEmail: userPref.alertByEmail,
  alertFrequency: userPref.alertFrequency,
  minHum: userPref.alertMinHumidite,
  maxHum: userPref.alertMaxHumidite,

  minTempC: userPref.alertMinTemperatureC,
  maxTempC: userPref.alertMaxTemperatureC,
  minTempF: userPref.alertMinTemperatureF,
  maxTempF: userPref.alertMaxTemperatureF,

  minPressHpa: userPref.alertMinPressionhpa,
  maxPressHpa: userPref.alertMaxPressionhpa,
  minPressBar: userPref.alertMinPressionbar,
  maxPressBar: userPref.alertMaxPressionbar,
  minPressInHg: userPref.alertMinPressionInHg,
  maxPressInHg: userPref.alertMaxPressionInHg
})

onMounted(async () => {
  if (!auth.user) {
    try {
      await auth.getCurrentUser()
    } catch { }
  }
  user.username = auth.user?.username ?? ''
  user.email = auth.user?.email ?? ''
})

const saveGeneralPref = () => {
  userPref.lang = generalPref.lang
  userPref.decimalDisplay = generalPref.decimalDisplay
  window.alert('Préférences générales enregistrées.')
}

const saveSensors = () => {
  userPref.sensor1name = sensors.sensor1
  userPref.sensor2name = sensors.sensor2
  userPref.sensor3name = sensors.sensor3
  window.alert('Préférences générales enregistrées.')
}

const saveCity = () => {
  userPref.userCity = userPref.userCity
  window.alert('Ville enregistrée.')
}

const saveUnits = () => {
  userPref.tempUnit = units.temp
  userPref.pressureUnit = units.pressure
  userPref.humidityUnit = units.humidity
  window.alert('Préférences générales enregistrées.')
}

const saveAlerts = () => {
  userPref.alertByEmail = alerts.alertByEmail
  userPref.alertFrequency = alerts.alertFrequency
  userPref.alertMinHumidite = alerts.minHum
  userPref.alertMaxHumidite = alerts.maxHum

  if (units.temp === 'Celsius') {
    userPref.alertMinTemperatureC = alerts.minTempC
    userPref.alertMaxTemperatureC = alerts.maxTempC
  } else {
    userPref.alertMinTemperatureF = alerts.minTempF
    userPref.alertMaxTemperatureF = alerts.maxTempF
  }

  if (units.pressure === 'hPa') {
    userPref.alertMinPressionhpa = alerts.minPressHpa
    userPref.alertMaxPressionhpa = alerts.maxPressHpa
  } else if (units.pressure === 'bar') {
    userPref.alertMinPressionbar = alerts.minPressBar
    userPref.alertMaxPressionbar = alerts.maxPressBar
  } else if (units.pressure === 'inHg') {
    userPref.alertMinPressionInHg = alerts.minPressInHg
    userPref.alertMaxPressionInHg = alerts.maxPressInHg
  }
  window.alert('Alertes enregistrées.')
}
</script>

<template>
  <div class="flex flex-col gap-6" :class="isTelephone ? 'p-4' : 'p-6'">
    <h1 class="flex justify-start !my-0 !p-0 text-center title">Paramètres</h1>

    <section class="border border-var[--color-sumato-border] rounded-xl p-6 bg-[var(--color-sumato-surface)]">
      <div class="flex flex-col md:flex-row md:items-start gap-6">
        <div class="md:w-1/3">
          <h3 class="text-base font-semibold">Profil utilisateur</h3>
          <p class="text-sm text-gray-500 mt-1">Modifiez vos informations de connexion.</p>
        </div>
        <div class="md:flex-1 space-y-4">
          <input v-model="user.username" type="text" placeholder="Nom d'utilisateur"
            class="w-full px-4 py-2 rounded-lg border border-gray-300" />
          <input v-model="user.email" type="email" placeholder="Adresse email"
            class="w-full px-4 py-2 rounded-lg border border-gray-300" />
          <button :disabled="auth.isLoading" class="px-4 py-2 rounded-lg flex m-auto">
            {{ auth.isLoading ? 'Enregistrement…' : 'Enregistrer les modifications' }}
          </button>
        </div>
      </div>
    </section>

    <section class="border border-var[--color-sumato-border] rounded-xl p-6 bg-[var(--color-sumato-surface)]">
      <div class="flex flex-col md:flex-row md:items-start gap-6">
        <div class="md:w-1/3">
          <h3 class="text-base font-semibold">Préférences générales</h3>
          <p class="text-sm text-gray-500 mt-1">Langue et affichage général de l’application.</p>
        </div>
        <div class="md:flex-1 space-y-4">
          <select v-model="generalPref.lang" class="w-full px-3 py-2 rounded-lg border">
            <option value="fr">Français</option>
          </select>
          <select v-model="generalPref.decimalDisplay" class="w-full px-3 py-2 rounded-lg border">
            <option :value="true">Oui</option>
            <option :value="false">Non</option>
          </select>
          <button @click="saveGeneralPref" class="px-4 py-2 rounded-lg flex m-auto">
            Enregistrer
          </button>
        </div>
      </div>
    </section>

    <section class="border border-var[--color-sumato-border] rounded-xl p-6 bg-[var(--color-sumato-surface)]">
      <div class="flex flex-col md:flex-row md:items-start gap-6">
        <div class="md:w-1/3">
          <h3 class="text-base font-semibold">Ville</h3>
          <p class="text-sm text-gray-500 mt-1">Choisissez la ville de référence pour la température extérieure.</p>
        </div>
        <div class="md:flex-1 space-y-4">
          <select v-model="userPref.userCity" class="w-full px-3 py-2 rounded-lg border bg-[var(--color-sumato-light)]">
            <option value="Paris">Paris</option>
            <option value="Lyon">Lyon</option>
            <option value="Marseille">Marseille</option>
            <option value="Bordeaux">Bordeaux</option>
            <option value="Lille">Lille</option>
          </select>
          <button @click="saveCity" class="mt-4 px-4 py-2 rounded-lg flex m-auto">
            Enregistrer
          </button>
        </div>
      </div>
    </section>


    <section class="border border-var[--color-sumato-border] rounded-xl p-6 bg-[var(--color-sumato-surface)]">
      <div class="flex flex-col md:flex-row md:items-start gap-6">
        <div class="md:w-1/3">
          <h3 class="text-base font-semibold">Noms des capteurs</h3>
          <p class="text-sm text-gray-500 mt-1">Attribuez un nom personnalisé à vos capteurs.</p>
        </div>
        <div class="md:flex-1 space-y-4">
          <input v-model="sensors.sensor1" class="w-full p-2 rounded-lg border" placeholder="Capteur 1" />
          <input v-model="sensors.sensor2" class="w-full p-2 rounded-lg border" placeholder="Capteur 2" />
          <input v-model="sensors.sensor3" class="w-full p-2 rounded-lg border" placeholder="Capteur 3" />
          <button @click="saveSensors" class="mt-4 px-4 py-2 rounded-lg flex m-auto">
            Enregistrer
          </button>
        </div>
      </div>
    </section>

    <section class="border border-var[--color-sumato-border] rounded-xl p-6 bg-[var(--color-sumato-surface)]">
      <div class="flex flex-col md:flex-row md:items-start gap-6">
        <div class="md:w-1/3">
          <h3 class="text-base font-semibold">Unités d’affichage</h3>
          <p class="text-sm text-gray-500 mt-1">Choisissez vos unités préférées pour les mesures.</p>
        </div>
        <div class="md:flex-1 space-y-3">
          <select v-model="units.temp" class="w-full px-3 py-2 rounded-lg border">
            <option>Celsius</option>
            <option>Fahrenheit</option>
          </select>
          <select v-model="units.pressure" class="w-full px-3 py-2 rounded-lg border">
            <option>hPa</option>
          </select>
          <select v-model="units.humidity" class="w-full px-3 py-2 rounded-lg border">
            <option>%</option>
          </select>
          <button @click="saveUnits" class="mt-4 px-4 py-2 rounded-lg flex m-auto">
            Enregistrer
          </button>
        </div>
      </div>
    </section>

    <section class="border border-var[--color-sumato-border] rounded-xl p-6 bg-[var(--color-sumato-surface)]">
      <div class="flex flex-col md:flex-row md:items-start gap-6">
        <div class="md:w-1/3">
          <h3 class="text-base font-semibold">Notifications & alertes</h3>
          <p class="text-sm text-gray-500 mt-1">Définissez les seuils et la fréquence des alertes.</p>
        </div>
        <div class="md:flex-1 space-y-4">
          <div>
            <label class="block text-sm font-medium mb-1">Recevoir des alertes par email</label>
            <select v-model="alerts.alertByEmail" class="w-full px-3 py-2 rounded-lg border">
              <option :value="true">Oui</option>
              <option :value="false">Non</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium mb-1">Fréquence des alertes</label>
            <select v-model="alerts.alertFrequency" class="w-full px-3 py-2 rounded-lg border">
              <option>En temps réel</option>
              <option>Une fois par heure</option>
              <option>Une fois par jour</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium mb-1">Seuil humidité (%)</label>
            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="block text-xs text-gray-500 mb-1">Min</label>
                <input type="number" v-model="alerts.minHum" placeholder="Min"
                  class="w-full px-3 py-2 border rounded-lg" />
              </div>
              <div>
                <label class="block text-xs text-gray-500 mb-1">Max</label>
                <input type="number" v-model="alerts.maxHum" placeholder="Max"
                  class="w-full px-3 py-2 border rounded-lg" />
              </div>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium mb-1">Seuil température ({{ units.temp }})</label>
            <div class="grid grid-cols-2 gap-2" v-if="units.temp === 'Celsius'">
              <input type="number" v-model="alerts.minTempC" class="w-full px-3 py-2 border rounded-lg" />
              <input type="number" v-model="alerts.maxTempC" class="w-full px-3 py-2 border rounded-lg" />
            </div>
            <div class="grid grid-cols-2 gap-2" v-else>
              <input type="number" v-model="alerts.minTempF" class="w-full px-3 py-2 border rounded-lg" />
              <input type="number" v-model="alerts.maxTempF" class="w-full px-3 py-2 border rounded-lg" />
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium mb-1">Seuil pression ({{ units.pressure }})</label>
            <div class="grid grid-cols-2 gap-2" v-if="units.pressure === 'hPa'">
              <input type="number" v-model="alerts.minPressHpa" class="w-full px-3 py-2 border rounded-lg" />
              <input type="number" v-model="alerts.maxPressHpa" class="w-full px-3 py-2 border rounded-lg" />
            </div>
            <div class="grid grid-cols-2 gap-2" v-else-if="units.pressure === 'bar'">
              <input type="number" v-model="alerts.minPressBar" class="w-full px-3 py-2 border rounded-lg" />
              <input type="number" v-model="alerts.maxPressBar" class="w-full px-3 py-2 border rounded-lg" />
            </div>
            <div class="grid grid-cols-2 gap-2" v-else-if="units.pressure === 'inHg'">
              <input type="number" v-model="alerts.minPressInHg" class="w-full px-3 py-2 border rounded-lg" />
              <input type="number" v-model="alerts.maxPressInHg" class="w-full px-3 py-2 border rounded-lg" />
            </div>
          </div>

          <button @click="saveAlerts" class="mt-4 px-4 py-2 rounded-lg flex m-auto">
            Enregistrer
          </button>
        </div>
      </div>
    </section>

    <section class="border border-var[--color-sumato-border] rounded-xl p-6 bg-[var(--color-sumato-surface)]">
      <div class="flex flex-col md:flex-row md:items-start gap-6">
        <div class="md:w-1/3">
          <h3 class="text-base font-semibold">Gestion du compte</h3>
          <p class="text-sm text-gray-500 mt-1">Déconnectez-vous ou supprimez définitivement votre compte.</p>
        </div>
        <div class="md:flex-1 grid grid-cols-1 sm:grid-cols-2 gap-4">
          <button @click="onLogout" class="px-4 py-2 rounded-lg buttonUser flex items-center justify-center gap-2">
            <img :src="LogOut" alt="Logout" class="w-5 h-5" /> Déconnexion
          </button>
          <button @click="toLogin" class="px-4 py-2 rounded-lg flex items-center justify-center gap-2">
            <img :src="UserSwitch" alt="Switch" class="w-5 h-5" /> Changer de compte
          </button>
          <button @click="onDeleteAccount"
            class="px-4 py-2 rounded-lg buttonUser flex items-center justify-center gap-2">
            <img :src="Trash" alt="Delete" class="w-5 h-5" /> Supprimer le compte
          </button>
        </div>
      </div>
    </section>
  </div>
</template>
