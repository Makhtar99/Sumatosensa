<script setup>
import Temp from '../layout/Datas/Temperature.vue'
import Humidity from '../layout/Datas/Humidity.vue'
import Pressure from '../layout/Datas/Pressure.vue'
import Outside from '../layout/Datas/Outside.vue'
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