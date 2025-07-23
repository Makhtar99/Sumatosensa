<script setup>
import { ref, inject } from 'vue';
defineProps({
  icon: String,
  label: String,
  to: String
});

const isSidebarCollapsed = inject('isSidebarCollapsed', ref(false));
</script>

<template>
  <router-link :to="to" v-slot="{ isActive }">
    <div
      :class="[
        'flex items-center gap-3 p-3 rounded-xl transition hover:bg-[#7cabf7]',
        isActive ? 'bg-[#3B82F6] font-semibold' : '',
        isSidebarCollapsed ? 'justify-center' : 'justify-start'
      ]"
    >
      <img
        :src="icon"
        :alt="label"
        class="w-5 h-5"
      />
       <transition name="fade">
        <span
          v-show="!isSidebarCollapsed"
          class="text-sm truncate text-var(--sumato-text)"
        >
          {{ label }}
        </span>
      </transition>
    </div>
  </router-link>
</template>