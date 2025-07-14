<script setup>
import { RouterView } from 'vue-router';

import Sidebar from '@/layout/Sidebar.vue';
import Topbar from '@/layout/Topbar.vue';
import Dashboard from '@/views/Dashboard.vue';
import LoginForm from '@/views/LoginForm.vue';

// const isAuthenticated = ref(false);

</script>

<template>
    <div class="flex h-screen">
        <Sidebar />
        <div class="flex-1 flex flex-col">
        <Topbar />
        <main class="w-full p-4 flex-1 overflow-y-auto">
            <Router-view />
            <!-- <LoginForm v-else @login-success="isAuthenticated = true" /> -->
        </main>
        </div>
    </div>
</template>