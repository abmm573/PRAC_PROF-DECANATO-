<template>
  <div class="min-h-screen flex items-center justify-center umsa-page px-4 relative">
    <!-- Botón de volver al inicio en la esquina superior derecha -->
    <button @click="volverAlInicio" 
      class="absolute top-4 right-4 flex items-center gap-2 py-2 px-4 border border-gray-300 rounded-md shadow-sm
             text-sm font-medium text-gray-700 bg-white hover:bg-gray-50
             focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition-colors">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
      </svg>
      Volver al Inicio
    </button>

    <div class="max-w-md w-full umsa-card rounded-lg p-8">

      <div class="text-center mb-8">
        <h2 class="text-3xl font-bold text-gray-800">Iniciar Sesión</h2>
        <p class="text-gray-600 mt-2">Facultad de Ciencias Sociales - UMSA</p>
        <p class="text-sm text-gray-500">Sistema de Control de Asistencia de Pasantes</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-6">

        <div>
          <label for="email" class="block text-sm font-medium text-gray-700">Correo Electrónico</label>
          <input
            v-model="email"
            id="email"
            type="email"
            required
            class="mt-1 appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm
                   placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            placeholder="tu@correo.com"
          />
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-gray-700">Contraseña</label>
          <div class="mt-1 relative">
            <input
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              id="password"
              required
              class="appearance-none block w-full px-3 py-2 pr-10 border border-gray-300 rounded-md shadow-sm
                     placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              placeholder="••••••••"
            />
            <button
              type="button"
              @click="showPassword = !showPassword"
              class="absolute inset-y-0 right-0 pr-3 flex items-center"
            >
              <svg 
                v-if="showPassword" 
                class="w-5 h-5 text-gray-400 hover:text-gray-600" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"/>
              </svg>
              <svg 
                v-else 
                class="w-5 h-5 text-gray-400 hover:text-gray-600" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
              </svg>
            </button>
          </div>
          <div class="mt-2 text-right">
            <button type="button" @click="abrirModalReset"
              class="text-xs font-medium text-blue-700 hover:text-blue-800 hover:underline">
              Olvidaste tu contrasena
            </button>
          </div>
        </div>

        <div v-if="errorMessage" class="text-red-600 text-sm text-center bg-red-50 p-2 rounded">
          {{ errorMessage }}
        </div>

        <button
          type="submit"
          :disabled="isLoading"
          class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm
                 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700
                 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500
                 disabled:opacity-50 transition-colors"
        >
          <span v-if="isLoading">Iniciando...</span>
          <span v-else>Entrar</span>
        </button>

      </form>

      <!-- Modal recuperar contrasena -->
      <div v-if="showResetModal" class="fixed inset-0 z-50 flex items-start sm:items-center justify-center bg-slate-900/60 px-4 py-8 backdrop-blur-sm overflow-y-auto">
        <div class="bg-white w-full max-w-md rounded-xl shadow-2xl border border-gray-200 overflow-hidden max-h-[calc(100vh-4rem)] flex flex-col">
          <div class="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
            <h3 class="text-lg font-bold text-gray-800">Recuperar contrasena</h3>
            <button @click="cerrarModalReset" class="text-gray-500 hover:text-gray-800">X</button>
          </div>
          <div class="p-6 overflow-y-auto">
            <p class="text-sm text-gray-600 mb-4">
              Ingresa tu correo. Si existe una cuenta, se enviara un enlace de recuperacion.
            </p>

            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700">Correo</label>
                <input v-model="resetEmail" type="email" required placeholder="tu@correo.com"
                  class="mt-1 appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm
                         placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
              </div>

              <div v-if="resetMensajeOk" class="text-emerald-700 text-sm text-center bg-emerald-50 p-2 rounded border border-emerald-200">
                {{ resetMensajeOk }}
              </div>
              <div v-if="resetErrorMessage" class="text-red-600 text-sm text-center bg-red-50 p-2 rounded border border-red-200">
                {{ resetErrorMessage }}
              </div>

              <button type="button" @click="enviarReset" :disabled="isResetLoading"
                class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm
                       text-sm font-medium text-white bg-blue-600 hover:bg-blue-700
                       focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500
                       disabled:opacity-50 transition-colors">
                <span v-if="isResetLoading">Enviando...</span>
                <span v-else>Enviar enlace</span>
              </button>

              <button type="button" @click="cerrarModalReset"
                class="w-full flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm
                       text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 transition-colors">
                Cerrar
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

const email      = ref('')
const password   = ref('')
const showPassword = ref(false)
const isLoading  = ref(false)
const errorMessage = ref('')
const showResetModal = ref(false)
const resetEmail = ref('')
const isResetLoading = ref(false)
const resetErrorMessage = ref('')
const resetMensajeOk = ref('')

const authStore = useAuthStore()
const router    = useRouter()

const volverAlInicio = () => {
  // Redirigir a la página principal o landing page
  window.location.href = '/' // O puedes usar router.push('/') si tienes una ruta de inicio
}

const handleLogin = async () => {
  isLoading.value    = true
  errorMessage.value = ''

  try {
    await authStore.login(email.value, password.value)

    const rol = authStore.user?.rol
    console.log('Rol detectado:', rol)

    // ✅ Redirección según los 3 roles del sistema
    if (rol === 'ADMINISTRADOR') {
      router.push('/admin')
    } else if (rol === 'ENCARGADO') {
      router.push('/encargado')
    } else {
      router.push('/dashboard')   // PASANTE
    }

  } catch (error) {
    if (error.response?.status === 401) {
      errorMessage.value = 'Correo o contraseña incorrectos.'
    } else if (error.response?.status === 403) {
      errorMessage.value = 'Tu cuenta está desactivada. Contacta al administrador.'
    } else {
      errorMessage.value = 'Error al conectar con el servidor.'
    }
  } finally {
    isLoading.value = false
  }
}

const abrirModalReset = () => {
  resetEmail.value = email.value || ''
  resetErrorMessage.value = ''
  resetMensajeOk.value = ''
  showResetModal.value = true
}

const cerrarModalReset = () => {
  showResetModal.value = false
}

const enviarReset = async () => {
  resetErrorMessage.value = ''
  resetMensajeOk.value = ''
  const correo = (resetEmail.value || '').trim()
  if (!correo) {
    resetErrorMessage.value = 'El correo es obligatorio.'
    return
  }

  isResetLoading.value = true
  try {
    await api.post('/usuarios/password-reset/solicitar', { email: correo })
    resetMensajeOk.value = 'Listo. Revisa tu correo para continuar.'
  } catch (e) {
    resetErrorMessage.value = e.response?.data?.detail || 'No se pudo enviar el enlace.'
  } finally {
    isResetLoading.value = false
  }
}
</script>
