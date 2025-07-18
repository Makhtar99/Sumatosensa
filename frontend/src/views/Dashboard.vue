<script setup>


import Temp from '../views/Datas/Temperature.vue'
import Humidity from '../views/Datas/Humidity.vue'
import Pressure from '../views/Datas/Pressure.vue'
import Outside from '../views/Datas/Outside.vue'
import ConnectedDevices from './Datas/ConnectedDevices.vue'

// import { useUserStore } from '../stores/userStore';
</script>

<template>
    <div class="flex gap-5">
        <div class="flex flex-col">
            <h1 class="text-2xl font-bold" style="margin: 0; padding: 0;">Bienvenue <span v-if="userInfo"> {{ username }}</span> !</h1>
            <div>
                <img src="../assets/img/house.png" alt="mézon" style="width: 90%; height: 300px; margin-left: 20px; margin-top: 20px;" />
            </div>
            <div class="dashboard_data">
                <Temp />
                <Humidity />
                <Pressure />
                <Outside />
            </div>
        </div>
        <div class="flex flex-col justify-between" style="width: 20%; margin: auto;">
            <ConnectedDevices />
        </div>
    </div>
</template>