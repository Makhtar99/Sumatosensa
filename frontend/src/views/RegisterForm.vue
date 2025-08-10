<script setup lang="ts">
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { z } from 'zod'
import { register } from '../services/AuthService'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()

const registerSchema = z.object({
  username: z.string().min(3, "Le nom d'utilisateur doit contenir au moins 3 caractères"),
  email: z.string().email("Email invalide"),
  password: z.string().min(6, "Le mot de passe doit contenir au moins 6 caractères"),
  confirmPassword: z.string()
}).refine(data => data.password === data.confirmPassword, {
  message: "Les mots de passe ne correspondent pas",
  path: ["confirmPassword"]
})

const form = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

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
   console.error('Validation error:', result.error)
    return
  }

  try {
    await register(result.data.username, result.data.email, result.data.password)

    const authStore = useAuthStore()
    const credentials = {
      username: result.data.username,
      password: result.data.password
    }
    await authStore.login(credentials)

    router.push('/')
  } catch (error: unknown) {
    if (error instanceof Error) {
      errors.general = error.message || 'Erreur lors de l’inscription.'
    } else {
      errors.general = 'Erreur lors de l’inscription.'
    }
  }
}


</script>

<template>
  <div class="flex h-screen items-center justify-center" style="max-height:-webkit-fill-available;">
    <div class="flex flex-col gap-2 items-center justify-center max-w-[40%] bg-white p-4 rounded-xl">
      <img src="../assets/img/Logo_auth.png" alt="Logo" />

      <form @submit.prevent="onSubmit" class="max-w-md m-auto space-y-6">
        <div class="flex flex-col gap-4">
          
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

          <button type="submit" class="w-full py-2 px-4 rounded-xl cursor-pointer" style="color: var(--color-text); background: var(--color-coral);">
            Créer un compte
          </button>

          <RouterLink to="/login" class="block text-center mt-4">
            Déjà inscrit ? <span class="underline">Connectez-vous</span>
          </RouterLink>
        </div>

        <p v-if="errors.general" class="text-red-500 text-sm text-center mt-4">
          {{ errors.general }}
        </p>
      </form>
    </div>
  </div>
</template>
