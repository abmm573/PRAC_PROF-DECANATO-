import { defineStore } from 'pinia'
import api from '../services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: JSON.parse(localStorage.getItem('user')) || null,
  }),

  getters: {
    // Helpers de rol para usar en templates fácilmente
    esAdministrador: (state) => state.user?.rol === 'ADMINISTRADOR',
    esEncargado:     (state) => state.user?.rol === 'ENCARGADO',
    esPasante:       (state) => state.user?.rol === 'PASANTE',
  },

  actions: {
    async login(email, password) {
      // 1. Autenticación → obtener token JWT
      const formData = new URLSearchParams()
      formData.append('username', email)
      formData.append('password', password)

      const response = await api.post('/usuarios/login', formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      })
      this.token = response.data.access_token
      localStorage.setItem('token', this.token)

      // 2. Descargar perfil del usuario (incluye rol, username, etc.)
      try {
        const profileResponse = await api.get('/usuarios/me')
        this.user = profileResponse.data
        localStorage.setItem('user', JSON.stringify(this.user))
      } catch (error) {
        console.error('Error al obtener el perfil del usuario:', error)
        this.logout()
        throw error
      }
    },

    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    },

    // Ruta de inicio según el rol del usuario autenticado
    rutaInicio() {
      const rol = this.user?.rol
      if (rol === 'ADMINISTRADOR') return '/admin'
      if (rol === 'ENCARGADO')     return '/encargado'
      return '/dashboard'
    }
  }
})