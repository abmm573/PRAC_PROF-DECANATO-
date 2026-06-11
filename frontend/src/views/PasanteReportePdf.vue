<template>
  <div class="min-h-screen bg-slate-100 font-sans pb-12">

    <header class="bg-blue-950 border-b-4 border-red-700 sticky top-0 z-50 shadow-2xl">
      <div class="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-5 pointer-events-none"></div>
      <div class="max-w-[96rem] mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div class="flex justify-between h-16 items-center">
          <div class="flex items-center gap-4">
            <button @click="$router.go(-1)"
              class="inline-flex items-center gap-2 bg-white/10 hover:bg-white/20 px-4 py-2 rounded-lg text-white transition-colors font-semibold text-sm">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
              </svg>
              Volver
            </button>
            <div class="border-l-2 border-white/10 pl-4 py-1 hidden sm:block">
              <p class="text-[10px] text-red-400 font-black uppercase tracking-widest leading-none mb-1">Facultad de Cs. Sociales</p>
              <p class="text-sm font-extrabold text-white leading-none tracking-tight">
                Reporte PDF
                <span class="text-blue-300/50 font-medium ml-1">| Descarga tu reporte</span>
              </p>
            </div>
          </div>
          <div class="flex items-center gap-4">
            <div class="hidden sm:flex flex-col items-end">
              <span class="text-white text-sm font-bold leading-tight">{{ authStore.user?.nombres }}</span>
              <span class="text-[10px] font-black text-red-400 uppercase tracking-widest">{{ authStore.user?.rol }}</span>
            </div>
            <button @click="cerrarSesion" class="text-blue-300 hover:text-red-400 transition-colors" title="Cerrar Sesión">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </header>

    <main class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">

      <!-- CONFIGURACIÓN -->
      <div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        <div class="px-8 py-5 bg-gradient-to-r from-blue-950 to-blue-900 border-b-4 border-red-600">
          <h1 class="text-lg font-black text-white uppercase tracking-widest flex items-center gap-2">
            <svg class="w-5 h-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414A1 1 0 0119 9.414V19a2 2 0 01-2 2z"/>
            </svg>
            Configurar Reporte PDF
          </h1>
        </div>

        <div class="p-6">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">

            <!-- Tipo -->
            <div>
              <label class="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-2">Tipo de Reporte</label>
              <div class="flex rounded-xl overflow-hidden border border-slate-300">
                <button @click="tipoPdf = 'semanal'"
                  :class="tipoPdf === 'semanal' ? 'bg-blue-950 text-white' : 'bg-white text-slate-600 hover:bg-slate-50'"
                  class="px-4 py-3 text-sm font-bold transition-all flex-1">Semanal</button>
                <button @click="tipoPdf = 'mensual'"
                  :class="tipoPdf === 'mensual' ? 'bg-blue-950 text-white' : 'bg-white text-slate-600 hover:bg-slate-50'"
                  class="px-4 py-3 text-sm font-bold transition-all flex-1">Mensual</button>
              </div>
            </div>

            <!-- Filtro Semanal -->
            <div v-if="tipoPdf === 'semanal'">
              <label class="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-2">Seleccionar Semana</label>
              <input type="date" v-model="pdfFechaSemana"
                class="w-full border border-slate-300 rounded-xl px-3 py-3 text-sm outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all font-bold bg-slate-50 focus:bg-white"/>
              <div v-if="infoSemana" class="mt-2 bg-blue-50 border border-blue-200 rounded-xl p-3">
                <p class="text-sm text-blue-800 font-bold">{{ infoSemana }}</p>
              </div>
            </div>

            <!-- Filtro Mensual -->
            <div v-if="tipoPdf === 'mensual'">
              <label class="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-2">Mes y Año</label>
              <div class="grid grid-cols-2 gap-3">
                <select v-model="pdfMes"
                  class="w-full border border-slate-300 rounded-xl px-3 py-3 text-sm outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 font-bold bg-slate-50 focus:bg-white transition-all">
                  <option v-for="(nombre, idx) in mesesNombres" :key="idx + 1" :value="idx + 1">{{ nombre }}</option>
                </select>
                <select v-model="pdfAnio"
                  class="w-full border border-slate-300 rounded-xl px-3 py-3 text-sm outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 font-bold bg-slate-50 focus:bg-white transition-all">
                  <option v-for="y in aniosDisponibles" :key="y" :value="y">{{ y }}</option>
                </select>
              </div>
              <div v-if="pdfMes && pdfAnio" class="mt-2 bg-blue-50 border border-blue-200 rounded-xl p-3">
                <p class="text-sm text-blue-800 font-bold">{{ mesesNombres[pdfMes - 1] }} {{ pdfAnio }}</p>
              </div>
            </div>

            <!-- Botón buscar -->
            <div class="flex items-end">
              <button @click="cargarVistaPrevia" :disabled="cargando || !puedeCargar"
                class="w-full px-6 py-3 bg-gradient-to-r from-blue-800 to-blue-950 text-white rounded-xl text-sm font-black uppercase tracking-widest hover:from-blue-700 hover:to-blue-900 disabled:opacity-50 shadow-lg shadow-blue-900/30 transition-all flex items-center justify-center gap-2">
                <svg v-if="cargando" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
                </svg>
                <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                </svg>
                {{ cargando ? 'Buscando...' : 'Buscar' }}
              </button>
            </div>

          </div>

          <p v-if="avisoPasante" class="mt-4 text-amber-700 text-sm bg-amber-50 border border-amber-200 p-3 rounded-xl font-bold">{{ avisoPasante }}</p>
          <p v-if="errorVistaPrevia" class="mt-4 text-red-600 text-sm bg-red-50 border border-red-200 p-3 rounded-xl font-bold">{{ errorVistaPrevia }}</p>
          <p v-if="errorDescarga" class="mt-4 text-red-600 text-sm bg-red-50 border border-red-200 p-3 rounded-xl font-bold">{{ errorDescarga }}</p>
        </div>
      </div>

      <!-- TABLA RESULTADOS -->
      <div v-if="datosVistaPrevia.length > 0" class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        <div class="px-8 py-5 bg-gradient-to-r from-blue-950 to-blue-900 border-b-4 border-red-600">
          <h3 class="text-lg font-black text-white uppercase tracking-widest">
            Reporte {{ tipoPdf === 'semanal' ? 'Semanal' : 'Mensual' }}
          </h3>
          <p v-if="usuarioReporte && requierePasante" class="text-blue-200 text-xs mt-1">
            Pasante: {{ usuarioReporte?.nombres }} {{ usuarioReporte?.apellidos }}
          </p>
          <p class="text-blue-200 text-sm mt-1">
            <span v-if="tipoPdf === 'semanal'">{{ obtenerRangoFechasSemana() }}</span>
            <span v-else>{{ mesesNombres[pdfMes - 1] }} {{ pdfAnio }}</span>
          </p>
        </div>

        <div class="p-6">
          <div class="overflow-x-auto rounded-xl border border-slate-200">
            <table class="w-full text-sm border-collapse">
              <thead>
                <tr class="bg-slate-50 border-b-2 border-slate-200">
                  <th class="px-4 py-3 text-left text-[10px] font-black text-slate-500 uppercase tracking-widest whitespace-nowrap">Fecha</th>
                  <th class="px-4 py-3 text-left text-[10px] font-black text-slate-500 uppercase tracking-widest whitespace-nowrap">Entrada</th>
                  <th class="px-4 py-3 text-left text-[10px] font-black text-slate-500 uppercase tracking-widest whitespace-nowrap">Salida</th>
                  <th class="px-4 py-3 text-left text-[10px] font-black text-slate-500 uppercase tracking-widest whitespace-nowrap">Horas</th>
                  <th class="px-4 py-3 text-left text-[10px] font-black text-blue-700 uppercase tracking-widest whitespace-nowrap">Est. Encargado</th>
                  <th class="px-4 py-3 text-left text-[10px] font-black text-emerald-700 uppercase tracking-widest whitespace-nowrap">Est. Admin</th>
                  <th class="px-4 py-3 text-left text-[10px] font-black text-slate-500 uppercase tracking-widest">Actividades</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, index) in datosVistaPrevia" :key="index"
                  :class="index % 2 === 0 ? 'bg-white' : 'bg-slate-50/50'"
                  class="border-b border-slate-100 hover:bg-blue-50/30 transition-colors">
                  <td class="px-4 py-3 text-slate-800 font-bold whitespace-nowrap">{{ row.fecha }}</td>
                  <td class="px-4 py-3 text-slate-700 font-mono whitespace-nowrap">{{ row.entrada }}</td>
                  <td class="px-4 py-3 text-slate-700 font-mono whitespace-nowrap">{{ row.salida }}</td>
                  <td class="px-4 py-3 text-slate-800 font-black whitespace-nowrap">{{ row.horas }}</td>
                  <td class="px-4 py-3 whitespace-nowrap">
                    <span :class="badgeEstado(row.estado_encargado)" class="px-2.5 py-1 rounded-full text-[10px] font-black uppercase tracking-widest">
                      {{ row.estado_encargado }}
                    </span>
                  </td>
                  <td class="px-4 py-3 whitespace-nowrap">
                    <span :class="badgeEstado(row.estado_admin)" class="px-2.5 py-1 rounded-full text-[10px] font-black uppercase tracking-widest">
                      {{ row.estado_admin }}
                    </span>
                  </td>
                  <td class="px-4 py-3 text-slate-600 max-w-xs truncate" :title="row.comentario">{{ row.comentario || '—' }}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Resumen -->
          <div class="mt-6 bg-slate-50 border border-slate-200 rounded-2xl p-5">
            <h4 class="font-black text-blue-950 mb-4 uppercase tracking-widest text-sm">Resumen del Período</h4>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              <div class="bg-white rounded-xl p-4 border border-slate-200 text-center shadow-sm">
                <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Total Días</p>
                <p class="text-2xl font-black text-blue-950">{{ datosVistaPrevia.length }}</p>
              </div>
              <div class="bg-white rounded-xl p-4 border border-slate-200 text-center shadow-sm">
                <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Total Horas</p>
                <p class="text-2xl font-black text-blue-950">{{ totalHorasVistaPrevia }}h</p>
              </div>
              <div class="bg-white rounded-xl p-4 border border-emerald-200 text-center shadow-sm">
                <p class="text-[10px] font-black text-emerald-600 uppercase tracking-widest mb-1">Aprobados</p>
                <p class="text-2xl font-black text-emerald-700">{{ contadorEstados['APROBADO'] || 0 }}</p>
              </div>
              <div class="bg-white rounded-xl p-4 border border-amber-200 text-center shadow-sm">
                <p class="text-[10px] font-black text-amber-600 uppercase tracking-widest mb-1">Pendientes</p>
                <p class="text-2xl font-black text-amber-700">{{ contadorEstados['PENDIENTE'] || 0 }}</p>
              </div>
            </div>

            <div class="flex justify-center">
              <button @click="generarPdfDesdeVistaPrevia" :disabled="descargando || !puedeGenerarPdf"
                class="inline-flex items-center gap-2 bg-gradient-to-r from-blue-800 to-blue-950 hover:from-blue-700 hover:to-blue-900 text-white px-8 py-3 rounded-xl text-sm font-black uppercase tracking-widest transition-all disabled:opacity-50 shadow-lg shadow-blue-900/30">
                <svg v-if="descargando" class="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
                </svg>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414A1 1 0 0119 9.414V19a2 2 0 01-2 2z"/>
                </svg>
                {{ descargando ? 'Generando PDF...' : 'Generar PDF' }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Sin datos -->
      <div v-else-if="busquedaRealizada && !cargando" class="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">
        <div class="p-12 text-center">
          <div class="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-4 border border-slate-200">
            <svg class="w-8 h-8 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414A1 1 0 0119 9.414V19a2 2 0 01-2 2z"/>
            </svg>
          </div>
          <p class="text-slate-600 font-bold">No hay asistencias para este período</p>
          <p class="text-slate-400 text-sm mt-1">Selecciona otro período o registra tus asistencias primero</p>
        </div>
      </div>

    </main>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

const route     = useRoute()
const router    = useRouter()
const authStore = useAuthStore()

const rol = computed(() => authStore.user?.rol)
const requierePasante = computed(() => rol.value === 'ADMINISTRADOR' || rol.value === 'ENCARGADO')

const pasanteId = computed(() => {
  if (!requierePasante.value) return authStore.user?.id ?? null
  const q = route.query?.pasante_id ?? route.query?.pasanteId ?? route.query?.id
  const n = q != null && q !== '' ? Number(q) : null
  return Number.isFinite(n) ? n : null
})

// ---- ESTADO ----
const tipoPdf               = ref('semanal')
const pdfFechaSemana        = ref('')
const pdfMes                = ref(new Date().getMonth() + 1)
const pdfAnio               = ref(new Date().getFullYear())
const datosVistaPrevia      = ref([])
const totalHorasVistaPrevia = ref(0)
const contadorEstados       = ref({})
const descargando           = ref(false)
const cargando              = ref(false)
const busquedaRealizada     = ref(false)
const errorDescarga         = ref('')
const errorVistaPrevia      = ref('')
const usuarioReporte        = ref(null)

// ---- Cuando cambia el tipo, limpiar resultados anteriores ----
watch(tipoPdf, () => {
  datosVistaPrevia.value = []
  busquedaRealizada.value = false
  errorVistaPrevia.value = ''
  pdfFechaSemana.value = ''
})

// ---- Cargar usuario del pasante si es admin/encargado ----
watch([pasanteId, requierePasante], async () => {
  errorVistaPrevia.value = ''
  usuarioReporte.value = null
  if (!requierePasante.value) { usuarioReporte.value = authStore.user ?? null; return }
  if (!pasanteId.value) return
  try {
    const { data } = await api.get('/usuarios/listar', { timeout: 30000 })
    const found = (data || []).find(u => String(u.id) === String(pasanteId.value))
    usuarioReporte.value = found || null
    if (!found) errorVistaPrevia.value = 'No se encontró el pasante con ese ID.'
  } catch (e) {
    errorVistaPrevia.value = e.response?.data?.detail || 'No se pudo cargar los datos del pasante.'
  }
}, { immediate: true })

// ---- Computed ----
const puedeCargar = computed(() => {
  if (tipoPdf.value === 'semanal') return !!pdfFechaSemana.value
  return !!(pdfMes.value && pdfAnio.value)
})

const puedeGenerarPdf = computed(() => {
  if (descargando.value) return false
  if (requierePasante.value) return !!usuarioReporte.value
  return true
})

const avisoPasante = computed(() => {
  if (!requierePasante.value) return ''
  if (pasanteId.value) return ''
  return 'Para ver el reporte como encargado o admin, abre esta vista con ?pasante_id=ID'
})

const infoSemana = computed(() => {
  if (!pdfFechaSemana.value) return ''
  const d = new Date(pdfFechaSemana.value + 'T12:00:00')
  const diaSem = (d.getDay() + 6) % 7
  const lunes = new Date(d); lunes.setDate(d.getDate() - diaSem)
  const viernes = new Date(lunes); viernes.setDate(lunes.getDate() + 4)
  return `Semana del ${lunes.toLocaleDateString('es-BO', { day: '2-digit', month: '2-digit', year: 'numeric' })} al ${viernes.toLocaleDateString('es-BO', { day: '2-digit', month: '2-digit', year: 'numeric' })}`
})

const mesesNombres = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
const aniosDisponibles = computed(() => { const a = new Date().getFullYear(); return Array.from({ length: 5 }, (_, i) => a - 2 + i) })

const badgeEstado = (estado) => {
  switch (estado?.toUpperCase()) {
    case 'VERIFICADO': case 'APROBADO': return 'bg-emerald-100 text-emerald-800'
    case 'RECHAZADO': return 'bg-red-100 text-red-800'
    case 'PENDIENTE': return 'bg-amber-100 text-amber-800'
    default: return 'bg-slate-100 text-slate-600'
  }
}

const obtenerRangoFechasSemana = () => {
  if (!pdfFechaSemana.value) return ''
  const d = new Date(pdfFechaSemana.value + 'T12:00:00')
  const diaSem = (d.getDay() + 6) % 7
  const lunes = new Date(d); lunes.setDate(d.getDate() - diaSem)
  const viernes = new Date(lunes); viernes.setDate(lunes.getDate() + 4)
  return `${lunes.toLocaleDateString('es-BO', { day: '2-digit', month: '2-digit' })} — ${viernes.toLocaleDateString('es-BO', { day: '2-digit', month: '2-digit', year: 'numeric' })}`
}

// ---- CARGAR DATOS — solo al hacer clic en Buscar ----
const cargarVistaPrevia = async () => {
  if (!puedeCargar.value) return
  cargando.value = true
  busquedaRealizada.value = false
  datosVistaPrevia.value = []
  totalHorasVistaPrevia.value = 0
  contadorEstados.value = {}
  errorVistaPrevia.value = ''

  try {
    const params = {}
    if (tipoPdf.value === 'semanal') {
      const d = new Date(pdfFechaSemana.value + 'T12:00:00')
      const diaSem = (d.getDay() + 6) % 7
      const lunes = new Date(d); lunes.setDate(d.getDate() - diaSem)
      params.semana = isoSemana(lunes)
      params.anio = lunes.getFullYear()
    } else {
      params.mes = pdfMes.value
      params.anio = pdfAnio.value
    }
    if (requierePasante.value && pasanteId.value) params.pasante_id = pasanteId.value

    const { data: asistencias } = await api.get('/asistencias/mis-asistencias', { params })

    datosVistaPrevia.value = asistencias.map(asist => ({
      fecha:            new Date(asist.fecha).toLocaleDateString('es-BO', { day: '2-digit', month: '2-digit', year: 'numeric' }),
      entrada:          asist.hora_entrada ? new Date(asist.hora_entrada).toLocaleTimeString('es-BO', { hour: '2-digit', minute: '2-digit' }) : '—',
      salida:           asist.hora_salida  ? new Date(asist.hora_salida).toLocaleTimeString('es-BO', { hour: '2-digit', minute: '2-digit' }) : '—',
      horas:            asist.horas_trabajadas ? `${asist.horas_trabajadas}h` : '—',
      estado_encargado: asist.reporte?.estado_encargado ?? (asist.reporte ? 'PENDIENTE' : 'SIN REGISTRO'),
      estado_admin:     asist.reporte?.estado_admin     ?? (asist.reporte ? 'PENDIENTE' : 'SIN REGISTRO'),
      comentario:       asist.reporte?.actividades_realizadas || '',
    }))

    totalHorasVistaPrevia.value = Math.round(asistencias.reduce((acc, a) => acc + (parseFloat(a.horas_trabajadas) || 0), 0) * 10) / 10

    contadorEstados.value = asistencias.reduce((cnt, a) => {
      const e = a.reporte?.estado_admin ?? (a.reporte ? 'PENDIENTE' : 'SIN REGISTRO')
      cnt[e] = (cnt[e] || 0) + 1
      return cnt
    }, {})

  } catch (err) {
    errorVistaPrevia.value = err.response?.data?.detail || 'Error al cargar asistencias.'
  } finally {
    cargando.value = false
    busquedaRealizada.value = true
  }
}

// ---- GENERAR PDF ----
const generarPdfDesdeVistaPrevia = async () => {
  descargando.value = true
  errorDescarga.value = ''
  try {
    const u = usuarioReporte.value || authStore.user || {}
    const script = document.createElement('script')
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js'
    document.head.appendChild(script)
    await new Promise(resolve => { script.onload = resolve })

    const { jsPDF } = window.jspdf
    const doc = new jsPDF()
    const pageWidth = doc.internal.pageSize.getWidth()
    const pageHeight = doc.internal.pageSize.getHeight()
    const margin = 15
    let yPosition = 25

    doc.setFillColor(30, 58, 138)
    doc.rect(margin, yPosition - 8, pageWidth - 2 * margin, 30, 'F')
    doc.setTextColor(255, 255, 255)
    doc.setFontSize(16); doc.setFont(undefined, 'bold')
    doc.text(`REPORTE ${tipoPdf.value === 'semanal' ? 'SEMANAL' : 'MENSUAL'}`, pageWidth / 2, yPosition + 2, { align: 'center' })
    doc.setFontSize(10); doc.setFont(undefined, 'normal')
    const periodo = tipoPdf.value === 'semanal' ? obtenerRangoFechasSemana() : `${mesesNombres[pdfMes.value - 1]} ${pdfAnio.value}`
    doc.text(`Período: ${periodo}`, pageWidth / 2, yPosition + 10, { align: 'center' })
    doc.setFontSize(7); doc.setFont(undefined, 'italic')
    doc.text(`Generado: ${new Date().toLocaleDateString('es-BO')} ${new Date().toLocaleTimeString('es-BO', { hour: '2-digit', minute: '2-digit' })}`, pageWidth / 2, yPosition + 17, { align: 'center' })
    doc.setTextColor(0, 0, 0)
    yPosition += 35

    doc.setFillColor(240, 248, 255)
    doc.rect(margin, yPosition - 6, pageWidth - 2 * margin, 35, 'F')
    doc.setDrawColor(30, 58, 138)
    doc.rect(margin, yPosition - 6, pageWidth - 2 * margin, 35)
    doc.setTextColor(30, 58, 138); doc.setFontSize(12); doc.setFont(undefined, 'bold')
    doc.text('DATOS DEL USUARIO - FACULTAD DE CIENCIAS SOCIALES - UMSA', margin + 8, yPosition + 3)
    doc.setLineWidth(0.5); doc.line(margin + 8, yPosition + 8, pageWidth - margin - 8, yPosition + 8)
    doc.setTextColor(55, 65, 81); doc.setFontSize(9); doc.setFont(undefined, 'normal')
    doc.text(`Nombre Completo: ${u?.nombres || ''} ${u?.apellidos || ''}`, margin + 10, yPosition + 15)
    doc.text(`C.I.: ${u?.carnet_identidad || '—'}`, margin + 95, yPosition + 15)
    doc.text(`R.U.: ${u?.ru || '—'}`, margin + 10, yPosition + 21)
    doc.text(`Unidad Asignada: ${u?.unidad_asignada || '—'}`, margin + 95, yPosition + 21)
    doc.text(`Carrera: ${u?.carrera_nombre || u?.carrera?.nombre || '—'}`, margin + 10, yPosition + 27)
    doc.text(`Usuario: ${u?.username || '—'}`, margin + 95, yPosition + 27)
    yPosition += 40

    doc.setTextColor(30, 58, 138); doc.setFontSize(12); doc.setFont(undefined, 'bold')
    doc.text('REGISTRO DE ASISTENCIAS', margin, yPosition)
    yPosition += 8

    const headers = ['Fecha', 'Entrada', 'Salida', 'Horas', 'Est. Encargado', 'Est. Admin', 'Actividades']
    const colWidths = [22, 20, 20, 15, 28, 25, 55]
    doc.setFillColor(30, 58, 138)
    doc.rect(margin, yPosition - 3, pageWidth - 2 * margin, 6, 'F')
    doc.setTextColor(255, 255, 255); doc.setFontSize(7); doc.setFont(undefined, 'bold')
    headers.forEach((h, i) => {
      doc.text(h, margin + colWidths.slice(0, i).reduce((a, b) => a + b, 0) + 2, yPosition + 1)
    })
    yPosition += 5

    datosVistaPrevia.value.slice(0, 10).forEach((row, index) => {
      if (index % 2 === 0) { doc.setFillColor(248, 250, 252); doc.rect(margin, yPosition - 2, pageWidth - 2 * margin, 5, 'F') }
      const rowData = [row.fecha, row.entrada, row.salida, row.horas, row.estado_encargado || '—', row.estado_admin || '—', (row.comentario || '').substring(0, 30) + ((row.comentario || '').length > 30 ? '...' : '')]
      let xPos = margin
      rowData.forEach((data, colIndex) => {
        if (colIndex === 4) { const e = String(data || '').toUpperCase(); doc.setTextColor(e === 'VERIFICADO' ? 34 : e === 'RECHAZADO' ? 239 : e === 'PENDIENTE' ? 245 : 107, e === 'VERIFICADO' ? 197 : e === 'RECHAZADO' ? 68 : e === 'PENDIENTE' ? 158 : 114, e === 'VERIFICADO' ? 94 : e === 'RECHAZADO' ? 68 : e === 'PENDIENTE' ? 11 : 128) }
        else if (colIndex === 5) { const e = String(data || '').toUpperCase(); doc.setTextColor(e === 'APROBADO' ? 34 : e === 'RECHAZADO' ? 239 : e === 'PENDIENTE' ? 245 : 107, e === 'APROBADO' ? 197 : e === 'RECHAZADO' ? 68 : e === 'PENDIENTE' ? 158 : 114, e === 'APROBADO' ? 94 : e === 'RECHAZADO' ? 68 : e === 'PENDIENTE' ? 11 : 128) }
        else doc.setTextColor(55, 65, 81)
        doc.text(data || '—', xPos, yPosition + 3); xPos += colWidths[colIndex]
      })
      yPosition += 5
    })

    yPosition += 8
    doc.setFillColor(30, 58, 138); doc.rect(margin, yPosition - 3, pageWidth - 2 * margin, 6, 'F')
    doc.setTextColor(255, 255, 255); doc.setFontSize(10); doc.setFont(undefined, 'bold')
    doc.text('RESUMEN DEL PERÍODO', pageWidth / 2, yPosition + 1, { align: 'center' })
    yPosition += 10

    const resumenData = [
      { label: 'Total Días', value: datosVistaPrevia.value.length, color: [30, 58, 138] },
      { label: 'Total Horas', value: `${totalHorasVistaPrevia.value}h`, color: [30, 58, 138] },
      { label: 'Aprobados', value: contadorEstados.value['APROBADO'] || 0, color: [34, 197, 94] },
      { label: 'Pendientes', value: contadorEstados.value['PENDIENTE'] || 0, color: [245, 158, 11] }
    ]
    const cardWidth = (pageWidth - 2 * margin - 8) / 4
    resumenData.forEach((item, index) => {
      const cardX = margin + (cardWidth + 8) * index
      doc.setFillColor(...item.color); doc.rect(cardX, yPosition - 6, cardWidth, 14, 'F')
      doc.setDrawColor(30, 58, 138); doc.rect(cardX, yPosition - 6, cardWidth, 14)
      doc.setTextColor(255, 255, 255); doc.setFontSize(6); doc.setFont(undefined, 'normal')
      doc.text(item.label, cardX + cardWidth / 2, yPosition - 2, { align: 'center' })
      doc.setFontSize(9); doc.setFont(undefined, 'bold')
      doc.text(String(item.value), cardX + cardWidth / 2, yPosition + 4, { align: 'center' })
    })

    yPosition = pageHeight - 15
    doc.setDrawColor(203, 213, 225); doc.line(margin, yPosition, pageWidth - margin, yPosition)
    doc.setTextColor(107, 114, 128); doc.setFontSize(6); doc.setFont(undefined, 'italic')
    doc.text('Sistema de Asistencias — Reporte generado automáticamente · UMSA Facultad de Ciencias Sociales', pageWidth / 2, yPosition + 8, { align: 'center' })

    const nombrePasante = `${u?.nombres || ''}_${u?.apellidos || ''}`.trim().replace(/\s+/g, '_') || `pasante_${u?.id || ''}`
    doc.save(`reporte_${tipoPdf.value}_${nombrePasante}_${new Date().toISOString().split('T')[0]}.pdf`)

  } catch (error) {
    errorDescarga.value = 'Error al generar el PDF. Intenta nuevamente.'
  } finally {
    descargando.value = false
  }
}

const isoSemana = (date) => {
  const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()))
  const dayNum = d.getUTCDay() || 7
  d.setUTCDate(d.getUTCDate() + 4 - dayNum)
  const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1))
  return Math.ceil((((d - yearStart) / 86400000) + 1) / 7)
}

const cerrarSesion = () => { authStore.logout(); router.push('/login') }
</script>

