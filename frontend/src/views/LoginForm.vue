<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'
import { z } from 'zod'

const loginSchema = z.object({
  username: z.string()
    .min(2, "Le nom d'utilisateur doit contenir au moins 2 caractères")
    .max(100, "Le nom d'utilisateur ne peut pas dépasser 100 caractères"),
  password: z.string().min(6, 'Le mot de passe doit contenir au moins 6 caractères'),
})

const form = reactive({ username: '', password: '' })
const errors = reactive({ username: '', password: '', server: '' })
const errorMessages = ref<string[]>([]) // tableau de messages contextuels

const auth = useAuthStore()
const { isLoading, error: authError } = storeToRefs(auth)

const router = useRouter()

function clearErrors() {
  errors.username = ''
  errors.password = ''
  errors.server = ''
  errorMessages.value = []
}

function mapZodErrors(issues: import('zod').ZodIssue[]) {
  for (const issue of issues) {
    const field = (issue.path?.[0] as keyof typeof errors) ?? 'server'
    if (field in errors && !errors[field]) {
      errors[field] = issue.message
    }
  }
  if (issues.length) errorMessages.value.push("Veuillez corriger les champs en rouge puis réessayez.")
}

function setFriendlyErrorHints(err: unknown) {
  const raw = err instanceof Error ? err.message : String(err ?? '')
  const push = (m: string) => { if (!errorMessages.value.includes(m)) errorMessages.value.push(m) }

  if (/Network error|Failed to fetch|TypeError: Failed to fetch|HTTP 0/i.test(raw)) {
    push("Serveur injoignable. Vérifiez votre connexion ou l’URL de l’API.")
    push("Réessayez dans quelques instants.")
    return
  }
  if (/HTTP 401|unauthor/i.test(raw)) {
    push("Identifiants invalides. Vérifiez le nom d’utilisateur et le mot de passe.")
  }
  if (/HTTP 422|validation/i.test(raw)) {
    push("Données invalides côté serveur. Revérifiez les champs.")
  }
  if (/HTTP 429|too many/i.test(raw)) {
    push("Trop de tentatives. Patientez quelques minutes avant de réessayer.")
  }
  if (/HTTP 5\d{2}/i.test(raw)) {
    push("Erreur serveur. Réessayez plus tard.")
  }
  if (raw && !/^HTTP \d{3}$/.test(raw)) push(raw)
}

const onSubmit = async () => {
  clearErrors()

  const result = loginSchema.safeParse(form)
  if (!result.success) {
    mapZodErrors(result.error.issues)
    return
  }

  try {
    await auth.login({ username: form.username, password: form.password })
    const redirect = (router.currentRoute.value.query.redirect as string) ?? '/'
    router.push(redirect)
  } catch (e) {
    errors.server = authError.value ?? 'Une erreur est survenue'
    setFriendlyErrorHints(e)
    if (errors.username) document.getElementById('username')?.focus()
    else if (errors.password) document.getElementById('password')?.focus()
  }
}
</script>

<template>
  <div class="flex h-screen items-center justify-center" style="max-height: -webkit-fill-available">
    <div
      class="flex flex-col gap-2 items-center justify-center max-w-[40%] bg-[var(--color-sumato-surface)] p-4 rounded-xl"
    >
      <img src="../assets/img/Logo_auth.png" alt="Logo" class="img_light" />
      <img src="../assets/img/Logo_auth_dark.png" alt="Logo" class="img_dark" />

      <form @submit.prevent="onSubmit" class="max-w-md m-auto space-y-6" autocomplete="on">
        <div class="flex flex-col gap-4">
          
          <div>
            <label for="username" class="sr-only">Nom d’utilisateur</label>
            <input
              id="username"
              name="username"
              v-model="form.username"
              type="text"
              autocomplete="username"
              autocapitalize="none"
              autocorrect="off"
              spellcheck="false"
              class="w-full p-2 rounded-xl !text-[var(--color-sumato-text)]"
              style="border: 1px solid lightgray"
              placeholder="Renseignez votre username"
              :aria-invalid="!!errors.username"
              :aria-describedby="errors.username ? 'err-username' : undefined"
            />
            <p v-if="errors.username" id="err-username" class="text-[var(--color-sumato-danger)] text-sm mt-1">
              {{ errors.username }}
            </p>
          </div>

          <div>
            <label for="password" class="sr-only">Mot de passe</label>
            <input
              id="password"
              name="password"
              v-model="form.password"
              type="password"
              autocomplete="current-password"
              class="w-full p-2 rounded-xl !text-[var(--color-sumato-text)]"
              style="border: 1px solid lightgray"
              placeholder="Renseignez votre mot de passe"
              :aria-invalid="!!errors.password"
              :aria-describedby="errors.password ? 'err-password' : undefined"
            />
            <p v-if="errors.password" id="err-password" class="text-[var(--color-sumato-danger)] text-sm mt-1">
              {{ errors.password }}
            </p>
          </div>

          <p v-if="errors.server" class="text-[var(--color-sumato-danger)] text-sm text-center" role="alert">
            {{ errors.server }}
          </p>

          <button
            type="submit"
            class="w-full py-2 px-4 rounded-xl cursor-pointer"
            :disabled="isLoading"
          >
            {{ isLoading ? 'Connexion…' : 'Se connecter' }}
          </button>

          <RouterLink to="/register" class="block text-center mt-4">
            Pas encore inscrit ? <span class="underline">Créez un compte</span>
          </RouterLink>
        </div>
      </form>
    </div>
  </div>
</template>
