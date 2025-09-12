<script setup lang="ts">
import Temp from './Datas/DataTemperature.vue'
import Humidity from './Datas/DataHumidity.vue'
import Pressure from './Datas/DataPressure.vue'
import Outside from './Datas/DataOutside.vue'
</script>

<template>
    <div class="flex flex-col">
        <div>
            <img src="../assets/img/house.png" alt="mézon" style="width: 70%; height: 300px; margin-left: 20px; margin-top: 20px;" />
        </div>
        <div class="flex">
            <Temp />
            <Humidity />
            <Pressure />
            <Outside />
        </div>
    </div>
</template>