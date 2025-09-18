<script setup lang="ts">
import { useMediaQuery } from '@vueuse/core'

const isTelephone = useMediaQuery('(max-width: 768px)')

const props = defineProps({
  icon: String,
  label: String,
  to: {
    type: String,
    default: '/dashboard'
  },
  isSidebarCollapsed: Boolean,
});

</script>

<template>
  <router-link :to="to" v-slot="{ isActive, isExactActive }">
  <div
    :class="[
      'flex items-center relative gap-3 p-3 rounded-xl hover:bg-[var(--color-sumato-primary-hover)]',
      (to === '/' ? isExactActive : isActive) ? 'bg-[var(--color-primary)] font-semibold' : '',
      isSidebarCollapsed ? 'justify-center' : 'justify-start',
      isTelephone ? 'flex flex-col' : ''
    ]"
  >
    <img :src="icon" :alt="label" class="w-5 h-5 SumatoIcon" />
    <div v-if="props.label === 'Alertes'" class="absolute w-4 h-4 bg-red-600 text-white text-xs font-bold rounded-full flex items-center justify-center" style="left: 1.3rem; top: 0.2rem;">
        6
    </div>
    <transition name="fade">
      <span v-show="!isSidebarCollapsed" class="text-sm truncate">
        {{ label }}
      </span>
    </transition>
  </div>
</router-link>
</template>