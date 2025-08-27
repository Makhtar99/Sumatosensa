<script setup lang="ts">
import { ref, computed } from 'vue'
import notifications from '../assets/json/notification_data.json'

const notifList = ref(notifications)

const importanceFilter = ref<'all' | 'critical' | 'warning' | 'info'>('all')

const filteredNotifList = computed(() => {
  if (importanceFilter.value === 'all') return notifList.value
  return notifList.value.filter(n => n.importance === importanceFilter.value)
})

const importanceStyle: Record<string, string> = {
   info:     'border-[var(--notif-info-border)] bg-[var(--notif-info-bg)] text-[var(--notif-info-text)]',
  warning:  'border-[var(--notif-warning-border)] bg-[var(--notif-warning-bg)] text-[var(--notif-warning-text)]',
  critical: 'border-[var(--notif-critical-border)] bg-[var(--notif-critical-bg)] text-[var(--notif-critical-text)]',
}

const typeStyle: Record<string, string> = {
  Système: 'bg-[var(--color-sumato-neutral)] text-[var(--color-sumato-text)]',
  Température: 'bg-[var(--color-sumato-card-temp)] text-[var(--color-sumato-danger)]',
  Humidité: 'bg-[var(--color-sumato-card-humidity)] text-blue-700',
  Pression: 'bg-[var(--color-sumato-card-pressure)] text-yellow-700',
  Connexion: 'bg-[var(--color-sumato-connected)] text-orange-700',
  Général: 'bg-gray-200 text-gray-700'
}
</script>

<template>
  <div class="p-6">
    <h1 class="title mb-6">🔔 Notifications & Alertes</h1>

    <div class="mb-6 max-w-sm">
      <label for="importanceFilter" class="block mb-2 text-sm font-medium text-[var(--color-sumato-text)]">Filtrer par importance :</label>
      <select
        id="importanceFilter"
        v-model="importanceFilter"
        class="block w-full p-2 border border-[var(--color-sumato-border)] rounded-md bg-white text-[var(--color-sumato-text)]"
      >
        <option value="all">Toutes</option>
        <option value="critical">Critique</option>
        <option value="warning">Avertissement</option>
        <option value="info">Information</option>
      </select>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div
        v-for="(notif, index) in filteredNotifList"
        :key="index"
        class="flex flex-col md:flex-row justify-between items-start md:items-center border-l-4 rounded-xl p-4 shadow bg-[var(--color-surface)]"
        :class="importanceStyle[notif.importance] || importanceStyle.info"
      >
        <div class="flex-1">
          <p class="font-semibold text-base md:text-lg text-[var(--color-sumato-text)]">
            {{ notif.alerte_message }}
          </p>
          <span class="text-sm opacity-70 mt-1 block">{{ notif.date }}</span>
        </div>

        <span
          class="mt-3 md:mt-0 px-3 py-1 rounded-full text-sm font-medium whitespace-nowrap"
          :class="typeStyle[notif.type] || typeStyle['Général']"
        >
          {{ notif.type || 'Général' }}
        </span>
      </div>
    </div>

    <div v-if="filteredNotifList.length === 0" class="text-center text-gray-500 italic mt-10">
      Aucune notification à afficher pour ce filtre.
    </div>
  </div>
</template>
