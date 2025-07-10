<script setup>
import { computed, ref } from 'vue';

import Sidebar from '@/layout/Sidebar.vue';
import Topbar from '@/layout/Topbar.vue';
import Dashboard from '@/layout/Dashboard.vue';

</script>

<template>
    <div class="app-layout">
        <div class="sidebar">
            <Sidebar />
        </div>
        <div class="main-content">
            <Topbar />
            <Dashboard />
        </div>
    </div>
</template>