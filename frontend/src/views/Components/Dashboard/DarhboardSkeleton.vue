<script setup lang="ts">
import { useMediaQuery } from '@vueuse/core'

const isTelephone = useMediaQuery('(max-width: 768px)')
</script>

<template>
    <div v-if="!isTelephone" class="flex flex-col gap-6 h-screen">
      <h3 class="flex justify-start text-center title">Chargement...</h3>
      <div class="flex items-start gap-4">
        <PrimeSkeleton width="15rem" height="3rem" class="mb-2"></PrimeSkeleton>
      </div>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
        <PrimeSkeleton width="20rem" height="20rem"></PrimeSkeleton>
        <PrimeSkeleton width="20rem" height="20rem"></PrimeSkeleton>
        <PrimeSkeleton width="20rem" height="20rem"></PrimeSkeleton>
        <PrimeSkeleton width="20rem" height="20rem"></PrimeSkeleton>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 w-full">
        <PrimeSkeleton width="30rem" height="15rem"></PrimeSkeleton>
        <PrimeSkeleton width="30rem" height="15rem"></PrimeSkeleton>
        <PrimeSkeleton width="30rem" height="15rem"></PrimeSkeleton>
      </div>
    </div>
    <div v-if="isTelephone" class="flex gap-3 flex-col h-screen">
      <h3 class="flex justify-start text-center title">Chargement...</h3>
      <div class="flex flex-col items-center gap-4">
        <PrimeSkeleton width="10rem" height="3rem" class="mb-2"></PrimeSkeleton>
        <PrimeSkeleton width="10rem" height="3rem" class="mb-2"></PrimeSkeleton>
      </div>
      <div class="grid grid-cols-2 xl:grid-cols-4 gap-6 p-6 w-full">
        <PrimeSkeleton width="10rem" height="15rem"></PrimeSkeleton>
        <PrimeSkeleton width="10rem" height="15rem"></PrimeSkeleton>
        <PrimeSkeleton width="10rem" height="15rem"></PrimeSkeleton>
        <PrimeSkeleton width="10rem" height="15rem"></PrimeSkeleton>
      </div>
      <div class="h-fit m-auto space-y-5">
        <PrimeSkeleton width="15rem" height="15rem"></PrimeSkeleton>
        <PrimeSkeleton width="15rem" height="15rem"></PrimeSkeleton>
        <PrimeSkeleton width="15rem" height="15rem"></PrimeSkeleton>
      </div>
    </div>
</template>