<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { z } from 'zod'

const router = useRouter()
const auth = useAuthStore()

import Logo from '@/assets/img/Logo_auth.png'
import LogoDark from '@/assets/img/Logo_auth_dark.png'

const registerSchema = z.object({
  username: z.string().min(3, "Le nom d'utilisateur doit contenir au moins 3 caractères"),
  email: z.string().email("Email invalide"),
  password: z.string().min(6, "Le mot de passe doit contenir au moins 6 caractères"),
  confirmPassword: z.string()
}).refine(data => data.password === data.confirmPassword, {
  message: "Les mots de passe ne correspondent pas",
  path: ["confirmPassword"]
})

const form = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const errors = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  general: ''
})

const errorMessages = ref<string[]>([])

function clearErrors() {
  errors.value = { username: '', email: '', password: '', confirmPassword: '', general: '' }
  errorMessages.value = []
}

function mapZodErrors(issues: import('zod').ZodIssue[]) {
  for (const issue of issues) {
    const field = (issue.path?.[0] as keyof typeof errors.value) ?? 'general'
    if (field in errors.value && !errors.value[field]) {
      errors.value[field] = issue.message
    }
  }
}

function errorFormMessage(err: unknown) {
  const msg = err instanceof Error ? err.message : String(err ?? '')
  const push = (m: string) => { if (!errorMessages.value.includes(m)) errorMessages.value.push(m) }

  if (/Network error|Failed to fetch|HTTP 0/i.test(msg)) {
    push("Serveur injoignable. Vérifiez votre connexion ou l’URL de l’API.")
    push("Réessayez dans quelques instants.")
    return
  }

  if (/HTTP 409|already|exists|taken|duplicate/i.test(msg)) {
    push("Cet email ou nom d’utilisateur est déjà utilisé.")
    push("Essayez avec un autre identifiant ou utilisez la page de connexion.")
  }

  if (/HTTP 422|validation/i.test(msg)) {
    push("Données invalides côté serveur. Vérifiez les champs et réessayez.")
  }

  if (/HTTP 401|unauthor/i.test(msg)) {
    push("Action non autorisée. Connectez-vous puis réessayez.")
  }

  if (/HTTP 400|bad request/i.test(msg)) {
    push("Requête invalide. Vérifiez les informations saisies.")
  }

  if (msg && !/^HTTP \d{3}$/.test(msg)) push(msg)
}

const onSubmit = async () => {
  clearErrors()

  const result = registerSchema.safeParse(form.value)
  if (!result.success) {
    mapZodErrors(result.error.issues)
    errorMessages.value.push("Veuillez corriger les champs en rouge puis réessayez.")
    return
  }

  try {
    await auth.registerAndLogin({
      username: result.data.username,
      email: result.data.email,
      password: result.data.password,
    })

    const redirect = (router.currentRoute.value.query.redirect as string) ?? '/'
    router.push(redirect)
  } catch (e: unknown) {
    errors.value.general =
      e instanceof Error ? (e.message || "Erreur lors de l’inscription.") : "Erreur lors de l’inscription."
    errorFormMessage(e)
  }
}
</script>

<template>
  <div class="flex h-screen items-center justify-center" style="max-height:-webkit-fill-available;">
    <div class="flex flex-col gap-2 items-center justify-center w-full max-w-[480px] p-6 rounded-xl shadow">
      <img :src="Logo" alt="Logo" class="img_light" />
      <img :src="LogoDark" alt="Logo" class="img_dark" />

      <form @submit.prevent="onSubmit" class="w-full space-y-5 mt-4">
        <div class="flex flex-col gap-4">
          <div>
            <input
              v-model="form.username"
              type="text"
              class="w-full p-2 rounded-xl"
              style="border: 1px solid lightgray"
              placeholder="Nom d'utilisateur"
              autocomplete="username"
            />
            <p v-if="errors.username" class="text-[var(--color-sumato-danger)] text-sm mt-1 flex justify-center">{{ errors.username }}</p>
          </div>

          <div>
            <input
              v-model="form.email"
              type="email"
              class="w-full p-2 rounded-xl"
              style="border: 1px solid lightgray"
              placeholder="Renseignez votre email"
              autocomplete="email"
            />
            <p v-if="errors.email" class="text-[var(--color-sumato-danger)] text-sm mt-1 flex justify-center">{{ errors.email }}</p>
          </div>

          <div>
            <input
              v-model="form.password"
              type="password"
              class="w-full p-2 rounded-xl"
              style="border: 1px solid lightgray"
              placeholder="Créez un mot de passe"
              autocomplete="new-password"
            />
            <p v-if="errors.password" class="text-[var(--color-sumato-danger)] text-sm mt-1 flex justify-center">{{ errors.password }}</p>
          </div>

          <div>
            <input
              v-model="form.confirmPassword"
              type="password"
              class="w-full p-2 rounded-xl"
              style="border: 1px solid lightgray"
              placeholder="Confirmez votre mot de passe"
              autocomplete="new-password"
            />
            <p v-if="errors.confirmPassword" class="text-[var(--color-sumato-danger)] text-sm mt-1 flex justify-center">{{ errors.confirmPassword }}</p>
          </div>

          <button
            type="submit"
            class="w-full py-2 px-4 rounded-xl cursor-pointer"
            :disabled="auth.isLoading"
          >
            {{ auth.isLoading ? 'Création en cours…' : 'Créer un compte' }}
          </button>

          <RouterLink to="/login" class="block text-center mt-2">
            Déjà inscrit ? <span class="underline">Connectez-vous</span>
          </RouterLink>
        </div>

        <p v-if="errors.general" class="text-[var(--color-sumato-danger)] text-sm  flex justify-center text-center mt-2">
          {{ errors.general }}
        </p>

      </form>
    </div>
  </div>
</template>
