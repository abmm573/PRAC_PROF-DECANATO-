<template>
  <div class="min-h-screen bg-slate-50 font-sans">
    <nav class="bg-slate-900 shadow-md">
      <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16 items-center">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-white/10 rounded-xl flex items-center justify-center border border-white/10">
              <span class="text-amber-400 font-extrabold text-xs tracking-wider">UMSA</span>
            </div>
            <div>
              <p class="text-white text-sm font-extrabold leading-tight">Perfil</p>
              <p class="text-[10px] text-slate-300 font-bold uppercase tracking-widest">{{ authStore.user?.rol }}</p>
            </div>
          </div>

          <div class="flex items-center gap-3">
            <button @click="volver"
              class="px-4 py-2 rounded-lg text-sm font-bold text-slate-200 hover:bg-white/10 hover:text-white transition-colors">
              Volver
            </button>
            <button @click="cerrarSesion"
              class="px-4 py-2 rounded-lg text-sm font-bold text-slate-200 hover:text-rose-300 hover:bg-white/10 transition-colors">
              Salir
            </button>
          </div>
        </div>
      </div>
    </nav>

    <main class="max-w-5xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      <div class="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 sm:p-8">
        <div class="flex items-start justify-between gap-6">
          <div>
            <h1 class="text-2xl font-black text-slate-800">Editar perfil</h1>
            <p class="mt-1 text-sm text-slate-500 font-medium">Actualiza tu informacion personal.</p>
          </div>
          <div class="w-11 h-11 bg-slate-100 rounded-full flex items-center justify-center text-slate-700 font-extrabold border border-slate-200">
            {{ iniciales }}
          </div>
        </div>

        <div v-if="isLoading" class="mt-6 text-slate-500 font-bold">
          Cargando...
        </div>

        <div v-else class="mt-6 space-y-6">
          <div v-if="mensajeOk" class="text-emerald-700 bg-emerald-50 border border-emerald-200 p-3 rounded-xl text-sm font-bold">
            {{ mensajeOk }}
          </div>
          <div v-if="errorMessage" class="text-rose-700 bg-rose-50 border border-rose-200 p-3 rounded-xl text-sm font-bold">
            {{ errorMessage }}
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
            <!-- Solo mostrar nombres y apellidos como lectura para pasantes y encargados -->
            <div v-if="authStore.user?.rol === 'ADMINISTRADOR'">
              <label class="block text-[11px] font-extrabold text-slate-500 uppercase tracking-widest mb-1.5 ml-1">Nombres</label>
              <input v-model="form.nombres" type="text" required
                class="w-full border border-slate-300 rounded-2xl p-3.5 focus:ring-2 focus:ring-blue-500 outline-none transition-all bg-slate-50 focus:bg-white font-semibold text-slate-800" />
            </div>
            <div v-else>
              <label class="block text-[11px] font-extrabold text-slate-500 uppercase tracking-widest mb-1.5 ml-1">Nombres (solo lectura)</label>
              <input :value="form.nombres" type="text" disabled
                class="w-full border border-slate-200 rounded-2xl p-3.5 bg-slate-100 text-slate-500 cursor-not-allowed font-bold" />
            </div>
            
            <div v-if="authStore.user?.rol === 'ADMINISTRADOR'">
              <label class="block text-[11px] font-extrabold text-slate-500 uppercase tracking-widest mb-1.5 ml-1">Apellidos</label>
              <input v-model="form.apellidos" type="text" required
                class="w-full border border-slate-300 rounded-2xl p-3.5 focus:ring-2 focus:ring-blue-500 outline-none transition-all bg-slate-50 focus:bg-white font-semibold text-slate-800" />
            </div>
            <div v-else>
              <label class="block text-[11px] font-extrabold text-slate-500 uppercase tracking-widest mb-1.5 ml-1">Apellidos (solo lectura)</label>
              <input :value="form.apellidos" type="text" disabled
                class="w-full border border-slate-200 rounded-2xl p-3.5 bg-slate-100 text-slate-500 cursor-not-allowed font-bold" />
            </div>
            
            <!-- Celular editable para pasantes y encargados -->
            <div>
              <label class="block text-[11px] font-extrabold text-slate-500 uppercase tracking-widest mb-1.5 ml-1">Celular</label>
              <input v-model="form.celular" type="tel" required
                class="w-full border border-slate-300 rounded-2xl p-3.5 focus:ring-2 focus:ring-blue-500 outline-none transition-all bg-slate-50 focus:bg-white font-semibold text-slate-800" />
            </div>
            
            <!-- RU solo editable por administrador -->
            <div v-if="authStore.user?.rol === 'ADMINISTRADOR'">
              <label class="block text-[11px] font-extrabold text-slate-500 uppercase tracking-widest mb-1.5 ml-1">RU</label>
              <input v-model="form.ru" type="text" placeholder="Opcional"
                class="w-full border border-slate-300 rounded-2xl p-3.5 focus:ring-2 focus:ring-blue-500 outline-none transition-all bg-slate-50 focus:bg-white font-semibold text-slate-800 placeholder:font-normal" />
            </div>
            <div v-else-if="authStore.user?.rol === 'PASANTE'">
              <label class="block text-[11px] font-extrabold text-slate-500 uppercase tracking-widest mb-1.5 ml-1">RU (solo lectura)</label>
              <input :value="form.ru" type="text" disabled
                class="w-full border border-slate-200 rounded-2xl p-3.5 bg-slate-100 text-slate-500 cursor-not-allowed font-bold" />
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
            <div>
              <label class="block text-[11px] font-extrabold text-slate-500 uppercase tracking-widest mb-1.5 ml-1">Email (solo lectura)</label>
              <input :value="perfil.email" type="text" disabled
                class="w-full border border-slate-200 rounded-2xl p-3.5 bg-slate-100 text-slate-500 cursor-not-allowed font-bold" />
            </div>
            <div>
              <label class="block text-[11px] font-extrabold text-slate-500 uppercase tracking-widest mb-1.5 ml-1">Username (solo lectura)</label>
              <input :value="perfil.username" type="text" disabled
                class="w-full border border-slate-200 rounded-2xl p-3.5 bg-slate-100 text-slate-500 cursor-not-allowed font-bold" />
            </div>
          </div>

          <div class="border-t border-slate-200 pt-6">
            <h2 class="text-sm font-black text-slate-800 uppercase tracking-widest">Cambiar contrasena</h2>
            <p class="text-xs text-slate-500 font-medium mt-1">Opcional. Si no quieres cambiarla, deja vacio.</p>

            <div class="mt-4 grid grid-cols-1 md:grid-cols-2 gap-5">
              <div>
                <label class="block text-[11px] font-extrabold text-slate-500 uppercase tracking-widest mb-1.5 ml-1">Password actual</label>
                <input v-model="form.password_actual" type="password" placeholder="Opcional"
                  class="w-full border border-slate-300 rounded-2xl p-3.5 focus:ring-2 focus:ring-blue-500 outline-none transition-all bg-slate-50 focus:bg-white font-semibold text-slate-800 placeholder:font-normal" />
              </div>
              <div>
                <label class="block text-[11px] font-extrabold text-slate-500 uppercase tracking-widest mb-1.5 ml-1">Nueva password</label>
                <input v-model="form.nueva_password" type="password" placeholder="Minimo 6 caracteres"
                  class="w-full border border-slate-300 rounded-2xl p-3.5 focus:ring-2 focus:ring-blue-500 outline-none transition-all bg-slate-50 focus:bg-white font-semibold text-slate-800 placeholder:font-normal" />
              </div>
            </div>
          </div>

          <div class="flex justify-end gap-3 pt-2">
            <button type="button" @click="volver"
              class="px-6 py-3 border border-slate-300 rounded-xl text-slate-600 font-bold hover:bg-slate-50 transition-colors">
              Cancelar
            </button>
            <button type="button" @click="guardar" :disabled="isSaving"
              class="px-8 py-3 bg-blue-900 text-white rounded-xl font-bold hover:bg-blue-800 disabled:opacity-50 transition-all shadow-lg flex items-center gap-2">
              <span v-if="isSaving" class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
              Guardar cambios
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

const router = useRouter()
const authStore = useAuthStore()

const isLoading = ref(true)
const isSaving = ref(false)
const errorMessage = ref('')
const mensajeOk = ref('')

const perfil = ref({ email: '', username: '' })
const form = ref({
  nombres: '',
  apellidos: '',
  celular: '',
  ru: '',
  password_actual: '',
  nueva_password: '',
})

const iniciales = computed(() => {
  const n = (authStore.user?.nombres || '').trim()
  const a = (authStore.user?.apellidos || '').trim()
  const n1 = n ? n.charAt(0) : ''
  const a1 = a ? a.charAt(0) : ''
  return (n1 + a1).toUpperCase() || 'U'
})

const volver = () => {
  router.push(authStore.rutaInicio())
}

const cerrarSesion = () => {
  authStore.logout()
  router.push('/login')
}

const cargar = async () => {
  isLoading.value = true
  errorMessage.value = ''
  try {
    const res = await api.get('/usuarios/me')
    const u = res.data || {}
    perfil.value = { email: u.email || '', username: u.username || '' }
    form.value.nombres = u.nombres || ''
    form.value.apellidos = u.apellidos || ''
    form.value.celular = u.celular || ''
    form.value.ru = u.ru || ''
  } catch (e) {
    errorMessage.value = e.response?.data?.detail || 'No se pudo cargar tu perfil.'
  } finally {
    isLoading.value = false
  }
}

const guardar = async () => {
  mensajeOk.value = ''
  errorMessage.value = ''
  isSaving.value = true
  try {
    const payload = {}
    
    // Solo administrador puede editar nombres, apellidos y RU
    if (authStore.user?.rol === 'ADMINISTRADOR') {
      payload.nombres = (form.value.nombres || '').trim()
      payload.apellidos = (form.value.apellidos || '').trim()
      payload.ru = (form.value.ru || '').trim() || null
    }
    
    // Pasantes y encargados pueden editar celular
    payload.celular = (form.value.celular || '').trim()
    
    // Todos pueden cambiar contraseña
    if (form.value.password_actual || form.value.nueva_password) {
      payload.password_actual = form.value.password_actual
      payload.nueva_password = form.value.nueva_password
    }
    
    const res = await api.put('/usuarios/mi-perfil', payload)
    if (res?.data) {
      authStore.user = res.data
      localStorage.setItem('user', JSON.stringify(res.data))
    }
    form.value.password_actual = ''
    form.value.nueva_password = ''
    mensajeOk.value = 'Perfil actualizado.'
  } catch (e) {
    errorMessage.value = e.response?.data?.detail || 'No se pudo guardar.'
  } finally {
    isSaving.value = false
  }
}

onMounted(async () => {
  await cargar()
})
</script>
