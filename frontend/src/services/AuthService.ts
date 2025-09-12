const API_URL = 'http://localhost:8000'


export async function login(username: string, password: string) {
  const res = await fetch(`${API_URL}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  })

  if (!res.ok) throw new Error('Échec de la connexion')

  const data = await res.json()
  localStorage.setItem('access_token', data.access_token)
  console.log("📡 Envoi vers /login avec :", username)
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
  console.log('Données retour de register:', data)
  // Ne tente plus de stocker un token inexistant ici :
  // localStorage.setItem('access_token', data.access_token)
  console.log("✅ Réponse backend register :", data)
  return data
}

export function logout() {
  localStorage.removeItem('access_token')
  window.location.reload()
}

export function getToken() {
  return localStorage.getItem('access_token')
}

export function isAuthenticated(): boolean {
  return !!localStorage.getItem('access_token')
}

export function isAdmin(): boolean {
  const token = getToken()
  if (!token) return false

  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    return payload.is_admin || false
  } catch (e) {
    console.error('Erreur lors de la vérification du token:', e)
    return false
  }
}