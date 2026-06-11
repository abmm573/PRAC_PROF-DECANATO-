<template>
  <div class="min-h-screen flex items-center justify-center umsa-page px-4">
    <div class="max-w-md w-full umsa-card rounded-lg p-8">

      <div class="text-center mb-8">
        <h2 class="text-3xl font-bold text-gray-800">Recuperar contrasena</h2>
        <p class="text-gray-600 mt-2">Define una nueva contrasena</p>
      </div>

      <div v-if="mensajeOk" class="text-emerald-700 text-sm text-center bg-emerald-50 p-3 rounded border border-emerald-200 mb-4">
        {{ mensajeOk }}
      </div>

      <div v-if="errorMessage" class="text-red-600 text-sm text-center bg-red-50 p-3 rounded border border-red-200 mb-4">
        {{ errorMessage }}
      </div>

      <form v-if="!mensajeOk" @submit.prevent="confirmar" class="space-y-6">
        <div>
          <label class="block text-sm font-medium text-gray-700">Nueva contrasena</label>
          <input
            v-model="password1"
            type="password"
            required
            class="mt-1 appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm
                   placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            placeholder="Minimo 6 caracteres"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700">Confirmar contrasena</label>
          <input
            v-model="password2"
            type="password"
            required
            class="mt-1 appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm
                   placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            placeholder="Repite la contrasena"
          />
        </div>

        <button
          type="submit"
          :disabled="isLoading"
          class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm
                 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700
                 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500
                 disabled:opacity-50 transition-colors"
        >
          <span v-if="isLoading">Procesando...</span>
          <span v-else>Guardar contrasena</span>
        </button>

        <button type="button" @click="router.push('/login')"
          class="w-full flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm
                 text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 transition-colors">
          Volver al login
        </button>
      </form>

      <button v-else type="button" @click="router.push('/login')"
        class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm
               text-sm font-medium text-white bg-blue-600 hover:bg-blue-700
               focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors">
        Ir al login
      </button>

    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../services/api'

const route = useRoute()
const router = useRouter()

const token = computed(() => String(route.query.token || '').trim())

const password1 = ref('')
const password2 = ref('')
const isLoading = ref(false)
const errorMessage = ref('')
const mensajeOk = ref('')

const confirmar = async () => {
  errorMessage.value = ''
  mensajeOk.value = ''

  if (!token.value) {
    errorMessage.value = 'Token no encontrado. Revisa el enlace.'
    return
  }
  if (!password1.value || password1.value.length < 6) {
    errorMessage.value = 'La contrasena debe tener al menos 6 caracteres.'
    return
  }
  if (password1.value !== password2.value) {
    errorMessage.value = 'Las contrasenas no coinciden.'
    return
  }

  isLoading.value = true
  try {
    await api.post('/usuarios/password-reset/confirmar', {
      token: token.value,
      nueva_password: password1.value,
    })
    mensajeOk.value = 'Contrasena actualizada. Ya puedes iniciar sesion.'
  } catch (e) {
    errorMessage.value = e.response?.data?.detail || 'No se pudo actualizar la contrasena.'
  } finally {
    isLoading.value = false
  }
}
</script>

