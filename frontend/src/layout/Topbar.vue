<template>
    <header class="flex items-center justify-between p-4 bg-red-500 text-white w-full h-[100px]">
    <h1>HEADER</h1>
    <router-link to="/logIn" class="btn">
      Connexion
    </router-link>
    </header>
</template>

<script setup>
import { RouterLink } from 'vue-router';
</script>

<style>
.btn {
    background-color: #fff;
    color: #000;
    padding: 10px 20px;
    border-radius: 5px;
    text-decoration: none;
    height: 50px;
    width: 150px;
    border: 2px solid black;
}
</style>