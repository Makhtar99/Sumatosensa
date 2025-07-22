<script setup lang="ts">
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { z } from 'zod'
import { register } from '../services/AuthService'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()

// Schéma de validation Zod
const registerSchema = z.object({
  username: z.string().min(3, "Le nom d'utilisateur doit contenir au moins 3 caractères"),
  email: z.string().email("Email invalide"),
  password: z.string().min(6, "Le mot de passe doit contenir au moins 6 caractères"),
  confirmPassword: z.string()
}).refine(data => data.password === data.confirmPassword, {
  message: "Les mots de passe ne correspondent pas",
  path: ["confirmPassword"]
})


// Formulaire réactif
const form = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

// 3. Gestion des erreurs
const errors = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  general: ''
})


const onSubmit = async () => {
  Object.keys(errors).forEach((key) => errors[key as keyof typeof errors] = '')

  const result = registerSchema.safeParse(form)

  if (!result.success) {
    result.error.errors.forEach(err => {
      const field = err.path[0]
      if (field in errors) {
        errors[field as keyof typeof errors] = err.message
      }
    })
    return
  }

  try {
    // ✅ Étape 1 : Enregistrement
    await register(result.data.username, result.data.email, result.data.password)

    // ✅ Étape 2 : Connexion automatique
    const authStore = useAuthStore()
    const credentials = {
      username: result.data.username,
      password: result.data.password
    }
    await authStore.login(credentials)

    // ✅ Étape 3 : Redirection vers dashboard
    router.push('/')
  } catch (error: any) {
    errors.general = error.message || 'Erreur lors de l’inscription.'
  }

  console.log("📤 Formulaire soumis :", form)
  console.log("✅ Validation réussie :", result.data)
}


</script>

<template>
  <div class="flex h-screen items-center justify-center" style="max-height:-webkit-fill-available;">
    <div class="flex flex-col gap-2 items-center justify-center max-w-[40%] bg-white p-4 rounded-xl">
      <img src="../assets/img/Logo_auth.png" alt="Logo" />

      <form @submit.prevent="onSubmit" class="max-w-md m-auto space-y-6">
        <div class="flex flex-col gap-4">
          
          <!-- Champ username -->
          <div>
            <input
              v-model="form.username"
              type="text"
              class="w-full p-2 rounded-xl"
              style="border: 1px solid lightgray"
              placeholder="Nom d'utilisateur"
            />
            <p v-if="errors.username" class="text-red-500 text-sm mt-1">{{ errors.username }}</p>
          </div>
          <!-- Champ email -->
          <div>
            <input
              v-model="form.email"
              type="email"
              class="w-full p-2 rounded-xl"
              style="border: 1px solid lightgray"
              placeholder="Renseignez votre email"
            />
            <p v-if="errors.email" class="text-red-500 text-sm mt-1">{{ errors.email }}</p>
          </div>

          <!-- Mot de passe -->
          <div>
            <input
              v-model="form.password"
              type="password"
              class="w-full p-2 rounded-xl"
              style="border: 1px solid lightgray"
              placeholder="Créez un mot de passe"
            />
            <p v-if="errors.password" class="text-red-500 text-sm mt-1">{{ errors.password }}</p>
          </div>

          <!-- Confirmation -->
          <div>
            <input
              v-model="form.confirmPassword"
              type="password"
              class="w-full p-2 rounded-xl"
              style="border: 1px solid lightgray"
              placeholder="Confirmez votre mot de passe"
            />
            <p v-if="errors.confirmPassword" class="text-red-500 text-sm mt-1">{{ errors.confirmPassword }}</p>
          </div>

          <!-- Bouton -->
          <button type="submit" class="w-full py-2 px-4 rounded-xl cursor-pointer" style="color: var(--color-text); background: var(--color-coral);">
            Créer un compte
          </button>

          <RouterLink to="/login" class="block text-center mt-4">
            Déjà inscrit ? <span class="underline">Connectez-vous</span>
          </RouterLink>
        </div>

        <!-- Erreur serveur -->
        <p v-if="errors.general" class="text-red-500 text-sm text-center mt-4">
          {{ errors.general }}
        </p>
      </form>
    </div>
  </div>
</template>
