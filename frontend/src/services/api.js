import axios from 'axios'

export const API_BASE_URL = 'http://127.0.0.1:8000/api/v1'
export const API_ORIGIN = new URL(API_BASE_URL).origin

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
})

// Interceptor: Antes de cada petición, revisa si hay un token y lo añade
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Interceptor: Manejar errores 401 (Unauthorized)
api.interceptors.response.use(
  response => response, // Si la respuesta es exitosa, la devuelve
  error => {
    // Si el error es 401 (Unauthorized)
    if (error.response && error.response.status === 401) {
      console.log('Token expirado o inválido, cerrando sesión...')
      // Limpiar localStorage
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      // Redirigir al login
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api