<script setup lang="ts">
  import { RouterView } from 'vue-router';
  console.log("🚀 App montée avec router et token :", localStorage.getItem('token'))
</script>

<template>
    <div class="wrapper">
      <router-view />
    </div>
</template>
