<script setup lang="ts">
import Fan from '../../assets/svg/fan.svg'
import Heat from '../../assets/svg/heat.svg'
import Deshumidifier from '../../assets/svg/deshumidifier.svg'
</script>

<template>
  <div class="connected-devices flex flex-col gap-3 rounded-xl">
    <div
      class="flex flex-col items-center p-4 rounded-xl w-60 h-48"
      style="border: 1px solid var(--color-sumato-connected-devices)"
    >
      <img :src="Fan" alt="Fan" />
      <h4>Ventilateur</h4>
      <p>Non connecté</p>
    </div>
    <div
      class="flex flex-col items-center p-4 rounded-xl w-60 h-48"
      style="border: 1px solid var(--color-sumato-connected-devices)"
    >
      <img :src="Heat" alt="Heat" />
      <h4>Chauffage</h4>
      <p>Non connecté</p>
    </div>
    <div
      class="flex flex-col items-center p-4 rounded-xl w-60 h-48"
      style="border: 1px solid var(--color-sumato-connected-devices)"
    >
      <img :src="Deshumidifier" alt="Dehumidifier" />
      <h4>Déshumidificateur</h4>
      <p>Non connecté</p>
    </div>
  </div>
</template>
