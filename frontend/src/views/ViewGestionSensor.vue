<!-- src/views/GestionSensor.vue -->
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { fetchSensor, createSensor, updateSensor, deleteSensor, type Sensor } from '@/services/sensorService'

const loading = ref(false)
const savingAll = ref(false)
const error = ref<string | null>(null)
const sensors = ref<Sensor[]>([])

const originalNames = ref<Map<number, string>>(new Map())
const newName = ref('')

const loadSensors = async () => {
  loading.value = true
  error.value = null
  try {
    const data = await fetchSensor()
    sensors.value = data
    // reset snapshot
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

const isRowDirty = (s: Sensor) => originalNames.value.get(s.id) !== s.name
const hasDirty = computed(() => sensors.value.some(isRowDirty))

const saveRow = async (s: Sensor) => {
  if (!isRowDirty(s)) return
  try {
    const updated = await updateSensor(s.id, { name: s.name })
    originalNames.value.set(s.id, updated.name ?? '')
  } catch (e: unknown) {
    console.error(`Capteur ${s.id}: échec de la mise à jour`, e)
  }
}

const saveAll = async () => {
  if (!hasDirty.value || savingAll.value) return
  savingAll.value = true
  try {
    const promises = sensors.value
      .filter(isRowDirty)
      .map(s => updateSensor(s.id, { name: s.name }))
    const updated = await Promise.all(promises)
    for (const u of updated) originalNames.value.set(u.id, u.name)
  } catch (e: unknown) {
    console.error('Erreur lors de l’enregistrement global', e)
  } finally {
    savingAll.value = false
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

const removeSensor = async (id: number) => {
  try {
    await deleteSensor(id)
    await loadSensors()
  } catch (e: unknown) {
    console.error(`Erreur lors de la suppression du capteur ${id}`, e)
  }
}
</script>

<template>
  <div class="flex flex-col gap-3 p-4 md:p-6">
    
    <h2 class="flex justify-center !mt-0 !p-0 mb-4">Gestion des capteurs</h2>

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
        <div class="flex items-center gap-2">
          <button
            class="px-4 py-2 rounded-lg bg-[var(--color-sumato-accent)] disabled:opacity-50"
            :disabled="!hasDirty || savingAll"
            @click="saveAll"
          >
            {{ savingAll ? 'Enregistrement…' : 'Enregistrer les noms modifiés' }}
          </button>
          <button
            class="px-3 py-2 rounded-lg border"
            @click="loadSensors"
          >
            Recharger
          </button>
        </div>
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
            <label class="block text-sm font-medium mb-1">Nom du capteur #{{ s.id }}</label>
            <input
              v-model="s.name"
              type="text"
              class="w-full p-2 rounded-lg border"
              placeholder="Nom du capteur"
            />
          </div>

          <div class="flex gap-2 justify-end">
            <button
              class="px-4 py-2 rounded-lg bg-[var(--color-primary)] disabled:opacity-50"
              :disabled="!isRowDirty(s)"
              @click="saveRow(s)"
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

        <div v-if="!sensors.length" class="text-sm opacity-70">Aucun capteur pour le moment.</div>
      </div>
    </div>

  </div>
</template>
