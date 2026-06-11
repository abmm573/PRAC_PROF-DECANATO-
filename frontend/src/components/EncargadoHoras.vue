<template>
  <div class="space-y-6">
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h1 class="text-2xl font-bold text-slate-800">Horas de Pasantes</h1>
        <p class="text-sm text-slate-500">
          {{ itemsFiltrados.length }} / {{ items.length }} pasantes
          <span v-if="periodoLabel" class="ml-2">· {{ periodoLabel }}</span>
        </p>
      </div>
      <div class="flex items-center gap-2">
        <button
          type="button"
          @click="descargarExcel"
          class="inline-flex items-center gap-2 border border-slate-300 bg-green-50 px-4 py-2.5 rounded-lg hover:bg-green-100 transition-colors text-sm font-medium text-green-700">
          Excel
        </button>
        <button
          type="button"
          @click="cargarResumen"
          class="inline-flex items-center gap-2 bg-blue-900 text-white px-5 py-2.5 rounded-lg hover:bg-blue-800 transition-colors font-medium shadow-sm">
          Actualizar
        </button>
      </div>
    </div>

    <div class="bg-white rounded-lg shadow p-4">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-3">
        <input
          v-model="filterText"
          type="text"
          placeholder="Buscar: pasante, @username"
          class="border border-slate-300 rounded-lg px-3 py-2 text-sm"
        />

        <select v-model="tipo" class="border border-slate-300 rounded-lg px-3 py-2 text-sm bg-white">
          <option value="dia">Día</option>
          <option value="semana">Semana</option>
          <option value="mes">Mes</option>
          <option value="total">Total</option>
        </select>

        <input
          v-model="fecha"
          :disabled="tipo === 'total'"
          type="date"
          class="border border-slate-300 rounded-lg px-3 py-2 text-sm bg-white disabled:bg-slate-100 disabled:text-slate-400"
        />

        <select v-model="sortBy" class="border border-slate-300 rounded-lg px-3 py-2 text-sm bg-white">
          <option value="horas_desc">Más horas</option>
          <option value="horas_asc">Menos horas</option>
          <option value="nombre_asc">Nombre (A-Z)</option>
        </select>
      </div>

      <div v-if="error" class="mt-3 p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-700">
        {{ error }}
      </div>
    </div>

    <div class="bg-white rounded-lg shadow overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Pasante</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Usuario</th>
              <th class="px-6 py-4 text-center text-xs font-semibold text-slate-500 uppercase tracking-wider">Registros</th>
              <th class="px-6 py-4 text-center text-xs font-semibold text-slate-500 uppercase tracking-wider">Sin Salida Registrada</th>
              <th class="px-6 py-4 text-right text-xs font-semibold text-slate-500 uppercase tracking-wider">Horas</th>
              <th class="px-6 py-4 text-right text-xs font-semibold text-slate-500 uppercase tracking-wider">Progreso</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr v-if="isLoading">
              <td colspan="6" class="px-6 py-12 text-center">
                <div class="flex flex-col items-center gap-3">
                  <div class="w-8 h-8 border-2 border-slate-300 border-t-blue-600 rounded-full animate-spin"></div>
                  <p class="text-slate-500 text-sm">Cargando resumen...</p>
                </div>
              </td>
            </tr>

            <tr v-else-if="itemsFiltradosOrdenados.length === 0">
              <td colspan="6" class="px-6 py-12 text-center">
                <div class="flex flex-col items-center gap-3">
                  <div class="w-12 h-12 bg-slate-100 rounded-full flex items-center justify-center">
                    <svg class="w-6 h-6 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                    </svg>
                  </div>
                  <p class="text-slate-500">No hay datos con esos filtros</p>
                </div>
              </td>
            </tr>

            <tr v-else v-for="row in itemsFiltradosOrdenados" :key="row.pasante_id" class="hover:bg-slate-50/50 transition-colors">
              <td class="px-6 py-4">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center text-blue-700 font-semibold text-xs">
                    {{ getIniciales(row.nombres, row.apellidos) }}
                  </div>
                  <div>
                    <p class="text-sm font-medium text-slate-800">{{ row.nombres }} {{ row.apellidos }}</p>
                    <p class="text-xs text-slate-400">ID: {{ row.pasante_id }}</p>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4">
                <span class="text-sm text-slate-600 font-mono">@{{ row.username }}</span>
              </td>
              <td class="px-6 py-4 text-center">
                <span class="text-sm text-slate-600">{{ row.registros }}</span>
              </td>
              <td class="px-6 py-4 text-center">
                <div class="flex items-center justify-center gap-2">
                  <span
                    :class="row.sin_salida > 0 ? 'bg-amber-50 text-amber-700 border-amber-200' : 'bg-emerald-50 text-emerald-700 border-emerald-200'"
                    class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium border">
                    {{ row.sin_salida }}
                  </span>
                  <div v-if="row.sin_salida > 0" class="w-4 h-4 bg-amber-100 rounded-full flex items-center justify-center" title="Registros sin hora de salida">
                    <svg class="w-2.5 h-2.5 text-amber-600" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
                    </svg>
                  </div>
                  <div v-else class="w-4 h-4 bg-emerald-100 rounded-full flex items-center justify-center" title="Todos los registros completos">
                    <svg class="w-2.5 h-2.5 text-emerald-600" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 text-right">
                <span class="text-sm font-semibold text-slate-800">{{ formatHoras(row.horas) }}</span>
              </td>
              <td class="px-6 py-4 text-right">
                <div class="flex items-center justify-end gap-3">
                  <div class="w-28 h-2 bg-slate-100 rounded-full overflow-hidden">
                    <div class="h-full bg-emerald-500 rounded-full" :style="{ width: progresoPct(row.horas) + '%' }"></div>
                  </div>
                  <span class="text-xs text-slate-500 w-12 text-right">{{ progresoPct(row.horas) }}%</span>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import api from '../services/api'
import { useAuthStore } from '../stores/auth'
import * as XLSX from 'xlsx'

const authStore = useAuthStore()

const tipo = ref('semana')
const fecha = ref(new Date().toISOString().slice(0, 10))
const sortBy = ref('horas_desc')
const filterText = ref('')

const items = ref([])
const periodo = ref(null)

const isLoading = ref(false)
const error = ref('')

const periodoLabel = computed(() => {
  if (!periodo.value) return ''
  if (periodo.value.tipo === 'total') return 'Total'
  if (periodo.value.inicio && periodo.value.fin) {
    return `${periodo.value.tipo} · ${periodo.value.inicio} → ${periodo.value.fin}`
  }
  return periodo.value.tipo
})

const itemsFiltrados = computed(() => {
  const q = (filterText.value || '').trim().toLowerCase()
  if (!q) return items.value
  return items.value.filter(r => {
    const nombre = `${r.nombres || ''} ${r.apellidos || ''}`.toLowerCase()
    const user = (r.username || '').toLowerCase()
    return nombre.includes(q) || user.includes(q) || String(r.pasante_id).includes(q)
  })
})

const itemsFiltradosOrdenados = computed(() => {
  const arr = [...itemsFiltrados.value]
  if (sortBy.value === 'horas_asc') {
    arr.sort((a, b) => (a.horas || 0) - (b.horas || 0))
  } else if (sortBy.value === 'nombre_asc') {
    arr.sort((a, b) => (`${a.nombres} ${a.apellidos}`).localeCompare(`${b.nombres} ${b.apellidos}`))
  } else {
    arr.sort((a, b) => (b.horas || 0) - (a.horas || 0))
  }
  return arr
})

const formatHoras = (h) => {
  const v = Number(h || 0)
  return `${v.toFixed(2)}h`
}

const progresoPct = (h) => {
  const total = 240
  const v = Number(h || 0)
  const pct = Math.max(0, Math.min(100, Math.round((v / total) * 100)))
  return pct
}

const getIniciales = (nombres, apellidos) => {
  const n = (nombres || '').trim().split(/\s+/).filter(Boolean)
  const a = (apellidos || '').trim().split(/\s+/).filter(Boolean)
  const i1 = n[0]?.[0] || ''
  const i2 = a[0]?.[0] || n[1]?.[0] || ''
  return (i1 + i2).toUpperCase()
}

const cargarResumen = async () => {
  error.value = ''
  isLoading.value = true
  try {
    const params = { tipo: tipo.value }
    if (tipo.value !== 'total') params.fecha = fecha.value

    // Admin podría enviar carrera_id; Encargado/Pasante se ignora del lado backend
    if (authStore.user?.rol_id === 1 && authStore.user?.carrera_id) {
      params.carrera_id = authStore.user.carrera_id
    }

    const { data } = await api.get('/asistencias/resumen-horas', { params })
    items.value = data?.items || []
    periodo.value = data?.periodo || null
  } catch (e) {
    console.error('Error resumen horas:', e)
    error.value = e?.response?.data?.detail || 'No se pudo cargar el resumen de horas.'
    items.value = []
    periodo.value = null
  } finally {
    isLoading.value = false
  }
}

const descargarExcel = () => {
  const rows = itemsFiltradosOrdenados.value
  
  // Crear libro de Excel
  const wb = XLSX.utils.book_new()
  
  // Preparar datos para Excel con nombres en español
  const datos = rows.map(r => ({
    'ID Pasante': r.pasante_id,
    'Nombres': r.nombres || '',
    'Apellidos': r.apellidos || '',
    'Username': r.username || '',
    'Total Registros': r.registros || 0,
    'Registros sin Salida': r.sin_salida || 0,
    'Total Horas': Number(r.horas || 0).toFixed(2),
    'Progreso (%)': progresoPct(r.horas) + '%',
    'Estado Pasantía': progresoPct(r.horas) >= 100 ? 'COMPLETADA' : 'EN CURSO'
  }))
  
  // Crear hoja de Excel
  const ws = XLSX.utils.json_to_sheet(datos, {
    header: ['ID Pasante', 'Nombres', 'Apellidos', 'Username', 'Total Registros', 'Registros sin Salida Registrada', 'Total Horas', 'Progreso (%)', 'Estado Pasantía']
  })
  
  // Aplicar estilos a los encabezados
  const range = XLSX.utils.decode_range(ws['!ref'] || 'A1')
  for (let col = range.s.c; col <= range.e.c; col++) {
    const cellAddress = XLSX.utils.encode_cell({ r: 0, c: col })
    if (!ws[cellAddress]) ws[cellAddress] = {}
    ws[cellAddress].s = {
      font: { bold: true, color: { rgb: 'FFFFFF' } },
      fill: { fgColor: { rgb: '059669' } },
      alignment: { horizontal: 'center', vertical: 'center' }
    }
  }
  
  // Ajustar ancho de columnas
  ws['!cols'] = [
    { width: 12 },  // ID Pasante
    { width: 20 },  // Nombres
    { width: 20 },  // Apellidos
    { width: 15 },  // Username
    { width: 18 },  // Total Registros
    { width: 25 },  // Registros sin Salida Registrada
    { width: 15 },  // Total Horas
    { width: 15 },  // Progreso (%)
    { width: 18 }   // Estado Pasantía
  ]
  
  XLSX.utils.book_append_sheet(wb, ws, 'Resumen de Horas')
  
  // Agregar hoja de estadísticas adicionales
  const stats = [
    { 'Métrica': 'Total de Pasantes', 'Valor': rows.length },
    { 'Métrica': 'Tipo de Reporte', 'Valor': tipo.value || 'general' },
    { 'Métrica': 'Período', 'Valor': periodoLabel.value || 'Todo el tiempo' },
    { 'Métrica': 'Fecha de Generación', 'Valor': new Date().toLocaleDateString('es-BO') },
    { 'Métrica': 'Generado por', 'Valor': authStore.user?.nombres + ' ' + (authStore.user?.apellidos || '') },
    { 'Métrica': 'Carrera', 'Valor': authStore.user?.carrera_nombre || 'Todas' },
    { 'Métrica': 'Total Horas Acumuladas', 'Valor': rows.reduce((sum, r) => sum + Number(r.horas || 0), 0).toFixed(2) + 'h' },
    { 'Métrica': 'Promedio Horas por Pasante', 'Valor': rows.length > 0 ? (rows.reduce((sum, r) => sum + Number(r.horas || 0), 0) / rows.length).toFixed(2) + 'h' : '0h' },
    { 'Métrica': 'Pasantes Completados', 'Valor': rows.filter(r => progresoPct(r.horas) >= 100).length }
  ]
  
  const wsStats = XLSX.utils.json_to_sheet(stats)
  wsStats['!cols'] = [
    { width: 30 }, // Métrica
    { width: 25 }  // Valor
  ]
  
  // Estilos para hoja de estadísticas
  const rangeStats = XLSX.utils.decode_range(wsStats['!ref'] || 'A1')
  for (let col = rangeStats.s.c; col <= rangeStats.e.c; col++) {
    const cellAddress = XLSX.utils.encode_cell({ r: 0, c: col })
    if (!wsStats[cellAddress]) wsStats[cellAddress] = {}
    wsStats[cellAddress].s = {
      font: { bold: true, color: { rgb: 'FFFFFF' } },
      fill: { fgColor: { rgb: '7C3AED' } },
      alignment: { horizontal: 'center', vertical: 'center' }
    }
  }
  
  XLSX.utils.book_append_sheet(wb, wsStats, 'Estadísticas')
  
  // Descargar archivo
  const safeTipo = (tipo.value || 'periodo')
  XLSX.writeFile(wb, `resumen_horas_${safeTipo}_${new Date().toISOString().slice(0, 10)}.xlsx`)
}

onMounted(() => {
  cargarResumen()
})
</script>
