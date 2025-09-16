import { useAuthStore } from '@/stores/auth'

export type User = {
  id: number
  email: string
  name: string
  created_at: string
  updated_at: string
}

export async function onLogout() {
  const auth = useAuthStore()
  await auth.logout()
  window.location.reload()
}

export async function toLogin() {
  const auth = useAuthStore()
  await auth.logout()
  window.location.href = '/login'
}

export async function onDeleteAccount() {
  const auth = useAuthStore()
  if (!confirm('Êtes-vous sûr de vouloir supprimer votre compte ? Cette action est irréversible.')) return
  try {
    await auth.logout()
    alert('Votre compte a été supprimé.')
    window.location.href = '/login'
  } catch (e) {
    console.error('Erreur lors de la suppression du compte :', e)
    alert("Échec de la suppression du compte. Veuillez réessayer plus tard.")
  }
}
