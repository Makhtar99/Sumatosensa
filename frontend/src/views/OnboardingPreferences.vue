<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserPrefStore } from '@/stores/userpref'
import DarkModeButton from './Components/DarkModeButton.vue'

const router = useRouter()
const userPref = useUserPrefStore()
const step = ref(0)

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

const general = reactive({
    lang: userPref.lang,
    decimalDisplay: userPref.decimalDisplay,
    alertByEmail: userPref.alertByEmail,
    alertFrequency: userPref.alertFrequency
})

const nextStep = () => {
    if (step.value < 5) step.value++
}
const prevStep = () => {
    if (step.value > 0) step.value--
}

const finish = () => {

    userPref.sensor1name = sensors.sensor1
    userPref.sensor2name = sensors.sensor2
    userPref.sensor3name = sensors.sensor3

    userPref.tempUnit = units.temp
    userPref.pressureUnit = units.pressure
    userPref.humidityUnit = units.humidity

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

    userPref.lang = general.lang
    userPref.decimalDisplay = general.decimalDisplay
    userPref.alertByEmail = general.alertByEmail
    userPref.alertFrequency = general.alertFrequency

    userPref.hasDoneOnboarding = true
    router.push('/dashboard')
}
</script>


<template>
    <div class="h-screen m-auto flex items-center justify-center">
        <div class="max-w-3xl mx-auto p-6 space-y-8">

            <div class="flex justify-between items-center text-sm text-gray-500">
                <span :class="step === 0 ? 'font-bold !text-[var(--color-primary)]' : ''">Intro</span>
                <span :class="step === 1 ? 'font-bold !text-[var(--color-primary)]' : ''">Capteurs</span>
                <span :class="step === 2 ? 'font-bold !text-[var(--color-primary)]' : ''">Unités</span>
                <span :class="step === 3 ? 'font-bold !text-[var(--color-primary)]' : ''">Alertes</span>
                <span :class="step === 4 ? 'font-bold !text-[var(--color-primary)]' : ''">Général</span>
                <span :class="step === 5 ? 'font-bold !text-[var(--color-primary)]' : ''">Fin</span>
                <DarkModeButton />
            </div>

            <section v-if="step === 0" class="space-y-4 text-center">
                <h1 class="text-2xl font-semibold">Bienvenue sur Sumatosensa</h1>
                <p>Configurez vos préférences pour personnaliser votre expérience.</p>
                <button @click="nextStep" class="px-6 py-2 bg-[var(--color-sumato-accent)] rounded-lg text-white">
                    Commencer
                </button>
            </section>

            <section v-if="step === 1" class="space-y-4">
                <h2 class="flex justify-start !my-0 !p-0 text-center title">Placement des capteurs</h2>
                <p>
                    Pour une meilleure expérience, nous vous recommandons d’installer vos 3 capteurs dans des pièces
                    éloignées
                    les unes des autres. Cela permet de couvrir une plus grande surface de votre logement et d’obtenir
                    des
                    données
                    plus variées et pertinentes pour vous.
                </p>
                <div class="flex justify-between">
                    <button @click="prevStep" class="px-6 py-2 border rounded-lg">Précédent</button>
                    <button @click="nextStep" class="px-6 py-2 bg-[var(--color-sumato-accent)] rounded-lg text-white">
                        J’ai placé mes capteurs
                    </button>
                </div>
            </section>

            <section v-if="step === 2" class="space-y-4">
                <h2 class="flex justify-start !my-0 !p-0 text-center title">Nommer vos capteurs</h2>
                <input v-model="sensors.sensor1" class="w-full p-2 border rounded-lg" placeholder="Capteur 1" />
                <input v-model="sensors.sensor2" class="w-full p-2 border rounded-lg" placeholder="Capteur 2" />
                <input v-model="sensors.sensor3" class="w-full p-2 border rounded-lg" placeholder="Capteur 3" />
                <div class="flex justify-between">
                    <button @click="prevStep" class="px-6 py-2 border rounded-lg">Précédent</button>
                    <button @click="nextStep"
                        class="px-6 py-2 bg-[var(--color-sumato-accent)] rounded-lg text-white">Suivant</button>
                </div>
            </section>

            <section v-if="step === 3" class="space-y-4">
                <h2 class="flex justify-start !my-0 !p-0 text-center title">Choisissez vos unités</h2>
                <select v-model="units.temp" class="w-full p-2 border rounded-lg">
                    <option>Celsius</option>
                    <option>Fahrenheit</option>
                </select>
                <select v-model="units.pressure" class="w-full p-2 border rounded-lg">
                    <option>hPa</option>
                    <option>bar</option>
                    <option>inHg</option>
                </select>
                <select v-model="units.humidity" class="w-full p-2 border rounded-lg">
                    <option>%</option>
                    <option>g/m³</option>
                </select>
                <div class="flex justify-between">
                    <button @click="prevStep" class="px-6 py-2 border rounded-lg">Précédent</button>
                    <button @click="nextStep"
                        class="px-6 py-2 bg-[var(--color-sumato-accent)] rounded-lg text-white">Suivant</button>
                </div>
            </section>

            <section v-if="step === 4" class="space-y-4">
                <h2 class="flex justify-start !my-0 !p-0 text-center title">Définissez vos seuils d’alerte</h2>

                <div>
                    <label class="block text-sm mb-1">Température ({{ units.temp }})</label>
                    <div class="grid grid-cols-2 gap-2" v-if="units.temp === 'Celsius'">
                        <input type="number" v-model="alerts.minTempC" class="p-2 border rounded-lg"
                            placeholder="Min" />
                        <input type="number" v-model="alerts.maxTempC" class="p-2 border rounded-lg"
                            placeholder="Max" />
                    </div>
                    <div class="grid grid-cols-2 gap-2" v-else>
                        <input type="number" v-model="alerts.minTempF" class="p-2 border rounded-lg"
                            placeholder="Min" />
                        <input type="number" v-model="alerts.maxTempF" class="p-2 border rounded-lg"
                            placeholder="Max" />
                    </div>
                </div>

                <div>
                    <label class="block text-sm mb-1">Pression ({{ units.pressure }})</label>
                    <div class="grid grid-cols-2 gap-2" v-if="units.pressure === 'hPa'">
                        <input type="number" v-model="alerts.minPressHpa" class="p-2 border rounded-lg"
                            placeholder="Min" />
                        <input type="number" v-model="alerts.maxPressHpa" class="p-2 border rounded-lg"
                            placeholder="Max" />
                    </div>
                    <div class="grid grid-cols-2 gap-2" v-else-if="units.pressure === 'bar'">
                        <input type="number" v-model="alerts.minPressBar" class="p-2 border rounded-lg"
                            placeholder="Min" />
                        <input type="number" v-model="alerts.maxPressBar" class="p-2 border rounded-lg"
                            placeholder="Max" />
                    </div>
                    <div class="grid grid-cols-2 gap-2" v-else>
                        <input type="number" v-model="alerts.minPressInHg" class="p-2 border rounded-lg"
                            placeholder="Min" />
                        <input type="number" v-model="alerts.maxPressInHg" class="p-2 border rounded-lg"
                            placeholder="Max" />
                    </div>
                </div>

                <div>
                    <label class="block text-sm mb-1">Humidité (%)</label>
                    <div class="grid grid-cols-2 gap-2">
                        <input type="number" v-model="alerts.minHum" class="p-2 border rounded-lg" placeholder="Min" />
                        <input type="number" v-model="alerts.maxHum" class="p-2 border rounded-lg" placeholder="Max" />
                    </div>
                </div>

                <div class="flex justify-between">
                    <button @click="prevStep" class="px-6 py-2 border rounded-lg">Précédent</button>
                    <button @click="nextStep"
                        class="px-6 py-2 bg-[var(--color-sumato-accent)] rounded-lg text-white">Suivant</button>
                </div>
            </section>

            <section v-if="step === 5" class="space-y-4">
                <h2 class="flex justify-start !my-0 !p-0 text-center title">Préférences générales</h2>
                <select v-model="general.lang" class="w-full p-2 border rounded-lg">
                    <option value="fr">Français</option>
                    <option value="en">Anglais</option>
                </select>
                <select v-model="general.decimalDisplay" class="w-full p-2 border rounded-lg">
                    <option :value="true">Afficher les décimales</option>
                    <option :value="false">Arrondir les valeurs</option>
                </select>
                <select v-model="general.alertByEmail" class="w-full p-2 border rounded-lg">
                    <option :value="true">Recevoir des alertes email</option>
                    <option :value="false">Pas d’alerte email</option>
                </select>
                <select v-model="general.alertFrequency" class="w-full p-2 border rounded-lg">
                    <option>En temps réel</option>
                    <option>Une fois par heure</option>
                    <option>Une fois par jour</option>
                </select>
                <div class="flex justify-between">
                    <button @click="prevStep" class="px-6 py-2 border rounded-lg">Précédent</button>
                    <button @click="finish" class="px-6 py-2 bg-[var(--color-sumato-accent)] rounded-lg text-white">
                        Enregistrer & Terminer
                    </button>
                </div>
            </section>
        </div>
    </div>
</template>
