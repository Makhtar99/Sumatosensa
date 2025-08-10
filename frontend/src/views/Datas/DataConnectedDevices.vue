<script setup lang="ts">
import { ref } from 'vue'
import Fan from '../../assets/svg/fan.svg'
import Heat from '../../assets/svg/heat.svg'
import Deshumidifier from '../../assets/svg/deshumidifier.svg'

const devices = ref([
  {name: "Ventilateur", icon: Fan, status: "Non connecté"},
  {name: "Chauffage", icon: Heat, status: "Non connecté"},
  {name: "Déshumidificateur", icon: Deshumidifier, status: "Non connecté"}
])
</script>

<template>
  <div class="connected-devices">
    <li v-for="device in devices" :key="device.name">
      <div class="connected-device">
        <img :src="device.icon" alt="Device Icon" class="w-25 h-25" />
        <h4>{{ device.name }}</h4>
        <p>{{ device.status }}</p>
      </div>
    </li>
  </div>
</template>
