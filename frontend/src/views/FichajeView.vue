<template>
  <div class="min-h-screen umsa-page flex flex-col">

    <!-- Barra superior -->
    <header class="flex items-center justify-between px-8 py-4 relative z-10">
      <span class="text-white/90 font-semibold text-sm tracking-wide">
        Facultad de Ciencias Sociales - UMSA
      </span>
      <span class="text-white/70 font-medium text-xs tracking-wide ml-2">
        Sistema de Control de Asistencia de Pasantes
      </span>
      <button
        @click="$router.push('/login')"
        class="flex items-center gap-2 text-sm text-slate-900 border border-white/30 bg-white/90 px-4 py-2 rounded-lg hover:bg-white transition shadow-sm"
      >
        Iniciar sesión
        <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/>
        </svg>
      </button>
    </header>

    <main class="flex-1 flex items-center justify-center px-4 relative z-10">

      <transition name="slide-fade" mode="out-in">

        <!-- ══════════════════════════════════════════════════════
             PANTALLA 1: FICHAJE (entrada / salida)
        ══════════════════════════════════════════════════════ -->
        <div v-if="pantalla === 'fichaje'" key="fichaje"
          class="umsa-card rounded-3xl w-full max-w-md px-8 py-10 text-center">

          <!-- Reloj -->
          <div class="text-6xl font-black text-gray-900 tracking-tight leading-none">
            {{ horaActual }}
          </div>
          <div class="text-sm text-gray-400 mt-2 capitalize">{{ fechaActual }}</div>

          <hr class="my-6 border-gray-100" />

          <!-- Tabs -->
          <div class="flex rounded-xl overflow-hidden border border-gray-200 mb-6">
            <button
              @click="cambiarModo('entrada')"
              :class="modo === 'entrada' ? 'bg-blue-900 text-white' : 'bg-white text-gray-500 hover:bg-gray-50'"
              class="flex-1 flex items-center justify-center gap-2 py-3 text-sm font-semibold transition"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a2 2 0 01-2 2H6a2 2 0 01-2-2V7a2 2 0 012-2h7a2 2 0 012 2v1"/>
              </svg>
              Entrada
            </button>
            <button
              @click="cambiarModo('salida')"
              :class="modo === 'salida' ? 'bg-red-700 text-white' : 'bg-white text-gray-500 hover:bg-gray-50'"
              class="flex-1 flex items-center justify-center gap-2 py-3 text-sm font-semibold transition"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a2 2 0 01-2 2H6a2 2 0 01-2-2V7a2 2 0 012-2h5a2 2 0 012 2v1"/>
              </svg>
              Salida
            </button>
          </div>

          <!-- Input username -->
          <label for="username-input" class="block text-left text-xs font-bold text-gray-500 uppercase tracking-widest mb-2">
            Ingresa tu username
          </label>
          <div class="relative">
            <svg xmlns="http://www.w3.org/2000/svg"
              class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400"
              fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
            </svg>
            <input
              v-model="username"
              ref="inputRef"
              id="username-input"
              name="username"
              type="text"
              placeholder="Ej. jp1234567"
              autocomplete="username"
              @keyup.enter="fichar"
              class="w-full pl-10 pr-4 py-3 border-2 border-gray-200 rounded-xl text-sm
                     focus:outline-none focus:border-blue-400 transition"
            />
          </div>

          <!-- Mensaje de error / aviso -->
          <transition name="fade">
            <div v-if="mensajeFichaje" :class="[
                esFichajeError
                  ? 'bg-red-50 border-red-200 text-red-700'
                  : 'bg-green-50 border-green-200 text-green-700',
                'mt-4 p-3 rounded-xl border text-sm text-left'
              ]">
              <p class="font-bold">{{ mensajeFichaje.titulo }}</p>
              <p v-if="mensajeFichaje.detalle" class="text-xs opacity-75 mt-0.5">{{ mensajeFichaje.detalle }}</p>
            </div>
          </transition>

          <!-- Botón fichar -->
          <button
            @click="fichar"
            :disabled="isLoading || !username.trim()"
            :class="modo === 'entrada'
              ? 'bg-blue-900 hover:bg-blue-800 disabled:bg-blue-700/50'
              : 'bg-red-700 hover:bg-red-800 disabled:bg-red-500/50'"
            class="w-full mt-5 py-3.5 rounded-xl text-white font-bold text-sm
                   transition disabled:cursor-not-allowed shadow-md"
          >
            <span v-if="isLoading" class="flex items-center justify-center gap-2">
              <svg class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
              </svg>
              Procesando...
            </span>
            <span v-else>
              {{ modo === 'entrada' ? 'Registrar Entrada' : 'Registrar Salida' }}
            </span>
          </button>

        </div>

        <!-- ══════════════════════════════════════════════════════
             PANTALLA 2: RESUMEN DE SALIDA
        ══════════════════════════════════════════════════════ -->
        <div v-else-if="pantalla === 'reporte'" key="reporte"
          class="w-full max-w-md">
          <div class="bg-white rounded-3xl shadow-xl overflow-hidden">

            <!-- Franja superior con resumen -->
            <div class="bg-gradient-to-r from-slate-700 to-slate-800 px-7 py-6">
              <div class="flex items-center gap-4">
                <div class="w-11 h-11 bg-white/15 rounded-2xl flex items-center justify-center flex-shrink-0">
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                </div>
                <div>
                  <p class="text-white font-bold text-base leading-tight">¡Salida registrada!</p>
                  <p class="text-slate-300 text-sm">Hola, <span class="font-semibold text-white">{{ datosJornada.nombre }}</span></p>
                </div>
              </div>
              <div class="grid grid-cols-3 gap-2 mt-5">
                <div class="bg-white/10 rounded-xl p-3 text-center">
                  <p class="text-xs text-slate-300 font-medium uppercase tracking-wide mb-0.5">Entrada</p>
                  <p class="text-sm font-bold text-white">{{ datosJornada.hora_entrada }}</p>
                </div>
                <div class="bg-white/10 rounded-xl p-3 text-center">
                  <p class="text-xs text-slate-300 font-medium uppercase tracking-wide mb-0.5">Salida</p>
                  <p class="text-sm font-bold text-white">{{ datosJornada.hora_salida }}</p>
                </div>
                <div class="bg-emerald-500/30 rounded-xl p-3 text-center border border-emerald-400/30">
                  <p class="text-xs text-emerald-200 font-medium uppercase tracking-wide mb-0.5">Total</p>
                  <p class="text-sm font-bold text-emerald-100">{{ formatHorasTrabajadas(datosJornada.horas_trabajadas) }}</p>
                </div>
              </div>
            </div>

            <!-- Cuerpo -->
            <div class="px-7 py-6">
              <p class="text-sm text-slate-600 font-semibold">
                Salida registrada correctamente.
              </p>
              <p class="text-xs text-slate-400 mt-2">
                Esta ventana se cerrará automáticamente en <strong>{{ cuentaRegresiva }}</strong>s.
              </p>
              <button
                @click="volverAlFichaje"
                class="w-full mt-4 py-3.5 rounded-xl bg-slate-800 text-white font-bold text-sm hover:bg-slate-700 transition shadow-sm"
              >
                Volver al inicio
              </button>
            </div>

          </div>
        </div>

      </transition>
    </main>

    <!-- Decoración fondo -->
    <div class="fixed top-0 right-0 w-72 h-72 bg-blue-100 rounded-full opacity-40
                -translate-y-1/3 translate-x-1/3 pointer-events-none -z-10"></div>
    <div class="fixed bottom-0 left-0 w-56 h-56 bg-indigo-100 rounded-full opacity-30
                translate-y-1/3 -translate-x-1/3 pointer-events-none -z-10"></div>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { formatHora, formatFecha, formatHorasTrabajadas } from '../utils/formatters'
import api from '../services/api'

// ── Pantallas: 'fichaje' | 'reporte' ─────────────────────────────────────────
const pantalla = ref('fichaje')

// ── Fichaje ───────────────────────────────────────────────────────────────────
const modo           = ref('entrada')
const username       = ref('')
const isLoading      = ref(false)
const mensajeFichaje = ref(null)
const esFichajeError = ref(false)
const inputRef       = ref(null)

// Datos que se guardan tras la salida exitosa
const datosJornada = ref({
  nombre:           '',
  hora_entrada:     '',
  hora_salida:      '',
  horas_trabajadas: 0,
  asistencia_id:    null,
})

// ── Cuenta regresiva ──────────────────────────────────────────────────────────
const cuentaRegresiva = ref(8)
let timerConfirmacion = null

// ── Reloj ─────────────────────────────────────────────────────────────────────
const horaActual  = ref('')
const fechaActual = ref('')
let intervalo = null

const actualizarReloj = () => {
  const ahora = new Date()
  horaActual.value = ahora.toLocaleTimeString('es-BO', {
    hour: '2-digit', minute: '2-digit', second: '2-digit'
  })
  fechaActual.value = ahora.toLocaleDateString('es-BO', {
    weekday: 'long', day: 'numeric', month: 'long', year: 'numeric'
  })
}

onMounted(() => {
  actualizarReloj()
  intervalo = setInterval(actualizarReloj, 1000)
})

onUnmounted(() => {
  clearInterval(intervalo)
  if (timerConfirmacion) clearInterval(timerConfirmacion)
})

// ── Helpers ───────────────────────────────────────────────────────────────────
const cambiarModo = (nuevoModo) => {
  modo.value           = nuevoModo
  mensajeFichaje.value = null
  username.value       = ''
  nextTick(() => inputRef.value?.focus())
}

let timeoutMensaje = null
const mostrarError = (titulo, detalle) => {
  esFichajeError.value = true
  mensajeFichaje.value = { titulo, detalle }
  if (timeoutMensaje) clearTimeout(timeoutMensaje)
  timeoutMensaje = setTimeout(() => { mensajeFichaje.value = null }, 5000)
}

// ── Lógica de fichaje ─────────────────────────────────────────────────────────
const fichar = async () => {
  if (!username.value.trim() || isLoading.value) return

  isLoading.value      = true
  mensajeFichaje.value = null

  try {
    const endpoint = modo.value === 'entrada'
      ? '/asistencias/publico/entrada'
      : '/asistencias/publico/salida'

    const { data } = await api.post(endpoint, { username: username.value.trim() })

    if (modo.value === 'entrada') {
      // Entrada exitosa → mensaje verde y limpiar
      esFichajeError.value = false
      mensajeFichaje.value = {
        titulo:  '✅ Entrada registrada',
        detalle: `Entrada registrada a las ${data.hora_entrada}`,
      }
      username.value = ''
      if (timeoutMensaje) clearTimeout(timeoutMensaje)
      timeoutMensaje = setTimeout(() => { mensajeFichaje.value = null }, 6000)

    } else {
      // Salida exitosa → guardar datos y pasar a pantalla de resumen
      datosJornada.value = {
        nombre:           data.nombre,
        hora_entrada:     data.hora_entrada,
        hora_salida:      data.hora_salida,
        horas_trabajadas: data.horas_trabajadas,
        asistencia_id:    data.asistencia_id,
      }
      username.value = ''
      pantalla.value = 'reporte'
      iniciarCuentaRegresiva()
    }

  } catch (error) {
    const detalle  = error.response?.data?.detail || 'Error al conectar con el servidor.'
    const titulos  = {
      404: '❌ Usuario no encontrado',
      403: '🚫 Acceso no permitido',
      400: '⚠️ Aviso',
    }
    mostrarError(titulos[error.response?.status] ?? '❌ Error', detalle)
  } finally {
    isLoading.value = false
  }
}

// ── Cuenta regresiva y retorno ────────────────────────────────────────────────
const iniciarCuentaRegresiva = () => {
  cuentaRegresiva.value = 8
  timerConfirmacion = setInterval(() => {
    cuentaRegresiva.value--
    if (cuentaRegresiva.value <= 0) {
      clearInterval(timerConfirmacion)
      volverAlFichaje()
    }
  }, 1000)
}

const volverAlFichaje = () => {
  if (timerConfirmacion) clearInterval(timerConfirmacion)
  pantalla.value     = 'fichaje'
  modo.value         = 'entrada'
  datosJornada.value = { nombre: '', hora_entrada: '', hora_salida: '', horas_trabajadas: 0, asistencia_id: null }
  nextTick(() => inputRef.value?.focus())
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.25s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.slide-fade-enter-active { transition: all 0.35s ease; }
.slide-fade-leave-active { transition: all 0.25s ease; }
.slide-fade-enter-from { opacity: 0; transform: translateY(16px); }
.slide-fade-leave-to   { opacity: 0; transform: translateY(-10px); }
</style>