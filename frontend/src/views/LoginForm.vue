<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { z } from 'zod'

const loginSchema = z.object({
  username: z.string().min(2, "Le nom d'utilisateur doit contenir au moins 2 caractères").max(100, "Le nom d'utilisateur ne peut pas dépasser 100 caractères"),
  password: z.string().min(6, "Le mot de passe doit contenir au moins 6 caractères")
})

const form = reactive({
  username: '',
  password: ''
})

const errors = reactive({
  username: '',
  password: '',
  server: ''
})

const authStore = useAuthStore()
const router = useRouter()

const onSubmit = async () => {
  errors.username = ''
  errors.password = ''
  errors.server = ''

  const result = loginSchema.safeParse(form)

  if (!result.success) {
    console.error('Validation error:', result.error)
    return
  }

const credentials = ref({
  username: form.username,
  password: form.password
})

  try {
    await authStore.login(credentials.value)
    router.push('/')
  } catch (error) {
    errors.server = authStore.error || "Une erreur est survenue"
    console.error('Erreur de connexion :', error)
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
              type="username"
              class="w-full p-2 rounded-xl"
              style="border: 1px solid lightgray"
              placeholder="Renseignez votre username"
            />
            <p v-if="errors.username" class="text-red-500 text-sm mt-1">{{ errors.username }}</p>
          </div>

          <div>
            <input
              v-model="form.password"
              type="password"
              class="w-full p-2 rounded-xl"
              style="border: 1px solid lightgray"
              placeholder="Renseignez votre mot de passe"
            />
            <p v-if="errors.password" class="text-red-500 text-sm mt-1">{{ errors.password }}</p>
          </div>

          <p v-if="errors.server" class="text-red-500 text-sm text-center">{{ errors.server }}</p>

          <button type="submit" class="w-full py-2 px-4 rounded-xl cursor-pointer" style="color: var(--color-sumato-text); background: var(--color-coral);">
            Se connecter
          </button>

          <RouterLink to="/register" class="block text-center mt-4">
            Pas encore inscrit ? <span class="underline">Créez un compte</span>
          </RouterLink>
        </div>
      </form>
    </div>
  </div>
</template>
