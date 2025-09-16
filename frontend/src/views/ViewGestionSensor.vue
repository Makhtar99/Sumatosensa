<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useUserPrefStore } from '@/stores/userpref'
import {
  fetchSensor,
  createSensor,
  deleteSensor,
  type Sensor
} from '@/services/sensorService'

const loading = ref(false)
const error = ref<string | null>(null)
const sensors = ref<Sensor[]>([])
const userPref = useUserPrefStore()

const originalNames = ref<Map<number, string>>(new Map())
const newName = ref('')

const loadSensors = async () => {
  loading.value = true
  error.value = null
  try {
    const data = await fetchSensor()
    sensors.value = data
    const snap = new Map<number, string>()
    for (const s of data) snap.set(s.id, s.name ?? '')
    originalNames.value = snap
  } catch (e: unknown) {
    console.error(e)
    error.value = (e as Error)?.message ?? 'Erreur lors du chargement des capteurs.'
  } finally {
    loading.value = false
  }
}

onMounted(loadSensors)

const saveSensors = () => {
  userPref.sensor1name = sensors.value[0].name
  userPref.sensor2name = sensors.value[1].name
  userPref.sensor3name = sensors.value[2].name
  window.alert('Préférences générales enregistrées.')
}

const removeSensor = async (id: number) => {
  try {
    await deleteSensor(id)
    await loadSensors()
  } catch (e: unknown) {
    console.error(`Erreur lors de la suppression du capteur ${id}`, e)
  }
}

const addSensor = async () => {
  const name = newName.value.trim()
  if (!name) return
  try {
    await createSensor({ name })
    newName.value = ''
    await loadSensors()
  } catch (e: unknown) {
    console.error('Erreur lors de la création du capteur', e)
  }
}

const getModel = (s: Sensor) => {
  if (s.id === 1) return userPref.sensor1name
  if (s.id === 2) return userPref.sensor2name
  if (s.id === 3) return userPref.sensor3name
  return s.name
}
</script>


<template>
  <div class="flex flex-col gap-3 p-2">

    <div class="p-4 rounded-xl border mb-4">
      <h3 class="font-medium mb-2">Ajouter un capteur</h3>
      <div class="flex gap-2 items-center">
        <input
          v-model="newName"
          type="text"
          class="flex-1 p-2 rounded-lg border"
          placeholder="Nom du capteur (ex. Salon)"
        />
        <button
          class="px-4 py-2 rounded-lg disabled:opacity-50"
          :disabled="!newName.trim()"
          @click="addSensor"
        >
          Ajouter
        </button>
      </div>
    </div>

    <div class="p-4 rounded-xl border">
      <div class="flex items-center justify-between mb-3">
        <h3 class="font-medium">Capteurs existants</h3>
        <button class="px-3 py-2 rounded-lg border" @click="loadSensors">
          Recharger
        </button>
      </div>

      <div v-if="loading" class="text-sm opacity-70">Chargement…</div>
      <div v-else-if="error" class="text-sm text-[var(--color-sumato-danger)]">{{ error }}</div>

      <div v-else class="space-y-3">
        <div
          v-for="s in sensors"
          :key="s.id"
          class="flex flex-col md:flex-row items-stretch md:items-center gap-2 p-3 rounded-lg border"
        >
          <div class="flex-1">
            <label class="block text-sm font-medium mb-1">Capteur #{{ s.id }}</label>
            <input
              :value="getModel(s)"
              @input="val => {
                if (s.id === 1) userPref.sensor1name = val.target.value
                else if (s.id === 2) userPref.sensor2name = val.target.value
                else if (s.id === 3) userPref.sensor3name = val.target.value
                else s.name = val.target.value
              }"
              type="text"
              class="w-full p-2 rounded-lg border"
              placeholder="Nom du capteur"
            />
          </div>

          <div class="flex gap-2 justify-end">
            <button
              class="px-4 py-2 rounded-lg bg-[var(--color-primary)]"
              @click="saveSensors()"
            >
              Enregistrer
            </button>
            <button
              class="px-4 py-2 rounded-lg bg-[var(--color-sumato-danger)]"
              @click="removeSensor(s.id)"
              title="Supprimer"
            >
              Supprimer
            </button>
          </div>
        </div>

        <div v-if="!sensors.length" class="text-sm opacity-70">
          Aucun capteur pour le moment.
        </div>
      </div>
    </div>
  </div>
</template>
