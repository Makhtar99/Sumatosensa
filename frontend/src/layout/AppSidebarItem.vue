<script setup lang="ts">
import { useMediaQuery } from '@vueuse/core'

const isTelephone = useMediaQuery('(max-width: 768px)')

defineProps({
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
      'flex items-center gap-3 p-3 rounded-xl transition hover:bg-[var(--color-sumato-primary-hover)]',
      (to === '/' ? isExactActive : isActive) ? 'bg-[var(--color-primary)] font-semibold' : '',
      isSidebarCollapsed ? 'justify-center' : 'justify-start',
      isTelephone ? 'flex flex-col' : ''
    ]"
  >
    <img :src="icon" :alt="label" class="w-5 h-5 sidebarIcon" />
    <transition name="fade">
      <span v-show="!isSidebarCollapsed" class="text-sm truncate text-[var(--sumato-text)]">
        {{ label }}
      </span>
    </transition>
  </div>
</router-link>
</template>