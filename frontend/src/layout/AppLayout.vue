<script setup>
import { computed, ref } from 'vue';

import Sidebar from '@/layout/Sidebar.vue';
import Topbar from '@/layout/Topbar.vue';
import Content from '@/layout/Content.vue';

</script>

<template>
    <div class="app-layout">
        <div class="sidebar">
            <Sidebar />
        </div>
        <div class="main-content">
            <Topbar />
            <Content />
        </div>
    </div>
</template>