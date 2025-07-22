<script setup>
import Temp from '../views/Datas/Temperature.vue'
import Humidity from '../views/Datas/Humidity.vue'
import Pressure from '../views/Datas/Pressure.vue'
import Outside from '../views/Datas/Outside.vue'
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