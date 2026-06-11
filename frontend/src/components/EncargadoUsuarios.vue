<template>
  <div class="space-y-6">
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h1 class="text-2xl font-bold text-slate-800">Pasantes</h1>
        <p class="text-slate-500 mt-1">Carrera ID: {{ authStore.user?.carrera_id ?? '—' }}</p>
      </div>

      <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-2">
        <input v-model="filterText" type="text" placeholder="Buscar: nombre, username, CI, email"
          class="border border-slate-300 rounded-lg px-3 py-2 text-sm" />
        <select v-model="filterState" class="border border-slate-300 rounded-lg px-3 py-2 text-sm bg-white">
          <option value="all">Todos</option>
          <option value="active">Activos</option>
          <option value="inactive">Inactivos</option>
        </select>
        <button type="button" @click="abrirModalCrear"
          class="inline-flex items-center justify-center gap-2 bg-blue-900 text-white px-5 py-2.5 rounded-lg hover:bg-blue-800 transition-colors font-medium shadow-sm">
          Nuevo Pasante
        </button>
      </div>
    </div>

    <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-slate-200">
          <thead class="bg-slate-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Pasante</th>
              <th class="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Email</th>
              <th class="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">CI</th>
              <th class="px-6 py-3 text-center text-xs font-semibold text-slate-500 uppercase tracking-wider">Estado</th>
              <th class="px-6 py-3 text-right text-xs font-semibold text-slate-500 uppercase tracking-wider">Acciones</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr v-if="isLoadingUsuarios">
              <td colspan="5" class="px-6 py-10 text-center text-slate-500">Cargando...</td>
            </tr>
            <tr v-else-if="usuariosFiltrados.length === 0">
              <td colspan="5" class="px-6 py-10 text-center text-slate-500">Sin pasantes.</td>
            </tr>
            <tr v-else v-for="u in usuariosFiltrados" :key="u.id" class="hover:bg-slate-50/50">
              <td class="px-6 py-4">
                <div class="flex items-center gap-3">
                  <div class="w-9 h-9 bg-blue-900 rounded-full flex items-center justify-center text-white text-xs font-bold">
                    {{ getIniciales(u.nombres, u.apellidos) }}
                  </div>
                  <div class="min-w-0">
                    <p class="text-sm font-semibold text-slate-800 truncate">{{ u.nombres }} {{ u.apellidos }}</p>
                    <p class="text-xs text-slate-400 font-mono">@{{ u.username }}</p>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 text-sm text-slate-600">{{ u.email }}</td>
              <td class="px-6 py-4 text-sm text-slate-600">{{ u.carnet_identidad }}</td>
              <td class="px-6 py-4 text-center">
                <span :class="u.estado ? 'bg-emerald-50 text-emerald-700 border-emerald-200' : 'bg-slate-100 text-slate-600 border-slate-200'"
                  class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium border">
                  {{ u.estado ? 'Activo' : 'Inactivo' }}
                </span>
              </td>
              <td class="px-6 py-4 text-right">
                <button class="text-sm text-blue-700 hover:underline" @click="abrirModalVer(u)">Ver</button>
                <span class="mx-2 text-slate-300">|</span>
                <button class="text-sm text-slate-700 hover:underline" @click="abrirModalEditar(u)">Editar</button>
                <span class="mx-2 text-slate-300">|</span>
                <button class="text-sm text-emerald-700 hover:text-emerald-900 hover:underline font-medium"
                  @click="descargarPdfPasante(u)" title="Descargar PDF">PDF</button>
                <span class="mx-2 text-slate-300">|</span>
                <button class="text-sm" :class="u.estado ? 'text-red-600' : 'text-emerald-700'"
                  @click="confirmarCambioEstado(u)">
                  {{ u.estado ? 'Baja' : 'Reactivar' }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal PDF -->
    <div v-if="showModalPdf" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/70 px-4 backdrop-blur-sm">
      <div class="bg-white rounded-xl shadow-2xl w-full max-w-md overflow-hidden">
        <div class="bg-gradient-to-r from-emerald-600 to-emerald-700 px-6 py-4 text-white">
          <h3 class="text-lg font-semibold flex items-center gap-2">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414A1 1 0 0119 9.414V19a2 2 0 01-2 2z"/>
            </svg>
            Descargar PDF de Pasante
          </h3>
          <p class="text-emerald-100 text-sm mt-1">{{ pasanteSeleccionado?.nombres }} {{ pasanteSeleccionado?.apellidos }}</p>
        </div>

        <div class="p-6 space-y-4">
          <div>
            <label class="block text-sm font-semibold text-slate-700 mb-2">Tipo de Reporte</label>
            <div class="flex rounded-lg overflow-hidden border border-slate-300">
              <button @click="tipoPdfSeleccionado = 'semanal'"
                :class="tipoPdfSeleccionado === 'semanal' ? 'bg-emerald-600 text-white' : 'bg-white text-slate-600 hover:bg-slate-50'"
                class="px-4 py-3 text-sm font-medium transition-all duration-200 flex-1">Semanal</button>
              <button @click="tipoPdfSeleccionado = 'mensual'"
                :class="tipoPdfSeleccionado === 'mensual' ? 'bg-emerald-600 text-white' : 'bg-white text-slate-600 hover:bg-slate-50'"
                class="px-4 py-3 text-sm font-medium transition-all duration-200 flex-1">Mensual</button>
            </div>
          </div>

          <!-- Semanal -->
          <div v-if="tipoPdfSeleccionado === 'semanal'">
            <label class="block text-sm font-semibold text-slate-700 mb-2">Seleccionar Semana</label>
            <div class="space-y-3">
              <div>
                <label class="block text-xs text-slate-600 mb-1">Cualquier día de la semana</label>
                <input type="date" v-model="fechaPdfSeleccionada"
                  class="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none
                         focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all" />
              </div>
              <div v-if="infoSemanaPdf" class="bg-emerald-50 border border-emerald-200 rounded-lg p-3">
                <p class="text-sm text-emerald-800 font-medium">{{ infoSemanaPdf }}</p>
              </div>
            </div>
          </div>

          <!-- Mensual -->
          <div v-if="tipoPdfSeleccionado === 'mensual'">
            <label class="block text-sm font-semibold text-slate-700 mb-2">Seleccionar Mes y Año</label>
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block text-xs text-slate-600 mb-1">Mes</label>
                <select v-model="mesPdfSeleccionado"
                  class="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none
                         focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all">
                  <option v-for="(nombre, idx) in mesesNombres" :key="idx + 1" :value="idx + 1">{{ nombre }}</option>
                </select>
              </div>
              <div>
                <label class="block text-xs text-slate-600 mb-1">Año</label>
                <select v-model="anioPdfSeleccionado"
                  class="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none
                         focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all">
                  <option v-for="y in aniosDisponibles" :key="y" :value="y">{{ y }}</option>
                </select>
              </div>
            </div>
            <div v-if="mesPdfSeleccionado && anioPdfSeleccionado" class="bg-blue-50 border border-blue-200 rounded-lg p-3 mt-3">
              <p class="text-sm text-blue-800 font-medium">Reporte: {{ mesesNombres[mesPdfSeleccionado - 1] }} {{ anioPdfSeleccionado }}</p>
            </div>
          </div>

          <div class="flex justify-end gap-3 pt-4 border-t border-slate-200">
            <button @click="showModalPdf = false"
              class="px-4 py-2 text-sm font-medium text-slate-600 hover:text-slate-800 transition-colors">
              Cancelar
            </button>
            <button @click="ejecutarDescargaPdf" :disabled="descargandoPdf || !puedeDescargarPdf"
              class="inline-flex items-center gap-2 bg-emerald-600 hover:bg-emerald-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed">
              <svg v-if="descargandoPdf" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
              </svg>
              {{ descargandoPdf ? 'Descargando...' : 'Descargar PDF' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Ver -->
    <div v-if="showModalVer" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/70 px-4 backdrop-blur-sm">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-2xl overflow-hidden">
        <div class="bg-gradient-to-r from-blue-900 to-blue-800 px-6 py-5 text-white flex items-start justify-between">
          <div>
            <p class="text-blue-100 text-xs font-medium uppercase tracking-wider">Pasante</p>
            <h3 class="text-xl font-bold mt-1">{{ pasanteSeleccionado?.nombres }} {{ pasanteSeleccionado?.apellidos }}</h3>
          </div>
          <button type="button" @click="showModalVer = false" class="text-blue-100 hover:text-white">✕</button>
        </div>

        <div class="p-6" v-if="pasanteSeleccionado">
          <div class="flex gap-2 mb-4">
            <button type="button" @click="tabVer = 'detalles'"
              :class="tabVer === 'detalles' ? 'bg-slate-100 text-slate-800' : 'bg-transparent text-slate-600'"
              class="px-3 py-1.5 rounded-lg text-xs font-semibold border border-slate-200">Detalles</button>
            <button type="button" @click="tabVer = 'historial'"
              :class="tabVer === 'historial' ? 'bg-slate-100 text-slate-800' : 'bg-transparent text-slate-600'"
              class="px-3 py-1.5 rounded-lg text-xs font-semibold border border-slate-200">Historial</button>
          </div>

          <div v-if="tabVer === 'detalles'" class="space-y-4">
            <div :class="cumplioPasantia ? 'bg-emerald-50 border-emerald-200 text-emerald-700' : 'bg-slate-50 border-slate-200 text-slate-700'"
              class="p-3 rounded-lg border">
              <p class="text-sm font-semibold">{{ cumplioPasantia ? 'Pasantía completada' : 'Progreso de pasantía' }}</p>
              <p class="text-xs mt-0.5" v-if="errorHistorial">{{ errorHistorial }}</p>
              <p class="text-xs mt-0.5" v-else>Horas: {{ isLoadingHistorial ? '...' : totalHorasPasante }} / 240</p>
            </div>

            <div class="grid sm:grid-cols-2 gap-3">
              <div class="p-3 bg-slate-50 rounded-lg">
                <p class="text-xs text-slate-400">Username</p>
                <p class="text-sm font-semibold text-slate-800">{{ pasanteSeleccionado.username }}</p>
              </div>
              <div class="p-3 bg-slate-50 rounded-lg">
                <p class="text-xs text-slate-400">Email</p>
                <p class="text-sm font-semibold text-slate-800">{{ pasanteSeleccionado.email }}</p>
              </div>
              <div class="p-3 bg-slate-50 rounded-lg">
                <p class="text-xs text-slate-400">CI</p>
                <p class="text-sm font-semibold text-slate-800">{{ pasanteSeleccionado.carnet_identidad }}</p>
              </div>
              <div class="p-3 bg-slate-50 rounded-lg">
                <p class="text-xs text-slate-400">RU</p>
                <p class="text-sm font-semibold text-slate-800">{{ pasanteSeleccionado.ru ?? '—' }}</p>
              </div>
              <div class="p-3 bg-slate-50 rounded-lg sm:col-span-2">
                <p class="text-xs text-slate-400">Unidad asignada</p>
                <p class="text-sm font-semibold text-slate-800">{{ pasanteSeleccionado.unidad_asignada ?? '—' }}</p>
              </div>
              <div class="p-3 bg-slate-50 rounded-lg">
                <p class="text-xs text-slate-400">Carrera ID</p>
                <p class="text-sm font-semibold text-slate-800">{{ pasanteSeleccionado.carrera_id ?? '—' }}</p>
              </div>
            </div>
          </div>

          <div v-else class="space-y-3">
            <div class="flex flex-col sm:flex-row gap-2">
              <select v-model="filterHistorialYear" class="border border-slate-300 rounded-lg px-3 py-2 text-xs bg-white">
                <option value="all">Todos los años</option>
                <option v-for="y in historialYears" :key="y" :value="String(y)">{{ y }}</option>
              </select>
              <select v-model="filterHistorialMonth" class="border border-slate-300 rounded-lg px-3 py-2 text-xs bg-white">
                <option value="all">Todos los meses</option>
                <option v-for="m in monthOptions" :key="m.value" :value="m.value">{{ m.label }}</option>
              </select>
              <select v-model="historialVista" class="border border-slate-300 rounded-lg px-3 py-2 text-xs bg-white">
                <option value="detalle">Detalle</option>
                <option value="dia">Por día</option>
                <option value="semana">Por semana</option>
                <option value="mes">Por mes</option>
              </select>
              <button type="button" @click="refrescarHistorial" class="px-3 py-2 text-xs border border-slate-300 rounded-lg hover:bg-slate-50">Actualizar</button>
              <button type="button" @click="descargarExcelHistorial" class="px-3 py-2 text-xs border border-slate-300 rounded-lg hover:bg-slate-50 bg-green-50 text-green-700 font-semibold">📊 Excel</button>
              <span v-if="isLoadingHistorial" class="self-center text-xs text-slate-500">Cargando...</span>
            </div>

            <p v-if="errorHistorial" class="text-xs text-red-600 bg-red-50 border border-red-200 p-2 rounded">{{ errorHistorial }}</p>
            <p class="text-xs text-slate-500">Registros: {{ historialFiltrado.length }} · Horas: {{ totalHorasHistorial }}h</p>
            <p class="text-xs text-slate-500">Esta semana: {{ horasSemanaActual }}h · Este mes: {{ horasMesActual }}h</p>

            <div v-if="historialVista === 'detalle'">
              <div v-if="historialFiltrado.length" class="border border-slate-200 rounded-xl overflow-hidden">
                <div class="max-h-72 overflow-y-auto">
                  <div v-for="a in historialFiltrado" :key="a.id" class="p-3 border-b border-slate-100 last:border-b-0">
                    <div class="flex items-start justify-between gap-3">
                      <div class="min-w-0">
                        <p class="text-sm font-semibold text-slate-800">
                          {{ formatFecha(a.fecha) }} · {{ formatHora(a.hora_entrada) }} → {{ a.hora_salida ? formatHora(a.hora_salida) : '—' }}
                        </p>
                        <p class="text-xs text-slate-500 mt-0.5">
                          Horas: {{ a.horas_trabajadas ?? '—' }}h ·
                          <span v-if="a.reporte">Reporte: {{ a.reporte.estado }}</span>
                          <span v-else>Sin reporte</span>
                        </p>
                        <p v-if="a.reporte?.actividades_realizadas" class="text-xs text-slate-600 mt-2 line-clamp-2">{{ a.reporte.actividades_realizadas }}</p>
                      </div>
                      <div class="shrink-0 flex flex-col items-end gap-2">
                        <span v-if="a.reporte" :class="reporteBadge(a.reporte.estado)" class="text-[11px] font-semibold px-2 py-0.5 rounded-full border">
                          {{ a.reporte.estado }}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <p v-else class="text-xs text-slate-500">Sin asistencias registradas.</p>
            </div>

            <div v-else>
              <div v-if="resumenHistorial.length" class="border border-slate-200 rounded-xl overflow-hidden">
                <div class="max-h-72 overflow-y-auto">
                  <div v-for="r in resumenHistorial" :key="r.key" class="p-3 border-b border-slate-100 last:border-b-0">
                    <div class="flex items-center justify-between gap-3">
                      <div class="min-w-0">
                        <p class="text-sm font-semibold text-slate-800">{{ r.label }}</p>
                        <p class="text-xs text-slate-500 mt-0.5">Registros: {{ r.registros }} · Horas: {{ r.horas }}h</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <p v-else class="text-xs text-slate-500">Sin asistencias registradas.</p>
            </div>
          </div>
        </div>

        <div class="px-6 py-4 bg-slate-50 border-t border-slate-200 flex justify-end gap-3">
          <button type="button" @click="showModalVer = false" class="px-4 py-2 text-sm border rounded-lg hover:bg-slate-100">Cerrar</button>
        </div>
      </div>
    </div>

    <!-- Modal Crear -->
    <div v-if="showModalCrear" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/70 px-4 backdrop-blur-sm">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg overflow-hidden">
        <div class="bg-gradient-to-r from-blue-900 to-blue-800 px-6 py-5 text-white flex items-start justify-between">
          <div>
            <p class="text-blue-100 text-xs font-medium uppercase tracking-wider">Registro</p>
            <h3 class="text-xl font-bold mt-1">Nuevo Pasante</h3>
          </div>
          <button type="button" @click="showModalCrear = false" class="text-blue-100 hover:text-white">✕</button>
        </div>

        <form @submit.prevent="registrarPasante" class="p-6 space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">Nombres</label>
              <input v-model="formulario.nombres" required class="w-full border border-slate-300 rounded-lg p-3 text-sm" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">Apellidos</label>
              <input v-model="formulario.apellidos" required class="w-full border border-slate-300 rounded-lg p-3 text-sm" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">CI</label>
              <input v-model="formulario.carnet_identidad" required class="w-full border border-slate-300 rounded-lg p-3 text-sm" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">RU</label>
              <input v-model="formulario.ru" class="w-full border border-slate-300 rounded-lg p-3 text-sm" placeholder="Registro Universitario (opcional)" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">Email</label>
              <input v-model="formulario.email" type="email" required class="w-full border border-slate-300 rounded-lg p-3 text-sm" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">Programa/Proyecto <span class="text-red-500">*</span></label>
              <select v-model="formulario.programa_id" required class="w-full border border-slate-300 rounded-lg p-3 text-sm bg-white">
                <option value="">Selecciona un programa</option>
                <option v-for="programa in programas" :key="programa.id" :value="programa.id">
                  {{ programa.nombre }} {{ programa.gestion ? `(${programa.gestion})` : '' }}
                </option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-semibold text-slate-700 mb-1">Celular</label>
              <input v-model="formulario.celular" type="tel" required
                class="w-full border border-slate-300 rounded-lg p-2.5 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none text-sm"
                placeholder="Ej. 70123456" />
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-slate-700 mb-1">Unidad asignada</label>
              <input v-model="formulario.unidad_asignada" class="w-full border border-slate-300 rounded-lg p-3 text-sm" placeholder="Ej. Biblioteca / Secretaría / Unidad X" />
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-slate-700 mb-1">Contraseña</label>
              <input v-model="formulario.password" type="password" minlength="6" required class="w-full border border-slate-300 rounded-lg p-3 text-sm" />
            </div>
          </div>

          <div v-if="mensajeError" class="p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-700">{{ mensajeError }}</div>

          <div class="pt-4 border-t border-slate-200 flex justify-end gap-3">
            <button type="button" @click="showModalCrear = false" class="px-4 py-2 text-sm border rounded-lg">Cancelar</button>
            <button type="submit" :disabled="isSubmittingCrear" class="px-5 py-2 text-sm bg-blue-900 text-white rounded-lg disabled:opacity-50">
              {{ isSubmittingCrear ? 'Registrando...' : 'Registrar' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Editar -->
    <div v-if="showModalEditar" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/70 px-4 backdrop-blur-sm">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg overflow-hidden">
        <div class="bg-gradient-to-r from-blue-900 to-blue-800 px-6 py-5 text-white flex items-start justify-between">
          <div>
            <p class="text-blue-100 text-xs font-medium uppercase tracking-wider">Edición</p>
            <h3 class="text-xl font-bold mt-1">{{ pasanteSeleccionado?.nombres }} {{ pasanteSeleccionado?.apellidos }}</h3>
          </div>
          <button type="button" @click="showModalEditar = false" class="text-blue-100 hover:text-white">✕</button>
        </div>

        <form @submit.prevent="guardarEdicion" class="p-6 space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">Nombres</label>
              <input v-model="formEditar.nombres" class="w-full border border-slate-300 rounded-lg p-3 text-sm" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">Apellidos</label>
              <input v-model="formEditar.apellidos" class="w-full border border-slate-300 rounded-lg p-3 text-sm" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">CI</label>
              <input v-model="formEditar.carnet_identidad" class="w-full border border-slate-300 rounded-lg p-3 text-sm" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">RU</label>
              <input v-model="formEditar.ru" class="w-full border border-slate-300 rounded-lg p-3 text-sm" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">Email</label>
              <input v-model="formEditar.email" type="email" class="w-full border border-slate-300 rounded-lg p-3 text-sm" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">Celular</label>
              <input v-model="formEditar.celular" type="tel" class="w-full border border-slate-300 rounded-lg p-3 text-sm" />
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-slate-700 mb-1">Unidad asignada</label>
              <input v-model="formEditar.unidad_asignada" class="w-full border border-slate-300 rounded-lg p-3 text-sm" />
            </div>
          </div>

          <div v-if="mensajeErrorEditar" class="p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-700">{{ mensajeErrorEditar }}</div>

          <div class="pt-4 border-t border-slate-200 flex justify-end gap-3">
            <button type="button" @click="showModalEditar = false" class="px-4 py-2 text-sm border rounded-lg">Cancelar</button>
            <button type="submit" :disabled="isSubmittingEditar" class="px-5 py-2 text-sm bg-blue-900 text-white rounded-lg disabled:opacity-50">
              {{ isSubmittingEditar ? 'Guardando...' : 'Guardar' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Confirmar baja -->
    <div v-if="showModalBaja" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/70 px-4 backdrop-blur-sm">
      <div class="bg-white rounded-xl shadow-lg p-6 max-w-sm w-full text-center">
        <h4 class="text-lg font-semibold mb-2">{{ pasanteSeleccionado?.estado ? 'Dar de baja?' : 'Reactivar?' }}</h4>
        <p class="mb-4">{{ pasanteSeleccionado?.nombres }} {{ pasanteSeleccionado?.apellidos }}</p>
        <button type="button" @click="showModalBaja = false" class="px-4 py-2 mr-2 border rounded">Cancelar</button>
        <button type="button" @click="ejecutarCambioEstado" class="px-4 py-2 bg-red-600 text-white rounded">Confirmar</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'
import * as XLSX from 'xlsx'

type Usuario = {
  id: number
  nombres: string
  apellidos: string
  carnet_identidad: string
  ru?: string | null
  unidad_asignada?: string | null
  username: string
  email: string
  celular?: string | null
  rol_id: number
  carrera_id: number | null
  estado: boolean
  rol?: string | null
}

type Reporte = {
  id: number
  actividades_realizadas?: string | null
  estado: string
  comentarios_director?: string | null
  creado_en?: string | null
}

type Asistencia = {
  id: number
  pasante_id: number
  fecha: string
  hora_entrada: string
  hora_salida?: string | null
  horas_trabajadas?: number | null
  reporte?: Reporte | null
}

interface Programa {
  id: number
  nombre: string
  gestion?: string
  descripcion?: string
  estado: boolean
}

const router    = useRouter()
const authStore = useAuthStore()

const filterText  = ref('')
const filterState = ref<'all' | 'active' | 'inactive'>('all')

const isLoadingUsuarios = ref(false)
const usuarios          = ref<Usuario[]>([])

// ── PDF modal ─────────────────────────────────────────────────────────────────
const showModalPdf         = ref(false)
const tipoPdfSeleccionado  = ref<'semanal' | 'mensual'>('mensual')
const fechaPdfSeleccionada = ref('')
const mesPdfSeleccionado   = ref(new Date().getMonth() + 1)
const anioPdfSeleccionado  = ref(new Date().getFullYear())
const descargandoPdf       = ref(false)

const mesesNombres = [
  'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
  'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre',
]

const aniosDisponibles = computed(() => {
  const actual = new Date().getFullYear()
  return Array.from({ length: 5 }, (_, i) => actual - 2 + i)
})

const infoSemanaPdf = computed(() => {
  if (!fechaPdfSeleccionada.value) return ''
  const d      = new Date(fechaPdfSeleccionada.value + 'T12:00:00')
  const diaSem = (d.getDay() + 6) % 7
  const lunes  = new Date(d); lunes.setDate(d.getDate() - diaSem)
  const viernes = new Date(lunes); viernes.setDate(lunes.getDate() + 4)
  const fmt    = (dt: Date) => dt.toLocaleDateString('es-BO', { day: '2-digit', month: '2-digit', year: 'numeric' })
  return `Semana del ${fmt(lunes)} al ${fmt(viernes)}`
})

const puedeDescargarPdf = computed(() => {
  if (tipoPdfSeleccionado.value === 'semanal') return fechaPdfSeleccionada.value !== ''
  return !!(mesPdfSeleccionado.value && anioPdfSeleccionado.value)
})

// ── Modales ───────────────────────────────────────────────────────────────────
const showModalVer    = ref(false)
const showModalCrear  = ref(false)
const showModalEditar = ref(false)
const showModalBaja   = ref(false)

const tabVer              = ref<'detalles' | 'historial'>('detalles')
const pasanteSeleccionado = ref<Usuario | null>(null)

const isLoadingHistorial = ref(false)
const historial          = ref<Asistencia[]>([])
const errorHistorial     = ref('')

const filterHistorialYear  = ref<'all' | string>('all')
const filterHistorialMonth = ref<'all' | string>('all')
const historialVista       = ref<'detalle' | 'dia' | 'semana' | 'mes'>('detalle')

const isSubmittingCrear  = ref(false)
const mensajeError       = ref('')
const isSubmittingEditar = ref(false)
const mensajeErrorEditar = ref('')

const programas          = ref<Programa[]>([])
const isLoadingProgramas = ref(false)

const formulario = ref({
  nombres: '', apellidos: '', carnet_identidad: '', ru: '',
  unidad_asignada: '', email: '', celular: '', password: '', programa_id: '',
})

const formEditar = ref({
  nombres: '', apellidos: '', carnet_identidad: '', ru: '',
  unidad_asignada: '', email: '', celular: '',
})

const monthOptions = [
  { value: '01', label: 'Enero' },   { value: '02', label: 'Febrero' },
  { value: '03', label: 'Marzo' },   { value: '04', label: 'Abril' },
  { value: '05', label: 'Mayo' },    { value: '06', label: 'Junio' },
  { value: '07', label: 'Julio' },   { value: '08', label: 'Agosto' },
  { value: '09', label: 'Septiembre' }, { value: '10', label: 'Octubre' },
  { value: '11', label: 'Noviembre' }, { value: '12', label: 'Diciembre' },
] as const

// ── Helpers ───────────────────────────────────────────────────────────────────
function httpStatus(error: any): number | null { return error?.response?.status ?? null }
function httpDetail(error: any): string        { return error?.response?.data?.detail ?? error?.message ?? 'Error' }

function requireLoginIf401(error: any) {
  if (httpStatus(error) === 401) { authStore.logout(); router.push('/login'); return true }
  return false
}

function getIniciales(nombres?: string, apellidos?: string) {
  return `${(nombres || ' ')[0].toUpperCase()}${(apellidos || ' ')[0].toUpperCase()}`
}

function toDate(value?: string | null): Date | null {
  if (!value) return null
  const d = new Date(value)
  return Number.isNaN(d.getTime()) ? null : d
}

function formatFecha(value: string) {
  const d = toDate(value)
  if (!d) return String(value)
  return d.toLocaleDateString('es-BO', { year: 'numeric', month: '2-digit', day: '2-digit' })
}

function formatHora(value?: string | null) {
  const d = toDate(value ?? undefined)
  if (!d) return value ? String(value) : '—'
  return d.toLocaleTimeString('es-BO', { hour: '2-digit', minute: '2-digit' })
}

function reporteBadge(estado?: string) {
  const e = (estado || '').toUpperCase()
  if (e === 'APROBADO')  return 'bg-emerald-50 text-emerald-700 border-emerald-200'
  if (e === 'RECHAZADO') return 'bg-red-50 text-red-700 border-red-200'
  return 'bg-amber-50 text-amber-700 border-amber-200'
}

// ── Semana ISO ────────────────────────────────────────────────────────────────
function isoSemana(d: Date): number {
  const tmp = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()))
  tmp.setUTCDate(tmp.getUTCDate() + 4 - (tmp.getUTCDay() || 7))
  const inicio = new Date(Date.UTC(tmp.getUTCFullYear(), 0, 1))
  return Math.ceil((((tmp.getTime() - inicio.getTime()) / 86400000) + 1) / 7)
}

// ── Computeds ─────────────────────────────────────────────────────────────────
const usuariosFiltrados = computed(() => {
  const text = filterText.value.trim().toLowerCase()
  return usuarios.value
    .filter(u => (u.rol === 'PASANTE' || u.rol_id === 3))
    .filter(u => {
      if (filterState.value === 'active')   return !!u.estado
      if (filterState.value === 'inactive') return !u.estado
      return true
    })
    .filter(u => {
      if (!text) return true
      return `${u.nombres} ${u.apellidos} ${u.username} ${u.carnet_identidad} ${u.email}`.toLowerCase().includes(text)
    })
})

const historialYears = computed(() => {
  const years = new Set<number>()
  for (const a of historial.value) {
    const d = toDate(a.fecha); if (d) years.add(d.getFullYear())
  }
  return Array.from(years).sort((a, b) => b - a)
})

const historialFiltrado = computed(() =>
  historial.value.filter(a => {
    const d = toDate(a.fecha); if (!d) return true
    if (filterHistorialYear.value !== 'all') {
      const y = Number(filterHistorialYear.value)
      if (!Number.isNaN(y) && d.getFullYear() !== y) return false
    }
    if (filterHistorialMonth.value !== 'all') {
      if (String(d.getMonth() + 1).padStart(2, '0') !== filterHistorialMonth.value) return false
    }
    return true
  })
)

const totalHorasPasante   = computed(() => Math.round(historial.value.reduce((acc, a) => acc + (Number(a.horas_trabajadas) || 0), 0) * 100) / 100)
const totalHorasHistorial = computed(() => Math.round(historialFiltrado.value.reduce((acc, a) => acc + (Number(a.horas_trabajadas) || 0), 0) * 100) / 100)
const cumplioPasantia     = computed(() => totalHorasPasante.value >= 240)

function round2(v: number) { return Math.round(v * 100) / 100 }

function startOfWeekMonday(date: Date) {
  const d = new Date(date); d.setHours(0, 0, 0, 0)
  d.setDate(d.getDate() - ((d.getDay() + 6) % 7)); return d
}

function formatShortDate(date: Date) {
  return date.toLocaleDateString('es-BO', { year: 'numeric', month: '2-digit', day: '2-digit' })
}

const horasSemanaActual = computed(() => {
  const start = startOfWeekMonday(new Date()); const end = new Date(start); end.setDate(end.getDate() + 7)
  return round2(historial.value.reduce((acc, a) => {
    const d = toDate(a.fecha)
    return d && d >= start && d < end ? acc + (Number(a.horas_trabajadas) || 0) : acc
  }, 0))
})

const horasMesActual = computed(() => {
  const now = new Date(); const y = now.getFullYear(); const m = now.getMonth()
  return round2(historial.value.reduce((acc, a) => {
    const d = toDate(a.fecha)
    return d && d.getFullYear() === y && d.getMonth() === m ? acc + (Number(a.horas_trabajadas) || 0) : acc
  }, 0))
})

type ResumenRow = { key: string; label: string; fechaParam: string; horas: number; registros: number }

const resumenHistorial = computed<ResumenRow[]>(() => {
  if (historialVista.value === 'detalle') return []
  const map = new Map<string, ResumenRow>()
  for (const a of historialFiltrado.value) {
    const d = toDate(a.fecha); if (!d) continue
    let key = ''; let label = ''
    if (historialVista.value === 'dia') {
      key = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`
      label = formatShortDate(d)
    } else if (historialVista.value === 'mes') {
      key = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}`
      label = d.toLocaleDateString('es-BO', { year: 'numeric', month: 'long' })
    } else {
      const start = startOfWeekMonday(d); const end = new Date(start); end.setDate(end.getDate() + 6)
      key = `${start.getFullYear()}-${String(start.getMonth()+1).padStart(2,'0')}-${String(start.getDate()).padStart(2,'0')}`
      label = `Semana del ${formatShortDate(start)} al ${formatShortDate(end)}`
    }
    const row = map.get(key) || { key, label, fechaParam: '', horas: 0, registros: 0 }
    row.horas += Number(a.horas_trabajadas) || 0
    row.registros += 1
    if (!row.fechaParam) row.fechaParam = historialVista.value === 'mes' ? key + '-01' : key
    map.set(key, row)
  }
  const rows = Array.from(map.values())
  rows.sort((a, b) => b.key.localeCompare(a.key))
  for (const r of rows) r.horas = round2(r.horas)
  return rows
})

// ── Excel ─────────────────────────────────────────────────────────────────────
function descargarExcelHistorial() {
  const u     = pasanteSeleccionado.value
  const base  = u?.username || 'pasante'
  const fecha = new Date().toISOString().slice(0, 10)
  const wb    = XLSX.utils.book_new()

  if (historialVista.value === 'detalle') {
    const datos = historialFiltrado.value.map(a => ({
      'Fecha':            formatFecha(a.fecha),
      'Hora Entrada':     formatHora(a.hora_entrada),
      'Hora Salida':      a.hora_salida ? formatHora(a.hora_salida) : 'Pendiente',
      'Horas Trabajadas': a.horas_trabajadas || 0,
      'Estado Reporte':   a.reporte?.estado || 'Pendiente',
      'Actividades':      a.reporte?.actividades_realizadas || '—',
    }))
    const ws = XLSX.utils.json_to_sheet(datos)
    ws['!cols'] = [{ width: 15 }, { width: 15 }, { width: 15 }, { width: 18 }, { width: 18 }, { width: 50 }]
    XLSX.utils.book_append_sheet(wb, ws, 'Detalle de Asistencias')
    const resumen = [
      { 'Métrica': 'Total Registros',     'Valor': historialFiltrado.value.length },
      { 'Métrica': 'Total Horas',         'Valor': `${totalHorasHistorial.value}h` },
      { 'Métrica': 'Horas Semana Actual', 'Valor': `${horasSemanaActual.value}h` },
      { 'Métrica': 'Horas Mes Actual',    'Valor': `${horasMesActual.value}h` },
      { 'Métrica': 'Pasante',             'Valor': `${u?.nombres} ${u?.apellidos}` },
      { 'Métrica': 'Username',            'Valor': u?.username || '' },
      { 'Métrica': 'CI',                  'Valor': u?.carnet_identidad || '' },
    ]
    const wsR = XLSX.utils.json_to_sheet(resumen)
    wsR['!cols'] = [{ width: 25 }, { width: 30 }]
    XLSX.utils.book_append_sheet(wb, wsR, 'Resumen')
  } else {
    const datos = resumenHistorial.value.map(r => ({
      'Período': r.label, 'Total Registros': r.registros, 'Total Horas': `${r.horas}h`,
    }))
    const ws = XLSX.utils.json_to_sheet(datos)
    ws['!cols'] = [{ width: 30 }, { width: 20 }, { width: 18 }]
    XLSX.utils.book_append_sheet(wb, ws, 'Resumen por Períodos')
  }
  XLSX.writeFile(wb, `historial_${base}_${fecha}.xlsx`)
}

// ── Cargar datos ──────────────────────────────────────────────────────────────
async function cargarUsuarios() {
  isLoadingUsuarios.value = true
  try {
    const res = await api.get('/usuarios/listar', { timeout: 30000 })
    usuarios.value = Array.isArray(res.data) ? (res.data as Usuario[]) : []
  } catch (e: any) {
    if (requireLoginIf401(e)) return
    if (e.code === 'ECONNABORTED' || e.message?.includes('timeout')) {
      alert('⏰ La conexión está tardando demasiado. Intenta recargar la página.')
    }
  } finally {
    isLoadingUsuarios.value = false
  }
}

async function cargarHistorial(pasanteId: number) {
  isLoadingHistorial.value = true
  errorHistorial.value     = ''
  try {
    const res = await api.get('/asistencias/mis-asistencias', { params: { pasante_id: pasanteId } })
    historial.value = Array.isArray(res.data) ? (res.data as Asistencia[]) : []
  } catch (e: any) {
    if (requireLoginIf401(e)) return
    errorHistorial.value = httpDetail(e)
    historial.value      = []
  } finally {
    isLoadingHistorial.value = false
  }
}

function refrescarHistorial() {
  if (pasanteSeleccionado.value) cargarHistorial(pasanteSeleccionado.value.id)
}

async function cargarProgramas() {
  if (programas.value.length > 0) return
  isLoadingProgramas.value = true
  try {
    const { data } = await api.get('/programas/listar')
    programas.value = data
  } catch (e) {
    console.error('Error cargando programas:', e)
  } finally {
    isLoadingProgramas.value = false
  }
}

// ── Modales ───────────────────────────────────────────────────────────────────
function abrirModalVer(u: Usuario) {
  pasanteSeleccionado.value  = u
  tabVer.value               = 'detalles'
  filterHistorialYear.value  = 'all'
  filterHistorialMonth.value = 'all'
  historialVista.value       = 'detalle'
  historial.value            = []
  errorHistorial.value       = ''
  showModalVer.value         = true
  cargarHistorial(u.id)
}

function abrirModalCrear() {
  mensajeError.value   = ''
  formulario.value     = { nombres: '', apellidos: '', carnet_identidad: '', ru: '', unidad_asignada: '', email: '', celular: '', password: '', programa_id: '' }
  showModalCrear.value = true
  cargarProgramas()
}

function abrirModalEditar(u: Usuario) {
  mensajeErrorEditar.value  = ''
  pasanteSeleccionado.value = u
  formEditar.value = {
    nombres:          u.nombres          ?? '',
    apellidos:        u.apellidos        ?? '',
    carnet_identidad: u.carnet_identidad ?? '',
    ru:               u.ru               ?? '',
    unidad_asignada:  u.unidad_asignada  ?? '',
    email:            u.email            ?? '',
    celular:          (u.celular as any) ?? '',
  }
  showModalEditar.value = true
}

async function registrarPasante() {
  mensajeError.value  = ''
  const carreraId     = authStore.user?.carrera_id ?? null
  if (!carreraId) { mensajeError.value = 'Tu cuenta de encargado no tiene carrera asignada.'; return }

  isSubmittingCrear.value = true
  try {
    await api.post('/usuarios/registro', {
      nombres:          formulario.value.nombres,
      apellidos:        formulario.value.apellidos,
      carnet_identidad: formulario.value.carnet_identidad,
      ru:               formulario.value.ru?.trim() || null,
      unidad_asignada:  formulario.value.unidad_asignada?.trim() || null,
      email:            formulario.value.email,
      celular:          formulario.value.celular,
      password:         formulario.value.password,
      programa_id:      formulario.value.programa_id || null,
      rol_id:           3,
      carrera_id:       carreraId,
    })
    showModalCrear.value = false
    await cargarUsuarios()
  } catch (e: any) {
    if (requireLoginIf401(e)) return
    mensajeError.value = httpDetail(e)
  } finally {
    isSubmittingCrear.value = false
  }
}

async function guardarEdicion() {
  mensajeErrorEditar.value = ''
  if (!pasanteSeleccionado.value) return
  isSubmittingEditar.value = true
  try {
    const res = await api.put(`/usuarios/editar/${pasanteSeleccionado.value.id}`, {
      nombres:          formEditar.value.nombres,
      apellidos:        formEditar.value.apellidos,
      carnet_identidad: formEditar.value.carnet_identidad,
      ru:               formEditar.value.ru?.trim() || null,
      unidad_asignada:  formEditar.value.unidad_asignada?.trim() || null,
      email:            formEditar.value.email,
      celular:          formEditar.value.celular?.trim() || null,
    })
    showModalEditar.value     = false
    pasanteSeleccionado.value = res.data as Usuario
    await cargarUsuarios()
  } catch (e: any) {
    if (requireLoginIf401(e)) return
    mensajeErrorEditar.value = httpDetail(e)
  } finally {
    isSubmittingEditar.value = false
  }
}

function confirmarCambioEstado(u: Usuario) {
  pasanteSeleccionado.value = u; showModalBaja.value = true
}

async function ejecutarCambioEstado() {
  if (!pasanteSeleccionado.value) return
  const objetivo = pasanteSeleccionado.value
  try {
    if (objetivo.estado) {
      await api.delete(`/usuarios/desactivar/${objetivo.id}`)
    } else {
      await api.put(`/usuarios/editar/${objetivo.id}`, { estado: true })
    }
    showModalBaja.value = false
    await cargarUsuarios()
  } catch (e: any) {
    if (requireLoginIf401(e)) return
    console.error('Error cambiando estado:', e)
  }
}

// ── PDF pasante ───────────────────────────────────────────────────────────────
function descargarPdfPasante(pasante: Usuario) {
  pasanteSeleccionado.value  = pasante
  tipoPdfSeleccionado.value  = 'mensual'
  fechaPdfSeleccionada.value = ''
  mesPdfSeleccionado.value   = new Date().getMonth() + 1
  anioPdfSeleccionado.value  = new Date().getFullYear()
  showModalPdf.value         = true
}

async function ejecutarDescargaPdf() {
  if (!pasanteSeleccionado.value || !puedeDescargarPdf.value) return

  descargandoPdf.value = true
  try {
    const u      = pasanteSeleccionado.value
    let url      = ''
    let filename = ''

    if (tipoPdfSeleccionado.value === 'semanal') {
      const d      = new Date(fechaPdfSeleccionada.value + 'T12:00:00')
      const diaSem = (d.getDay() + 6) % 7
      const lunes  = new Date(d); lunes.setDate(d.getDate() - diaSem)
      const anio   = lunes.getFullYear()
      const semana = isoSemana(lunes)
      // ✅ Endpoint correcto para ENCARGADO/ADMIN — semanal
      url      = `/reportes/admin/pdf/semanal/${u.id}?anio=${anio}&semana=${semana}`
      filename = `reporte_semanal_${u.username}_${anio}_s${semana}.pdf`
    } else {
      // ✅ Endpoint correcto para ENCARGADO/ADMIN — mensual
      url      = `/reportes/admin/pdf/mensual/${u.id}?anio=${anioPdfSeleccionado.value}&mes=${mesPdfSeleccionado.value}`
      filename = `reporte_mensual_${u.username}_${anioPdfSeleccionado.value}_${String(mesPdfSeleccionado.value).padStart(2, '0')}.pdf`
    }

    const response = await api.get(url, { responseType: 'blob' })
    const blob     = new Blob([response.data], { type: 'application/pdf' })
    const blobUrl  = window.URL.createObjectURL(blob)
    const link     = document.createElement('a')
    link.href      = blobUrl
    link.setAttribute('download', filename)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(blobUrl)
    showModalPdf.value = false

  } catch (error: any) {
    console.error('Error descargando PDF:', error)
    alert(error.response?.data?.detail || 'Error al descargar el PDF. Intenta nuevamente.')
  } finally {
    descargandoPdf.value = false
  }
}

// ── Watchers ──────────────────────────────────────────────────────────────────
watch(tabVer, (tab) => {
  if (tab === 'historial' && pasanteSeleccionado.value && historial.value.length === 0 && !isLoadingHistorial.value) {
    cargarHistorial(pasanteSeleccionado.value.id)
  }
})

onMounted(cargarUsuarios)
</script>