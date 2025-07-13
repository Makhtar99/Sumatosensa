<template>
  <aside class="h-screen w-64 bg-gray-900 text-white flex flex-col">

    <div class="px-6 py-5 text-xl font-bold border-b border-gray-700">
      <span>📊 GestionPro</span>
    </div>

    <nav class="flex flex-col px-4 py-4 space-y-2">
      <SidebarItem icon="🏠" label="Dashboard" to="/" />
      <SidebarItem icon="👥" label="Utilisateurs" to="/users" />
      <SidebarItem icon="📈" label="Rapports" to="/reports" />
      <SidebarItem icon="⚙️" label="Paramètres" to="/settings" />
    </nav>

    <div class="px-4 py-4 border-t border-gray-700">
      <SidebarItem icon="🚪" label="Déconnexion" to="/logout" />
    </div>
  </aside>
</template>

<script setup>
import SidebarItem from './SidebarItem.vue'
</script>

<style scoped>
/* Tu peux ajouter des animations ici si besoin */
</style>
