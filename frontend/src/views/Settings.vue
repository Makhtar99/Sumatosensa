<script setup>
import { ref } from 'vue'

const username = ref('username')
const email = ref('username@example.com')
</script>

<template>
  <div class="p-8 text-gray-800 bg-[#fef3d7] min-h-screen">
    <h2 class="text-3xl font-bold mb-8 flex items-center gap-3">⚙️ Paramètres</h2>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
      <!-- Colonne principale -->
      <div class="md:col-span-2 space-8">
        <!-- Profil utilisateur -->
        <section class="flex flex-col bg-[#fef3d7] rounded-xl shadow p-6 gap-3 border">
          <h3 class="text-xl font-semibold mb-4 flex items-center">👤 Profil utilisateur</h3>
          <p><span class="font-semibold">Nom :</span> {{ username }}</p>
          <p><span class="font-semibold">Email :</span> {{ email }}</p>
          <button class="mt-4 px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg">
            Modifier le profil
          </button>
          <button class="mt-4 px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-lg">
            Modifier le mot de passe
          </button>
        </section>
        <!-- Préférences -->
        <section class="flex flex-col gap-4 bg-[#fef3d7] rounded-xl shadow p-6 space-y-6 border">
          <h3 class="text-xl font-semibold mb-4">🌐 Préférences</h3>
          <div>
            <label class="block font-medium">Thème :</label>
            <select class="border mt-1 border rounded px-3 py-2 bg-gray-50 w-full" name="theme" id="theme">
              <option>Clair</option>
              <option>Sombre</option>
            </select>
            <div class="mb-4">
              <label class="block font-medium">Unité de température :</label>
              <div class="flex gap-3 mt-2">
                <select class="border rounded px-3 py-2 bg-gray-50" name="temperature-unit" id="temperature-unit">
                  <option value="celsius">°C</option>
                  <option value="fahrenheit">°F</option>
                </select>
              </div>
            </div>
          </div>
        </section>
      </div>
      <!-- Illustration -->
      <div class="hidden md:block">
        <img
          src="../assets/img/setting_boy.png"
          alt="Illustration utilisateur"
          class="w-full h-auto rounded-xl object-cover"
        />
      </div>
    </div>
  </div>
</template>
