<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

const form = ref({
  username: '',
  email: '',
  password: ''
})

const register = async () => {
  try {
    const response = await axios.post('http://localhost:8000/auth/register', form.value)
    console.log('✅ Utilisateur enregistré :', response.data)
    alert('Utilisateur enregistré avec succès')
  } catch (error) {
    console.error('❌ Erreur:', error.response?.data?.detail || error.message)
    alert('Erreur: ' + (error.response?.data?.detail || error.message))
  }
}
</script>

<template>
  <form @submit.prevent="register" style="max-width: 400px; margin: auto; padding: 1rem; border: 1px solid #ccc; border-radius: 6px;">
    <h2>Inscription</h2>
    <label>Nom d'utilisateur</label>
    <input v-model="form.username" required placeholder="Nom" />

    <label>Email</label>
    <input v-model="form.email" type="email" required placeholder="Email" />

    <label>Mot de passe</label>
    <input v-model="form.password" type="password" required placeholder="Mot de passe" />

    <button type="submit" style="margin-top: 1rem;">S'inscrire</button>
  </form>
</template>

<style scoped>
input {
  display: block;
  width: 100%;
  margin-bottom: 0.75rem;
  padding: 0.5rem;
  border: 1px solid #aaa;
  border-radius: 4px;
}
button {
  padding: 0.5rem 1rem;
}
</style>
