<template>
  <div class="space-y-6">
    <!-- Cabecera -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h1 class="text-2xl font-bold text-slate-800">Reportes Diarios</h1>
        <span class="text-sm text-slate-500">{{ reportesFiltrados.length }} / {{ reportes.length }} reportes</span>
      </div>
      <button
        @click="evaluarPendiente"
        class="inline-flex items-center gap-2 bg-blue-900 text-white px-5 py-2.5 rounded-lg hover:bg-blue-800 transition-colors font-medium shadow-sm">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
        </svg>
        Evaluar siguiente pendiente
      </button>
    </div>

    <!-- Filtros -->
    <div class="bg-white rounded-lg shadow p-4">
      <div class="grid grid-cols-1 md:grid-cols-5 gap-3">
        <input
          v-model="filterText"
          type="text"
          placeholder="Buscar: pasante, actividades, #ID"
          class="border border-slate-300 rounded-lg px-3 py-2 text-sm"
        />
        <select v-model="filterEstado" class="border border-slate-300 rounded-lg px-3 py-2 text-sm bg-white">
          <option value="all">Todos los estados</option>
          <option value="PENDIENTE">Pendiente</option>
          <option value="VERIFICADO">Verificado</option>
          <option value="APROBADO">Aprobado</option>
          <option value="RECHAZADO">Rechazado</option>
          <option value="RECTIFICADO">Rectificado</option>
        </select>
        <select v-model="filterYear" class="border border-slate-300 rounded-lg px-3 py-2 text-sm bg-white">
          <option value="all">Todos los años</option>
          <option v-for="y in yearOptions" :key="y" :value="String(y)">{{ y }}</option>
        </select>
        <select v-model="filterMonth" class="border border-slate-300 rounded-lg px-3 py-2 text-sm bg-white">
          <option value="all">Todos los meses</option>
          <option v-for="m in monthOptions" :key="m.value" :value="m.value">{{ m.label }}</option>
        </select>
        <div class="flex gap-2">
          <select v-model="sortBy" class="flex-1 border border-slate-300 rounded-lg px-3 py-2 text-sm bg-white">
            <option value="newest">Más recientes</option>
            <option value="oldest">Más antiguos</option>
          </select>
          <button type="button" @click="limpiarFiltros"
            class="px-4 py-2 text-sm border border-slate-300 rounded-lg hover:bg-slate-50">
            Limpiar
          </button>
        </div>
      </div>
    </div>

    <div v-if="errorReportes" class="p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-700">
      {{ errorReportes }}
    </div>

    <!-- Tabla -->
    <div class="bg-white rounded-lg shadow overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">#</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Pasante</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Fecha</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Comentario</th>
              <th class="px-6 py-4 text-center text-xs font-semibold text-slate-500 uppercase tracking-wider">Estado</th>
              <th class="px-6 py-4 text-center text-xs font-semibold text-slate-500 uppercase tracking-wider">Acciones</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr v-if="isLoadingReportes">
              <td colspan="5" class="px-6 py-12 text-center">
                <div class="flex flex-col items-center gap-3">
                  <div class="w-8 h-8 border-2 border-slate-300 border-t-blue-600 rounded-full animate-spin"></div>
                  <p class="text-slate-500 text-sm">Cargando reportes...</p>
                </div>
              </td>
            </tr>
            <tr v-else-if="reportesFiltrados.length === 0">
              <td colspan="5" class="px-6 py-12 text-center">
                <div class="flex flex-col items-center gap-3">
                  <div class="w-12 h-12 bg-slate-100 rounded-full flex items-center justify-center">
                    <svg class="w-6 h-6 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                    </svg>
                  </div>
                  <p class="text-slate-500">No hay reportes con esos filtros</p>
                </div>
              </td>
            </tr>
            <tr v-else v-for="reporte in reportesFiltrados" :key="reporte.id" class="hover:bg-slate-50/50 transition-colors">
              <td class="px-6 py-4">
                <span class="text-sm font-mono text-slate-500">#{{ reporte.id }}</span>
              </td>
              <td class="px-6 py-4">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 font-semibold text-xs">
                    {{ getInicialesFromName(reporte.nombre_pasante) }}
                  </div>
                  <span class="text-sm font-medium text-slate-700">{{ reporte.nombre_pasante || 'Pasante #' + reporte.asistencia_id }}</span>
                </div>
              </td>
              <td class="px-6 py-4">
                <span class="text-sm text-slate-500">{{ formatearFecha(reporte.creado_en) }}</span>
              </td>
              <td class="px-6 py-4">
                <div class="max-w-md">
                  <p class="text-sm text-slate-500 line-clamp-2 mb-2">{{ reporte.actividades_realizadas }}</p>
        
                </div>
              </td>
              <td class="px-6 py-4 text-center">
                <span :class="getEstadoBadgeClass(reporte.estado_encargado)" class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium">
                  <span :class="getEstadoDotClass(reporte.estado_encargado)" class="w-1.5 h-1.5 rounded-full mr-1.5"></span>
                  {{ reporte.estado_encargado || 'PENDIENTE' }}
                </span>
              </td>
              <td class="px-6 py-4 text-center">
                <div class="flex items-center gap-2 justify-center">
                  <button @click="abrirModalEvaluacion(reporte)"
                    class="inline-flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-blue-600 hover:text-white hover:bg-blue-600 border border-blue-200 hover:border-blue-600 rounded-lg transition-all">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/>
                    </svg>
                    Evaluar
                  </button>
                  <button @click="verHistorial(reporte)"
                    class="inline-flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-purple-600 hover:text-white hover:bg-purple-600 border border-purple-200 hover:border-purple-600 rounded-lg transition-all">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                    Historial
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal evaluación -->
    <div v-if="showModalEvaluacion" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/70 px-4 backdrop-blur-sm">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-xl overflow-hidden">
        <div class="bg-gradient-to-r from-blue-900 to-blue-800 px-6 py-5 text-white flex items-start justify-between">
          <div>
            <p class="text-blue-100 text-xs font-medium uppercase tracking-wider">Evaluación de reporte</p>
            <h3 class="text-xl font-bold mt-1">Reporte #{{ reporteSeleccionado?.id }}</h3>
            <p class="text-blue-100 text-xs mt-1">{{ reporteSeleccionado?.nombre_pasante || '—' }} · {{ formatearFecha(reporteSeleccionado?.creado_en) }}</p>
          </div>
          <button type="button" @click="cerrarModalEvaluacion" class="text-blue-100 hover:text-white">✕</button>
        </div>
        <div class="p-6 space-y-4">
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">Estado</label>
            <select v-model="evaluacion.estado" class="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm bg-white">
              <option value="VERIFICADO">Verificado</option>
              <option v-if="yaEvaluado(reporteSeleccionado)" value="RECTIFICADO">Rectificado</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">Comentario (obligatorio)</label>
            <textarea v-model="evaluacion.comentarios" rows="4"
              class="w-full border border-slate-300 rounded-lg p-3 text-sm"
              placeholder="Escribe una observación..."></textarea>
          </div>
          <div v-if="yaEvaluado(reporteSeleccionado)" class="p-3 bg-amber-50 border border-amber-200 rounded-lg">
            <p class="text-sm text-amber-800">
              <strong>⚠️ Atención:</strong> Este reporte ya fue evaluado anteriormente. Solo puedes modificarlo una vez seleccionando "Rectificado".
            </p>
          </div>
          <div class="pt-4 border-t border-slate-200 flex justify-end gap-3">
            <button type="button" @click="cerrarModalEvaluacion"
              class="px-4 py-2 text-sm border rounded-lg">Cancelar</button>
            <button type="button" @click="enviarEvaluacion"
              :disabled="isSubmittingEval || !evaluacion.comentarios.trim() || (yaEvaluado(reporteSeleccionado) && evaluacion.estado !== 'RECTIFICADO')"
              class="px-5 py-2 text-sm bg-blue-900 text-white rounded-lg disabled:opacity-50">
              {{ isSubmittingEval ? 'Guardando...' : (yaEvaluado(reporteSeleccionado) ? 'Guardar Rectificación' : 'Guardar evaluación') }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal historial -->
    <div v-if="showModalHistorial" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/70 px-4 backdrop-blur-sm">
      <div class="bg-white rounded-xl shadow-2xl w-full max-w-2xl max-h-[80vh] overflow-hidden">
        <div class="bg-gradient-to-r from-blue-900 to-red-800 px-4 py-3 text-white flex items-start justify-between">
          <div>
            <p class="text-purple-100 text-xs font-medium uppercase tracking-wider">Historial de Cambios</p>
            <h3 class="text-lg font-bold mt-1">Reporte #{{ reporteSeleccionado?.id }}</h3>
            <p class="text-purple-100 text-xs mt-1">{{ reporteSeleccionado?.nombre_pasante || '—' }}</p>
          </div>
          <button type="button" @click="cerrarModalHistorial" class="text-purple-100 hover:text-white text-xl">✕</button>
        </div>
        <div class="p-4 max-h-[60vh] overflow-y-auto">
          <div v-if="isLoadingHistorial" class="flex items-center justify-center py-6">
            <div class="w-6 h-6 border-2 border-purple-300 border-t-purple-600 rounded-full animate-spin"></div>
            <span class="ml-3 text-slate-500 text-sm">Cargando historial...</span>
          </div>
          <div v-else-if="historial.length === 0" class="text-center py-6">
            <div class="w-12 h-12 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <svg class="w-6 h-6 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <p class="text-slate-500 text-sm">No hay historial de cambios para este reporte.</p>
          </div>
          <div v-else class="space-y-3">
            <div v-for="item in historial" :key="item.id"
              class="border border-slate-200 rounded-lg p-3 hover:bg-slate-50 transition-colors">
              <div class="flex items-start justify-between mb-2">
                <div class="flex items-center gap-2">
                  <div class="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center text-purple-600 font-semibold text-xs">
                    {{ getInicialesFromName(item.actor_nombre) }}
                  </div>
                  <div>
                    <p class="font-medium text-slate-800 text-sm">{{ item.actor_nombre }}</p>
                    <p class="text-xs text-slate-500">{{ item.actor_rol }} · {{ formatearFecha(item.creado_en) }}</p>
                  </div>
                </div>
                <div class="flex items-center gap-1 text-xs">
                  <span :class="getEstadoBadgeClass(item.estado_anterior)" class="inline-flex items-center px-1.5 py-0.5 rounded text-xs font-medium">
                    {{ item.estado_anterior || 'SIN ESTADO' }}
                  </span>
                  <svg class="w-3 h-3 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
                  </svg>
                  <span :class="getEstadoBadgeClass(item.estado_nuevo)" class="inline-flex items-center px-1.5 py-0.5 rounded text-xs font-medium">
                    {{ item.estado_nuevo }}
                  </span>
                </div>
              </div>
              <div class="bg-slate-50 rounded p-2">
                <p class="text-xs text-slate-600 font-medium mb-1">Comentario:</p>
                <p class="text-xs text-slate-700 whitespace-pre-wrap">{{ item.comentarios }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import router from '../router'
import api from '../services/api'

type Reporte = {
  id: number
  asistencia_id: number
  actividades_realizadas: string
  estado: string
  comentarios_director?: string | null
  creado_en?: string | Date
  nombre_pasante?: string | null
  evaluaciones_count?: number
  ya_rectificado?: boolean
}

const authStore = useAuthStore()

const reportes            = ref<Reporte[]>([])
const isLoadingReportes   = ref(false)
const errorReportes       = ref('')
const reporteSeleccionado = ref<Reporte | null>(null)
const showModalEvaluacion = ref(false)
const showModalHistorial  = ref(false)
const isSubmittingEval    = ref(false)
const isLoadingHistorial  = ref(false)
const historial           = ref([])
const evaluacion          = ref({ estado: 'VERIFICADO', comentarios: '' })

const filterText   = ref('')
const filterEstado = ref<'all' | 'PENDIENTE' | 'VERIFICADO' | 'APROBADO' | 'RECHAZADO' | 'RECTIFICADO'>('all')
const filterYear   = ref<'all' | string>('all')
const filterMonth  = ref<'all' | string>('all')
const sortBy       = ref<'newest' | 'oldest'>('newest')

const monthOptions = [
  { value: '1',  label: 'Enero' },
  { value: '2',  label: 'Febrero' },
  { value: '3',  label: 'Marzo' },
  { value: '4',  label: 'Abril' },
  { value: '5',  label: 'Mayo' },
  { value: '6',  label: 'Junio' },
  { value: '7',  label: 'Julio' },
  { value: '8',  label: 'Agosto' },
  { value: '9',  label: 'Septiembre' },
  { value: '10', label: 'Octubre' },
  { value: '11', label: 'Noviembre' },
  { value: '12', label: 'Diciembre' },
]

const limpiarFiltros = () => {
  filterText.value   = ''
  filterEstado.value = 'all'
  filterYear.value   = 'all'
  filterMonth.value  = 'all'
  sortBy.value       = 'newest'
}

const parseDate = (value: unknown): Date | null => {
  if (!value) return null
  const d = value instanceof Date ? value : new Date(String(value))
  return Number.isNaN(d.getTime()) ? null : d
}

const formatearFecha = (value: unknown) => {
  const d = parseDate(value)
  if (!d) return '—'
  return d.toLocaleDateString('es-BO', { year: 'numeric', month: '2-digit', day: '2-digit' })
}

const yearOptions = computed(() => {
  const years = new Set<number>()
  for (const r of reportes.value) {
    const d = parseDate(r.creado_en)
    if (d) years.add(d.getFullYear())
  }
  return Array.from(years).sort((a, b) => b - a)
})

const reportesFiltrados = computed(() => {
  let list = reportes.value.slice()

  if (filterEstado.value !== 'all') {
    if (filterEstado.value === 'PENDIENTE') {
      list = list.filter(r => !r.estado_encargado && !r.estado_admin)
    } else {
      list = list.filter(r => r.estado_encargado === filterEstado.value)
    }
  }

  if (filterYear.value !== 'all' || filterMonth.value !== 'all') {
    list = list.filter(r => {
      const d = parseDate(r.creado_en)
      if (!d) return false
      if (filterYear.value  !== 'all' && String(d.getFullYear())  !== String(filterYear.value))  return false
      if (filterMonth.value !== 'all' && String(d.getMonth() + 1) !== String(filterMonth.value)) return false
      return true
    })
  }

  const q = filterText.value.trim().toLowerCase()
  if (q) {
    list = list.filter(r =>
      (r.nombre_pasante         || '').toLowerCase().includes(q) ||
      (r.actividades_realizadas || '').toLowerCase().includes(q) ||
      String(r.id).includes(q) ||
      String(r.asistencia_id).includes(q)
    )
  }

  const factor = sortBy.value === 'newest' ? -1 : 1
  list.sort((a, b) => {
    const da = parseDate(a.creado_en)?.getTime() ?? 0
    const db = parseDate(b.creado_en)?.getTime() ?? 0
    if (da === db) return 0
    return da < db ? -1 * factor : 1 * factor
  })

  return list
})

const cargarReportes = async () => {
  isLoadingReportes.value = true
  errorReportes.value     = ''
  try {
    const { data } = await api.get('/reportes/listar')
    reportes.value = data
  } catch (e: any) {
    if (e.response?.status === 401) cerrarSesion()
    else {
      errorReportes.value = e.response?.data?.detail || 'No se pudo cargar los reportes.'
      reportes.value      = []
    }
  } finally {
    isLoadingReportes.value = false
  }
}

const abrirModalEvaluacion = (reporte: Reporte) => {
  if (yaRectificado(reporte)) return
  reporteSeleccionado.value    = reporte
  evaluacion.value.estado      = yaEvaluado(reporte)
    ? 'RECTIFICADO'
    : (reporte.estado_encargado && reporte.estado_encargado !== '' ? reporte.estado_encargado : 'VERIFICADO')
  evaluacion.value.comentarios = (reporte as any).comentarios_director || ''
  showModalEvaluacion.value    = true
}

const cerrarModalEvaluacion = () => {
  showModalEvaluacion.value = false
  reporteSeleccionado.value = null
}

const enviarEvaluacion = async () => {
  if (!reporteSeleccionado.value) return
  if (!evaluacion.value.comentarios?.trim()) { alert('El comentario es obligatorio.'); return }
  if (yaEvaluado(reporteSeleccionado.value) && evaluacion.value.estado !== 'RECTIFICADO') {
    alert('Este reporte ya fue evaluado. Solo puedes seleccionar "Rectificado" para modificar.')
    return
  }
  if (yaRectificado(reporteSeleccionado.value)) {
    alert('Este reporte ya fue rectificado. No se permiten más modificaciones.')
    return
  }
  isSubmittingEval.value = true
  try {
    await api.put(`/reportes/evaluar/${reporteSeleccionado.value.id}`, {
      estado:               evaluacion.value.estado,
      comentarios_director: evaluacion.value.comentarios.trim(),
      es_rectificacion:     yaEvaluado(reporteSeleccionado.value),
    })
    await cargarReportes()
    cerrarModalEvaluacion()
    alert(yaEvaluado(reporteSeleccionado.value) ? '✅ Rectificación guardada con éxito' : '✅ Evaluación guardada con éxito')
  } catch {
    alert('Error al guardar la evaluación.')
  } finally {
    isSubmittingEval.value = false
  }
}

const yaEvaluado = (reporte?: Reporte | null): boolean => {
  if (!reporte) return false
  const e = reporte.estado_encargado || ''
  return e !== '' && e !== 'RECTIFICADO'
}

const yaRectificado = (reporte?: Reporte | null): boolean => {
  if (!reporte) return false
  return reporte.estado_encargado === 'RECTIFICADO'
}

const verHistorial = async (reporte: Reporte) => {
  reporteSeleccionado.value = reporte
  showModalHistorial.value  = true
  await cargarHistorial(reporte.id)
}

const cargarHistorial = async (reporteId: number) => {
  isLoadingHistorial.value = true
  try {
    const { data } = await api.get(`/reportes/historial/${reporteId}`)
    historial.value = data
  } catch (e: any) {
    console.error('Error al cargar historial:', e)
    historial.value = []
  } finally {
    isLoadingHistorial.value = false
  }
}

const cerrarModalHistorial = () => {
  showModalHistorial.value  = false
  reporteSeleccionado.value = null
  historial.value           = []
}

const evaluarPendiente = () => {
  const pendiente = reportes.value.find(r => !r.estado_encargado && !r.estado_admin)
  if (pendiente) abrirModalEvaluacion(pendiente)
  else alert('No hay reportes pendientes.')
}

const getInicialesFromName = (fullName?: string | null) => {
  if (!fullName) return '?'
  const parts = fullName.split(' ')
  return `${parts[0]?.[0] || ''}${parts[1]?.[0] || ''}`.toUpperCase()
}

const getEstadoBadgeClass = (estado?: string) => {
  if (estado === 'APROBADO')    return 'bg-emerald-50 text-emerald-700'
  if (estado === 'VERIFICADO')  return 'bg-blue-50 text-blue-700'
  if (estado === 'RECHAZADO')   return 'bg-red-50 text-red-700'
  if (estado === 'RECTIFICADO') return 'bg-purple-50 text-purple-700'
  return 'bg-amber-50 text-amber-700'
}

const getEstadoDotClass = (estado?: string) => {
  if (estado === 'APROBADO')    return 'bg-emerald-500'
  if (estado === 'VERIFICADO')  return 'bg-blue-500'
  if (estado === 'RECHAZADO')   return 'bg-red-500'
  if (estado === 'RECTIFICADO') return 'bg-purple-500'
  return 'bg-amber-500'
}

const cerrarSesion = () => {
  authStore.logout()
  router.push('/')
}

onMounted(cargarReportes)
</script>