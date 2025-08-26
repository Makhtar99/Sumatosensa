<script setup lang="ts">
import { ref } from 'vue';

import ExportView from './ViewExport.vue';
import HistoryView from './ViewHistory.vue';

const selectedView = ref<'history' | 'export'>('history')
</script>

<template>
    <div class="p-6">
        <h1 class="title mb-6">Gestion des données</h1>

            <div class="flex gap-4 mb-8">
        <button
            @click="selectedView = 'history'"
            :class="[
            'px-4 py-2 rounded-lg font-medium transition-all',
            selectedView === 'history'
                ? 'bg-[var(--color-primary)] text-white'
                : 'bg-[var(--color-surface)] text-[var(--color-sumato-text)] hover:bg-[var(--color-sumato-light)]'
            ]"
        >
            Historique
        </button>
        <button
            @click="selectedView = 'export'"
            :class="[
            'px-4 py-2 rounded-lg font-medium transition-all',
            selectedView === 'export'
                ? 'bg-[var(--color-primary)] text-white'
                : 'bg-[var(--color-surface)] text-[var(--color-sumato-text)] hover:bg-[var(--color-sumato-light)]'
            ]"
        >
            Exporter
        </button>
    </div>

        <HistoryView v-if="selectedView === 'history'" />
        <ExportView v-else/>
    </div>
</template>