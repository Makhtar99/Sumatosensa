import axios from 'axios'

const api = axios.create({
  baseURL: 'https://api.example.com', // à adapter selon l'environnement
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.response.use(
  response => response,
  error => {
    console.error('Erreur API:', error.response || error.message)
    return Promise.reject(error)
  }
)

export default api
