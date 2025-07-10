<script setup>
import { computed, ref } from 'vue';

import Sidebar from '@/layout/Sidebar.vue';
import Topbar from '@/layout/Topbar.vue';
import Footer from '@/layout/Footer.vue';

</script>

<template>
    <div class="app-layout">
        <Sidebar />
        <div class="main-content">
            <Topbar />
            <slot />
            <Footer />
        </div>
    </div>
</template>