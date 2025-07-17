const API_URL = 'http://localhost:8000'


export async function login(email: string, password: string) {
  const res = await fetch(`${API_URL}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  })

  if (!res.ok) throw new Error('Échec de la connexion')

  const data = await res.json()
  localStorage.setItem('access_token', data.access_token)
  console.log("📡 Envoi vers /login avec :", email)
  console.log("✅ Token reçu après login :", data.access_token)
  console.log("localStorage contient :", localStorage)
  return data
}

export async function register(username: string, email: string, password: string) {
  const res = await fetch(`${API_URL}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, email, password }),
  })
  console.log(`➡️ POST vers ${API_URL}/auth/register`)

  if (!res.ok) throw new Error('Échec de l\'inscription')

  const data = await res.json()
  localStorage.setItem('access_token', data.access_token)
  console.log("✅ Réponse backend register :", data)
  console.log("💾 Token stocké :", data.access_token)
  console.log("localStorage contient :", localStorage)
  return data
}

export function logout() {
  localStorage.removeItem('access_token')
}

export function getToken() {
  return localStorage.getItem('access_token')
}

export function isAuthenticated(): boolean {
  return !!localStorage.getItem('access_token')
}
