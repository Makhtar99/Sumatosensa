<script setup lang="ts">
import { ref } from 'vue';

import Sensor1 from '../views/Datas/DataSensor1.vue'
import Sensor2 from '../views/Datas/DataSensor2.vue'
import Sensor3 from '../views/Datas/DataSensor3.vue'

// Vue sélectionnée par défaut → Salon
const selectedSensor = ref<'sensor1' | 'sensor2' | 'sensor3'>('sensor1')
</script>

<template>
  <div class="p-6">
    <!-- Titre -->
    <h1 class="title mb-6">Données des Capteurs</h1>

    <!-- Boutons pour choisir la pièce -->
    <div class="flex gap-4 mb-8">
      <button
        @click="selectedSensor = 'sensor1'"
        :class="[
          'px-4 py-2 rounded-lg font-medium transition-all',
          selectedSensor === 'sensor1'
            ? 'bg-[var(--color-primary)] text-white'
            : 'bg-[var(--color-surface)] text-[var(--color-sumato-text)] hover:bg-[var(--color-sumato-light)]'
        ]"
      >
        Salon
      </button>

      <button
        @click="selectedSensor = 'sensor2'"
        :class="[
          'px-4 py-2 rounded-lg font-medium transition-all',
          selectedSensor === 'sensor2'
            ? 'bg-[var(--color-primary)] text-white'
            : 'bg-[var(--color-surface)] text-[var(--color-sumato-text)] hover:bg-[var(--color-sumato-light)]'
        ]"
      >
        Chambre
      </button>

      <button
        @click="selectedSensor = 'sensor3'"
        :class="[
          'px-4 py-2 rounded-lg font-medium transition-all',
          selectedSensor === 'sensor3'
            ? 'bg-[var(--color-primary)] text-white'
            : 'bg-[var(--color-surface)] text-[var(--color-sumato-text)] hover:bg-[var(--color-sumato-light)]'
        ]"
      >
        Grenier
      </button>
    </div>

    <!-- Affichage dynamique des capteurs -->
    <Sensor1 v-if="selectedSensor === 'sensor1'" />
    <Sensor2 v-else-if="selectedSensor === 'sensor2'" />
    <Sensor3 v-else />
  </div>
</template>
