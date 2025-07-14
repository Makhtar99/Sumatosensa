<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

import { z } from 'zod'

const router = useRouter()

const registerSchema = z.object({
  email: z.string().email("Email invalide"),
  password: z.string().min(6, "Le mot de passe doit contenir au moins 6 caractères"),
  confirmPassword: z.string()
}).refine(data => data.password === data.confirmPassword, {
  message: "Les mots de passe ne correspondent pas",
  path: ["confirmPassword"]
})

const form = reactive({
  email: '',
  password: '',
  confirmPassword: ''
})

const errors = reactive({
  email: '',
  password: '',
  confirmPassword: '',
  general: ''
})

const onSubmit = async () => {
  errors.email = ''
  errors.password = ''
  errors.confirmPassword = '',
  errors.general = ''

  const result = registerSchema.safeParse(form)

  if (!result.success) {
    result.error.errors.forEach(err => {
      const field = err.path[0]
      errors[field] = err.message
    })
    return
  }
  try {
    await registerUser(result.data)
    // console.log('Inscription réussie avec :', result.data)
    router.push('/login')
  } catch (error) {
    if (error.response && error.response.data && error.response.data.message) {
      errors.general = error.response.data.message
    } else {
      errors.general = "Une erreur est survenue. Veuillez réessayer."
    }
  }
}

const registerUser = (data) => {
  return axios.post('/api/register', {
    email: data.email,
    password: data.password
  })
}
</script>


<template>
  <div class="flex h-screen items-center justify-center" style="max-height:-webkit-fill-available;">
    <div class="flex flex-col gap-2 items-center justify-center max-w-[40%] bg-white p-4 rounded-xl">
      <img src="../assets/img/Logo_auth.png" alt="Logo" />
      <form action="/" @submit.prevent="onSubmit" class="max-w-md m-auto space-y-6">
        <div class="flex flex-col gap-4">
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

          <button @click="registerUser" type="submit" class="w-full py-2 px-4 rounded-xl cursor-pointer" style="color: var(--color-text); background: var(--color-coral);">
            Créer un compte
          </button>
          <RouterLink to="/login" class="block text-center mt-4">
            Déjà inscrit ? <span class="underline">Connectez-vous</span>
          </RouterLink>
        </div>
        <p v-if="errors.general" class="text-red-500 text-sm text-center">{{ errors.general }}</p>
      </form>
    </div>
  </div>
</template>
