
const API_URL = 'http://localhost:8000/api'

export async function login(email: string, password: string) {
  const res = await fetch(`${API_URL}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  })

  if (!res.ok) throw new Error('Échec de la connexion')

  const data = await res.json()
  localStorage.setItem('token', data.token)
  return data
}

export function logout() {
  localStorage.removeItem('token')
}

export function getToken() {
  return localStorage.getItem('token')
}

export function isAuthenticated(): boolean {
  return !!localStorage.getItem('token')
}
