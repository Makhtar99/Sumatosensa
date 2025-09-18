<script setup lang="ts">
import { ref } from 'vue'
import Fan from '../../assets/svg/fan.svg'
import Heat from '../../assets/svg/heat.svg'
import Deshumidifier from '../../assets/svg/deshumidifier.svg'

interface Device {
  name: string
  icon: string
  status: DeviceStatus
}

const devices = ref<Device[]>([
  { name: "Ventilateur chambre", icon: Fan, status: 'connected' },
  { name: "Chauffage salon", icon: Heat, status: 'connected' },
  { name: "Déshumidificateur cuisine", icon: Deshumidifier, status: 'disconnected' }
])

type DeviceStatus = 'connected' | 'disconnected' | 'connecting'
const errorMessage = ref('Impossible de connecter l\'appareil')

const toggleDeviceStatus = (device: Device) => {
  if (device.status === 'connecting') return

  const isConnecting = device.status === 'disconnected'
  device.status = 'connecting'

  setTimeout(() => {
    device.status = isConnecting ? 'connected' : 'disconnected'
  }, 2000)
}

</script>

<template>
  <ul class="grid grid-cols-1 md:grid-cols-3 gap-6 w-full mt-6">
    <li
      v-for="device in devices"
      :key="device.name"
      class="relative flex flex-col items-center p-4 rounded-xl
             bg-[var(--color-sumato-surface)] backdrop-blur-md border border-[var(--color-sumato-border)]
             shadow-md hover:shadow-lg transition-all"
    >
      <div class="absolute top-3 right-3">
        <label class="inline-flex items-center cursor-pointer relative">
          <input
            type="checkbox"
            class="sr-only"
            :checked="device.status === 'connected'"
            :disabled="device.status === 'connecting'"
            @change="toggleDeviceStatus(device)"
          />
          <div
            class="w-11 h-6 bg-gray-300 rounded-full transition-all peer-checked:bg-[var(--color-sumato-success)]"
            :class="{
              'bg-[var(--color-sumato-success)]': device.status === 'connected',
              'bg-[var(--color-sumato-danger)]': device.status === 'disconnected'
            }"
          ></div>
          <div
            class="dot absolute left-1 top-1 w-4 h-4 rounded-full transition-all transform"
            :class="{
              'translate-x-5': device.status === 'connected'
            }"
            :style="{ backgroundColor: 'var(--color-sumato-surface)' }"
          ></div>
        </label>
      </div>

      <img :src="device.icon" alt="Device Icon" class="w-16 h-16 mb-2" />

      <div class="flex flex-col justify-between items-center gap-3 w-full">
        <h5 class="text-lg font-semibold text-[var(--color-sumato-text)] text-center m-0">
          {{ device.name }}
        </h5>

        <div
          class="px-2 text-xs font-medium rounded-md h-fit flex items-center gap-1"
          :class="{
            'bg-[var(--color-sumato-success)] text-white': device.status === 'connected',
            'bg-[var(--color-sumato-danger)] text-white': device.status === 'disconnected',
            'bg-[var(--color-sumato-neutral)] text-[var(--color-sumato-text)]': device.status === 'connecting'
          }"
        >
          <span v-if="device.status === 'connecting'" class="loader"></span>
          {{ device.status === 'connecting' ? 'En connexion…' : (device.status === 'connected' ? 'Connecté' : 'Non connecté') }}
        </div>

        <small
          v-if="device.status === 'disconnected'"
          class="text-[var(--color-sumato-danger)] text-center"
        >
          {{ errorMessage }}
        </small>

        <div class="flex justify-end">
          <small class="text-gray-500">Dernière mise à jour : 09/09/2025 - 14:30</small>
        </div>
      </div>
    </li>
  </ul>
</template>

<style scoped>
.loader {
  border: 2px solid rgba(0, 0, 0, 0.1);
  border-top: 2px solid var(--color-sumato-text);
  border-radius: 9999px;
  width: 12px;
  height: 12px;
  animation: spin 0.6s linear infinite;
  display: inline-block;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>