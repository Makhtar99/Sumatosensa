<script setup lang="ts">
import { ref, computed } from 'vue'
import notifications from '../assets/json/notification_data.json'
import X from '../assets/svg/x.svg'

const notifList = ref(
  notifications.map((n) => ({
    ...n,
    visible: true,
  })),
)
const selectedFilter = ref<'all' | 'critical' | 'warning' | 'info'>('all')

const filteredNotifList = computed(() => {
  return notifList.value.filter(
    (n) => n.visible && (selectedFilter.value === 'all' || n.importance === selectedFilter.value),
  )
})

const hideNotification = (index: number) => {
  notifList.value[index].visible = false
}

const importanceStyle: Record<string, string> = {
  info: 'border-[var(--notif-info-border)] bg-[var(--notif-info-bg)] text-[var(--notif-info-text)]',
  warning:
    'border-[var(--notif-warning-border)] bg-[var(--notif-warning-bg)] text-[var(--notif-warning-text)]',
  critical:
    'border-[var(--notif-critical-border)] bg-[var(--notif-critical-bg)] text-[var(--notif-critical-text)]',
}

const typeStyle: Record<string, string> = {
  Système: 'bg-[var(--notif-info-border)]',
  Température: 'bg-[var(--notif-critical-border)] text-[var(--color-sumato-danger)]',
  Humidité: 'bg-[var(--notif-warning-border)] text-blue-700',
  Pression: 'bg-[var(--color-sumato-card-pressure)] text-yellow-700',
  Connexion: 'bg-[var(--color-sumato-connected)] text-orange-700',
  Général: 'bg-gray-200 text-gray-700',
  Batterie: 'bg-[var(--tag-general-bg)]',
}
</script>

<template>
  <div class="flex flex-col gap-4 p-4">
    <h1 class="flex justify-start !my-0 !p-0 text-center title">Notifications & Alertes</h1>

    <div class="grid grid-cols-2 md:grid-cols-4 gap-2">
      <button
        @click="selectedFilter = 'all'"
        :aria-pressed="selectedFilter === 'all'"
        :class="[
          'px-4 py-2 font-medium transition-all border',
          'rounded-l-lg',
          selectedFilter === 'all'
            ? 'bg-[var(--color-primary)]'
            : 'hover:bg-[var(--color-sumato-light)]',
        ]"
      >
        Toutes
      </button>

      <button
        @click="selectedFilter = 'critical'"
        :aria-pressed="selectedFilter === 'critical'"
        :class="[
          'px-4 py-2 font-medium transition-all border-t border-b',
          selectedFilter === 'critical'
            ? 'bg-[var(--color-primary)]'
            : 'hover:bg-[var(--color-sumato-light)]',
        ]"
      >
        Critique
      </button>

      <button
        @click="selectedFilter = 'warning'"
        :aria-pressed="selectedFilter === 'warning'"
        :class="[
          'px-4 py-2 font-medium transition-all border-t border-b',
          selectedFilter === 'warning'
            ? 'bg-[var(--color-primary)]'
            : 'hover:bg-[var(--color-sumato-light)]',
        ]"
      >
        Avertissement
      </button>

      <button
        @click="selectedFilter = 'info'"
        :aria-pressed="selectedFilter === 'info'"
        :class="[
          'px-4 py-2 font-medium transition-all border',
          'rounded-r-lg',
          selectedFilter === 'info'
            ? 'bg-[var(--color-primary)]'
            : 'hover:bg-[var(--color-sumato-light)]',
        ]"
      >
        Information
      </button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div
        v-for="(notif, index) in filteredNotifList"
        :key="index"
        class="relative flex flex-col md:flex-row justify-between items-start md:items-center border-l-4 rounded-xl p-4 shadow"
        :class="importanceStyle[notif.importance] || importanceStyle.info"
      >
        <button
          @click="hideNotification(index)"
          class="absolute rounded-[999px] top-2 right-4 transition !p-0.5 SumatoIcon"
          title="Fermer la notification"
        >
          <img :src="X" alt="Close" class="w-4 h-4" />
        </button>

        <div class="flex-1">
          <p class="font-semibold text-base md:text-lg w-[80%]">
            {{ notif.alerte_message }}
          </p>
          <div class="flex flex-row w-full">
            <p class="font-medium whitespace-nowrap">
              Reçue le <span>{{ notif.date }}</span> à <span>{{ notif.hour }}</span>
            </p>
          </div>
        </div>

        <span
          class="mt-3 md:mt-auto px-3 py-1 rounded-full text-sm font-medium whitespace-nowrap"
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
