<script setup>
import { reactive } from 'vue'
import { z } from 'zod'

const loginSchema = z.object({
  email: z.string().email("Email invalide"),
  password: z.string().min(6, "Le mot de passe doit contenir au moins 6 caractères")
})

const form = reactive({
  email: '',
  password: ''
})

const errors = reactive({
  email: '',
  password: ''
})

const onSubmit = () => {
  errors.email = ''
  errors.password = ''

  const result = loginSchema.safeParse(form)

  if (!result.success) {
    result.error.errors.forEach((err) => {
      const field = err.path[0]
      errors[field] = err.message
    })
    return
  }

  console.log('Connexion réussie avec :', result.data)
}
</script>

<template>
  <div class="flex h-screen items-center justify-center" style="max-height:-webkit-fill-available;">
    <div class="flex flex-col gap-2 items-center justify-center max-w-[40%] bg-white p-4 rounded-xl">
    <img src="../assets/img/Logo_auth.png" alt="Logo">
    <form @submit.prevent="onSubmit" class="max-w-md m-auto space-y-6">
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
            placeholder="Renseignez votre mot de passe"
          />
          <p v-if="errors.password" class="text-red-500 text-sm mt-1">{{ errors.password }}</p>
        </div>

        <button type="submit" class="w-full py-2 px-4 rounded-xl cursor-pointer" style="color: var(--color-text); background: var(--color-coral);">
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

