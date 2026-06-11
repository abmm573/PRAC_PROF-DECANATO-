<template>
  <div class="min-h-screen bg-slate-100 font-sans pb-12">

    <header class="bg-blue-950 border-b-4 border-red-700 sticky top-0 z-50 shadow-2xl">
      <div class="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-5 pointer-events-none"></div>
      <div class="max-w-[96rem] mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div class="flex justify-between h-16 items-center">

          <div class="flex items-center gap-4">
            <div class="w-12 h-12 bg-gradient-to-br from-white to-slate-200 rounded-xl flex items-center justify-center text-blue-950 font-black text-xs shadow-lg border border-white/20 overflow-hidden">
              <img v-if="authStore.user?.carrera_logo_url" :src="resolveStaticUrl(authStore.user.carrera_logo_url)" alt="Logo carrera" class="w-full h-full object-contain p-1" />
              <span v-else><span class="text-red-700 text-lg mr-0.5 leading-none">U</span>MSA</span>
            </div>
            <div class="border-l-2 border-white/10 pl-4 py-1 hidden sm:block">
              <p class="text-[10px] text-red-400 font-black uppercase tracking-widest leading-none mb-1">Facultad de Cs. Sociales</p>
              <p class="text-sm font-extrabold text-white leading-none tracking-tight">
                Sistema de Pasantías <span class="text-blue-300/50 font-medium ml-1">| Pasante</span>
              </p>
            </div>
          </div>

          <!-- NAV -->
          <nav class="hidden md:flex items-center gap-1 bg-blue-900/50 p-1 rounded-xl border border-white/5">
            <button @click="seccion = 'dashboard'"
              :class="seccion === 'dashboard' ? 'bg-blue-600 text-white shadow-md' : 'text-blue-200 hover:bg-blue-800/50 hover:text-white'"
              class="px-6 py-2 rounded-lg text-sm font-bold transition-all">Dashboard</button>
            <button @click="seccion = 'reportes'"
              :class="seccion === 'reportes' ? 'bg-blue-600 text-white shadow-md' : 'text-blue-200 hover:bg-blue-800/50 hover:text-white'"
              class="px-6 py-2 rounded-lg text-sm font-bold transition-all">Reportes</button>
          </nav>

          <div class="flex items-center gap-4">
            <div class="hidden sm:flex flex-col items-end">
              <span class="text-white text-sm font-bold leading-tight">{{ authStore.user?.nombres }} {{ authStore.user?.apellidos }}</span>
              <span class="text-[10px] font-black text-red-400 uppercase tracking-widest">Pasante</span>
            </div>
            <button @click="router.push('/perfil')" title="Perfil"
              class="w-10 h-10 bg-gradient-to-br from-red-600 to-red-800 rounded-xl flex items-center justify-center text-white font-bold text-sm border border-red-500 hover:shadow-lg hover:shadow-red-600/30 transition-all">
              {{ iniciales }}
            </button>
            <div class="h-6 w-px bg-white/10 hidden sm:block"></div>
            <button @click="cerrarSesion" class="text-blue-300 hover:text-red-400 transition-colors" title="Cerrar Sesión">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
      <!-- Móvil -->
      <div class="md:hidden border-t border-white/10 bg-blue-900/50 px-4 py-2 flex gap-2">
        <button @click="seccion = 'dashboard'" :class="seccion === 'dashboard' ? 'bg-blue-600 text-white' : 'text-blue-200'" class="flex-1 px-3 py-2 rounded-lg text-xs font-bold transition-all">Dashboard</button>
        <button @click="seccion = 'reportes'" :class="seccion === 'reportes' ? 'bg-blue-600 text-white' : 'text-blue-200'" class="flex-1 px-3 py-2 rounded-lg text-xs font-bold transition-all">Reportes</button>
      </div>
    </header>

    <main class="max-w-[96rem] mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">

      <!-- ===== DASHBOARD ===== -->
      <template v-if="seccion === 'dashboard'">

        <div v-if="alerta20h" class="bg-gradient-to-r from-amber-500 to-orange-500 rounded-2xl p-6 text-white flex items-center gap-4 shadow-lg animate-pulse">
          <div class="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center flex-shrink-0">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
          </div>
          <div>
            <p class="text-xs font-black uppercase tracking-widest text-amber-100">¡Atención, ya casi terminas!</p>
            <h3 class="mt-1 text-xl font-black">Faltan menos de {{ progreso.horas_restantes }} horas para terminar tu pasantía.</h3>
            <p class="text-sm text-amber-50 mt-1 font-medium">Asegúrate de que todos tus reportes estén validados por tu Encargado y Aprobados por el Administrador.</p>
          </div>
        </div>

        <!-- Resumen Semanal (solo los viernes) -->
        <div v-if="esViernes && historial.length > 0" class="bg-gradient-to-r from-emerald-600 to-teal-600 rounded-2xl p-8 text-white shadow-lg relative overflow-hidden border border-emerald-700">
          <div class="absolute top-0 right-0 w-[20rem] h-[20rem] bg-white/10 rounded-full blur-[60px] -translate-y-1/2 translate-x-1/3 pointer-events-none"></div>
          <div class="relative z-10">
            <div class="flex items-center gap-3 mb-6">
              <div class="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"/>
                </svg>
              </div>
              <div>
                <p class="text-xs font-black uppercase tracking-widest text-emerald-100">Resumen Semanal</p>
                <h3 class="text-2xl font-bold">¡Feliz viernes! 🎉</h3>
                <p class="text-emerald-50 text-sm mt-1">Tu progreso esta semana</p>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div class="bg-white/10 backdrop-blur-sm rounded-xl p-4 border border-white/20">
                <div class="flex items-center gap-2 mb-2">
                  <svg class="w-5 h-5 text-emerald-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                  </svg>
                  <span class="text-sm font-bold text-emerald-100">Días trabajados</span>
                </div>
                <p class="text-3xl font-black text-white">{{ diasTrabajadosSemana }}</p>
                <p class="text-xs text-emerald-200 mt-1">de esta semana</p>
              </div>

              <div class="bg-white/10 backdrop-blur-sm rounded-xl p-4 border border-white/20">
                <div class="flex items-center gap-2 mb-2">
                  <svg class="w-5 h-5 text-emerald-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                  <span class="text-sm font-bold text-emerald-100">Horas totales</span>
                </div>
                <p class="text-3xl font-black text-white">{{ totalHorasSemana }}h</p>
                <p class="text-xs text-emerald-200 mt-1">acumuladas</p>
              </div>

              <div class="bg-white/10 backdrop-blur-sm rounded-xl p-4 border border-white/20">
                <div class="flex items-center gap-2 mb-2">
                  <svg class="w-5 h-5 text-emerald-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                  <span class="text-sm font-bold text-emerald-100">Reportes</span>
                </div>
                <p class="text-3xl font-black text-white">{{ reportesAprobadosSemana }}</p>
                <p class="text-xs text-emerald-200 mt-1">aprobados esta semana</p>
              </div>

              <div class="bg-white/10 backdrop-blur-sm rounded-xl p-4 border border-white/20">
                <div class="flex items-center gap-2 mb-2">
                  <svg class="w-5 h-5 text-emerald-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                  </svg>
                  <span class="text-sm font-bold text-emerald-100">Promedio diario</span>
                </div>
                <p class="text-3xl font-black text-white">{{ promedioHorasDiarias }}h</p>
                <p class="text-xs text-emerald-200 mt-1">por día trabajado</p>
              </div>
            </div>

            <!-- Actividades destacadas de la semana -->
            <div class="mt-6 bg-white/10 backdrop-blur-sm rounded-xl p-4 border border-white/20">
              <h4 class="text-sm font-bold text-emerald-100 mb-3 flex items-center gap-2">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
                </svg>
                Actividades destacadas
              </h4>
              <div class="space-y-2 max-h-32 overflow-y-auto">
                <div v-for="actividad in actividadesDestacadasSemana" :key="actividad.id" class="text-sm text-emerald-50 bg-white/5 rounded-lg p-2 border border-white/10">
                  <span class="text-xs font-bold text-emerald-200">{{ formatFecha(actividad.fecha) }}:</span>
                  <p class="text-xs mt-1 line-clamp-2">{{ actividad.actividades_realizadas }}</p>
                </div>
                <div v-if="actividadesDestacadasSemana.length === 0" class="text-xs text-emerald-200 italic">
                  No hay actividades registradas esta semana
                </div>
              </div>
            </div>

            <!-- Botón para crear reporte semanal -->
            <div class="mt-6 flex justify-center">
              <button @click="crearReporteSemanal" class="inline-flex items-center gap-3 bg-white text-emerald-700 hover:bg-emerald-50 px-6 py-3 rounded-xl font-bold text-sm transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 border-2 border-emerald-300">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                </svg>
                Crear Reporte Semanal
              </button>
            </div>
          </div>
        </div>

        <!-- Banner -->
        <div class="bg-gradient-to-r from-blue-950 to-blue-900 rounded-2xl p-8 text-white shadow-lg relative overflow-hidden border border-blue-900">
          <div class="absolute top-0 right-0 w-48 h-48 bg-red-600/10 rounded-full blur-[60px] -translate-y-1/2 translate-x-1/3 pointer-events-none"></div>
          <div class="absolute bottom-0 left-0 w-32 h-32 bg-blue-500/10 rounded-full blur-[40px] translate-y-1/3 -translate-x-1/4 pointer-events-none"></div>
          <div class="relative z-10 flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
            <div>
              <p class="text-blue-200 text-sm font-medium uppercase tracking-wider mb-1">Bienvenido</p>
              <h1 class="text-3xl font-bold mb-2">{{ authStore.user?.nombres }} {{ authStore.user?.apellidos }}</h1>
              <p class="text-blue-100 text-sm">Panel de control — Pasante</p>
              <p v-if="authStore.user?.proyecto_nombre" class="mt-2 inline-flex items-center px-2.5 py-1 rounded-md text-xs font-bold bg-white/10 border border-white/20">
                <svg class="w-3.5 h-3.5 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>
                Proyecto: {{ authStore.user?.proyecto_nombre }}
              </p>
            </div>
            <div class="flex items-center gap-4">
              <div class="text-center px-6 py-3 bg-white/10 rounded-xl backdrop-blur-sm border border-white/20">
                <p class="text-3xl font-bold">{{ stats.totalDias }}</p>
                <p class="text-xs text-blue-200 uppercase tracking-wider">Dias</p>
              </div>
              <div class="text-center px-6 py-3 bg-white/10 rounded-xl backdrop-blur-sm border border-white/20">
                <p class="text-3xl font-bold">{{ formatHorasLegibles(stats.totalHoras) }}</p>
                <p class="text-xs text-blue-200 uppercase tracking-wider">Horas</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Métricas -->
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-6">
          <div class="bg-white rounded-xl border border-slate-200 p-6 hover:shadow-lg hover:border-blue-200 transition-all">
            <p class="text-xs font-bold text-slate-500 uppercase">Reportes pendientes</p>
            <p class="mt-2 text-3xl font-bold text-slate-800">{{ stats.reportesPendientes }}</p>
          </div>
          <div class="bg-white rounded-xl border border-slate-200 p-6 hover:shadow-lg hover:border-emerald-200 transition-all">
            <p class="text-xs font-bold text-slate-500 uppercase">Reportes aprobados</p>
            <p class="mt-2 text-3xl font-bold text-emerald-600">{{ stats.reportesAprobados }}</p>
          </div>
          <div class="bg-white rounded-xl border border-slate-200 p-6 hover:shadow-lg hover:border-blue-200 transition-all">
            <p class="text-xs font-bold text-slate-500 uppercase">Porcentaje aprobado</p>
            <p class="mt-2 text-3xl font-bold text-slate-800">{{ stats.pctAprobados }}%</p>
          </div>
          <div class="bg-white rounded-xl border border-slate-200 p-6 hover:shadow-lg hover:border-blue-200 transition-all">
            <p class="text-xs font-bold text-slate-500 uppercase">Total con reporte</p>
            <p class="mt-2 text-3xl font-bold text-slate-800">{{ stats.totalConReporte }}</p>
          </div>
        </div>

        <!-- Horas -->
        <div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
          <div class="px-6 py-4 border-b border-slate-100 bg-slate-50/50">
            <h2 class="text-lg font-semibold text-slate-800">Horas</h2>
            <p class="text-sm text-slate-500">Separacion de horas registradas y validadas</p>
          </div>
          <div class="p-6 grid grid-cols-1 md:grid-cols-4 gap-4">
            <div class="p-4 rounded-xl border border-slate-200 bg-slate-50">
              <p class="text-xs font-bold text-slate-500 uppercase">Meta</p>
              <p class="mt-1 text-2xl font-black text-slate-800">{{ formatHorasLegibles(progreso.meta_horas) }}</p>
            </div>
            <div class="p-4 rounded-xl border border-slate-200 bg-slate-50">
              <p class="text-xs font-bold text-slate-500 uppercase">Total Registrado</p>
              <p class="mt-1 text-2xl font-black text-slate-800">{{ formatHorasLegibles(progreso.total_horas) }}</p>
            </div>
            <div class="p-4 rounded-xl border border-blue-200 bg-blue-50 relative overflow-hidden">
              <div class="absolute top-0 right-0 bg-blue-200 text-blue-800 text-[9px] font-black px-2 py-0.5 rounded-bl-lg">POR ENCARGADO</div>
              <p class="text-xs font-bold text-blue-700 uppercase">Horas Verificadas</p>
              <p class="mt-1 text-2xl font-black text-blue-900">{{ formatHorasLegibles(progreso.horas_verificadas) }}</p>
            </div>
            <div class="p-4 rounded-xl border border-emerald-200 bg-emerald-50 relative overflow-hidden">
              <div class="absolute top-0 right-0 bg-emerald-200 text-emerald-800 text-[9px] font-black px-2 py-0.5 rounded-bl-lg">POR ADMIN</div>
              <p class="text-xs font-bold text-emerald-700 uppercase">Horas Validadas</p>
              <p class="mt-1 text-2xl font-black text-emerald-900">{{ formatHorasLegibles(progreso.horas_validadas) }}</p>
            </div>
          </div>
        </div>

        <!-- Historial con doble estado -->
        <div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
          <div class="px-6 py-4 border-b border-slate-100 bg-slate-50/50 flex items-center justify-between">
            <div>
              <h2 class="text-lg font-semibold text-slate-800">Historial de Asistencias</h2>
              <p class="text-sm text-slate-500">Estado por Encargado y por Administrador</p>
            </div>
            <button @click="cargarHistorial" class="p-2 text-slate-400 hover:text-blue-700 hover:bg-blue-50 rounded-lg transition-all" title="Actualizar">
              <svg class="w-5 h-5" :class="isLoading ? 'animate-spin' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
              </svg>
            </button>
          </div>

          <div v-if="isLoading" class="py-16 text-center text-slate-400">
            <svg class="animate-spin w-8 h-8 mx-auto mb-3 text-blue-400" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
            </svg>
            <p class="text-sm">Cargando historial...</p>
          </div>
          <div v-else-if="historial.length === 0" class="py-16 text-center text-slate-400">
            <p class="text-sm">No hay registros aun.</p>
          </div>
          <div v-else class="bg-white rounded-2xl shadow-lg border border-slate-200 overflow-hidden">
            <div class="overflow-x-auto">
              <table class="min-w-full">
                <thead class="bg-gradient-to-r from-slate-50 to-slate-100 border-b-2 border-slate-300">
                  <tr>
                    <th class="px-4 py-4 text-left text-xs font-bold text-slate-700 uppercase tracking-wider border-r border-slate-200">Fecha</th>
                    <th class="px-4 py-4 text-left text-xs font-bold text-slate-700 uppercase tracking-wider border-r border-slate-200">Entrada</th>
                    <th class="px-4 py-4 text-left text-xs font-bold text-slate-700 uppercase tracking-wider border-r border-slate-200">Salida</th>
                    <th class="px-4 py-4 text-left text-xs font-bold text-slate-700 uppercase tracking-wider border-r border-slate-200">Horas</th>
                    <th class="px-4 py-4 text-left text-xs font-bold text-blue-700 uppercase tracking-wider bg-blue-50 border-r-2 border-blue-300">Estado Encargado</th>
                    <th class="px-4 py-4 text-left text-xs font-bold text-blue-600 uppercase tracking-wider bg-blue-50/50 border-r border-blue-200">Comentario Encargado</th>
                    <th class="px-4 py-4 text-left text-xs font-bold text-purple-700 uppercase tracking-wider bg-purple-50/50 border-r border-purple-200">Comentario Admin</th>
                    <th class="px-4 py-4 text-left text-xs font-bold text-emerald-700 uppercase tracking-wider bg-emerald-50 border-r-2 border-emerald-300">Estado Admin</th>
                    <th class="px-4 py-4 text-center text-xs font-bold text-slate-700 uppercase tracking-wider">Acción</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100">
                  <tr v-for="item in historial" :key="item.id" class="hover:bg-slate-50/70 transition-colors">
                    <td class="px-4 py-4 text-sm font-medium text-slate-900 text-center whitespace-nowrap border-r border-slate-100">{{ formatFecha(item.fecha) }}</td>
                    <td class="px-4 py-4 text-sm text-slate-700 font-mono text-center whitespace-nowrap border-r border-slate-100">{{ formatHora(item.hora_entrada) }}</td>
                    <td class="px-4 py-4 text-sm text-slate-700 font-mono text-center whitespace-nowrap border-r border-slate-100">{{ formatHora(item.hora_salida) }}</td>
                    <td class="px-4 py-4 text-sm font-bold text-slate-900 text-center whitespace-nowrap border-r border-slate-100">{{ item.horas_trabajadas ?? '—' }}</td>
                    <td class="px-4 py-4 bg-blue-50/30 border-r-2 border-blue-200 text-center whitespace-nowrap">
                      <span class="inline-flex items-center px-3 py-1.5 rounded-full text-xs font-bold uppercase tracking-wider shadow-sm" :class="badgeEncargado(item.reporte?.estado_encargado)">
                        {{ item.reporte?.estado_encargado || 'PENDIENTE' }}
                      </span>
                    </td>
                    <td class="px-4 py-4 bg-blue-50/20 max-w-[200px] border-r border-blue-100">
                      <p class="text-xs text-slate-600 leading-relaxed text-center" :title="extraerComentarioEncargado(item.reporte?.comentarios_director)">
                        <span v-if="extraerComentarioEncargado(item.reporte?.comentarios_director)" class="line-clamp-2">
                          {{ extraerComentarioEncargado(item.reporte?.comentarios_director) }}
                        </span>
                        <span v-else class="text-slate-400 italic">Sin comentario</span>
                      </p>
                    </td>
                    <td class="px-4 py-4 bg-purple-50/20 max-w-[200px] border-r border-purple-100">
                      <p class="text-xs text-slate-600 leading-relaxed text-center" :title="extraerComentarioAdmin(item.reporte?.comentarios_director)">
                        <span v-if="extraerComentarioAdmin(item.reporte?.comentarios_director)" class="line-clamp-2">
                          {{ extraerComentarioAdmin(item.reporte?.comentarios_director) }}
                        </span>
                        <span v-else class="text-slate-400 italic">Sin comentario</span>
                      </p>
                    </td>
                    <td class="px-4 py-4 bg-emerald-50/30 border-r-2 border-emerald-200 text-center whitespace-nowrap">
                      <span class="inline-flex items-center px-3 py-1.5 rounded-full text-xs font-bold uppercase tracking-wider shadow-sm" :class="badgeAdmin(item.reporte?.estado_admin)">
                        {{ item.reporte?.estado_admin || '—' }}
                      </span>
                    </td>
                    <td class="px-4 py-4 text-center whitespace-nowrap">
                      <button @click="abrirModalReporte(item)" 
                        :disabled="item.reporte && (item.reporte.estado_encargado === 'VERIFICADO' || item.reporte.estado_encargado === 'RECTIFICADO')"
                        :class="(item.reporte && (item.reporte.estado_encargado === 'VERIFICADO' || item.reporte.estado_encargado === 'RECTIFICADO'))
                          ? 'bg-slate-100 text-slate-400 cursor-not-allowed border-slate-300 shadow-none' 
                          : 'bg-gradient-to-r from-blue-600 to-blue-800 text-white hover:from-blue-500 hover:to-blue-700 transition-all duration-200 shadow-md hover:shadow-lg transform hover:-translate-y-0.5'"
                        class="inline-flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-semibold border">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                        </svg>
                        {{ (item.reporte && (item.reporte.estado_encargado === 'VERIFICADO' || item.reporte.estado_encargado === 'RECTIFICADO')) ? 'Verificado' : 'Reporte' }}
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

      </template>

      <!-- ===== REPORTES PDF ===== -->
      <template v-if="seccion === 'reportes'">

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
              <div>
                <label class="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-2">Tipo de Reporte</label>
                <div class="flex rounded-xl overflow-hidden border border-slate-300">
                  <button @click="tipoPdf = 'semanal'" :class="tipoPdf === 'semanal' ? 'bg-blue-950 text-white' : 'bg-white text-slate-600 hover:bg-slate-50'" class="px-4 py-3 text-sm font-bold transition-all flex-1">Semanal</button>
                  <button @click="tipoPdf = 'mensual'" :class="tipoPdf === 'mensual' ? 'bg-blue-950 text-white' : 'bg-white text-slate-600 hover:bg-slate-50'" class="px-4 py-3 text-sm font-bold transition-all flex-1">Mensual</button>
                </div>
              </div>
              <div v-if="tipoPdf === 'semanal'">
                <label class="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-2">Seleccionar Semana</label>
                <input type="date" v-model="pdfFechaSemana" class="w-full border border-slate-300 rounded-xl px-3 py-3 text-sm outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all font-bold bg-slate-50 focus:bg-white"/>
                <div v-if="infoSemana" class="mt-2 bg-blue-50 border border-blue-200 rounded-xl p-3">
                  <p class="text-sm text-blue-800 font-bold">{{ infoSemana }}</p>
                </div>
              </div>
              <div v-if="tipoPdf === 'mensual'">
                <label class="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-2">Mes y Año</label>
                <div class="grid grid-cols-2 gap-3">
                  <select v-model="pdfMes" class="w-full border border-slate-300 rounded-xl px-3 py-3 text-sm outline-none focus:ring-2 focus:ring-blue-500 font-bold bg-slate-50 focus:bg-white transition-all">
                    <option v-for="(nombre, idx) in mesesNombres" :key="idx + 1" :value="idx + 1">{{ nombre }}</option>
                  </select>
                  <select v-model="pdfAnio" class="w-full border border-slate-300 rounded-xl px-3 py-3 text-sm outline-none focus:ring-2 focus:ring-blue-500 font-bold bg-slate-50 focus:bg-white transition-all">
                    <option v-for="y in aniosDisponibles" :key="y" :value="y">{{ y }}</option>
                  </select>
                </div>
                <div v-if="pdfMes && pdfAnio" class="mt-2 bg-blue-50 border border-blue-200 rounded-xl p-3">
                  <p class="text-sm text-blue-800 font-bold">{{ mesesNombres[pdfMes - 1] }} {{ pdfAnio }}</p>
                </div>
              </div>
              <div class="flex items-end">
                <button @click="cargarVistaPrevia" :disabled="cargandoPdf || !puedeCargar"
                  class="w-full px-6 py-3 bg-gradient-to-r from-blue-800 to-blue-950 text-white rounded-xl text-sm font-black uppercase tracking-widest hover:from-blue-700 hover:to-blue-900 disabled:opacity-50 shadow-lg shadow-blue-900/30 transition-all flex items-center justify-center gap-2">
                  <svg v-if="cargandoPdf" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
                  </svg>
                  <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                  </svg>
                  {{ cargandoPdf ? 'Buscando...' : 'Buscar' }}
                </button>
              </div>
            </div>
            <p v-if="errorVistaPrevia" class="mt-4 text-red-600 text-sm bg-red-50 border border-red-200 p-3 rounded-xl font-bold">{{ errorVistaPrevia }}</p>
            <p v-if="errorDescarga" class="mt-4 text-red-600 text-sm bg-red-50 border border-red-200 p-3 rounded-xl font-bold">{{ errorDescarga }}</p>
          </div>
        </div>

        <!-- Tabla resultados PDF -->
        <div v-if="datosVistaPrevia.length > 0" class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
          <div class="px-8 py-5 bg-gradient-to-r from-blue-950 to-blue-900 border-b-4 border-red-600">
            <h3 class="text-lg font-black text-white uppercase tracking-widest">Reporte {{ tipoPdf === 'semanal' ? 'Semanal' : 'Mensual' }}</h3>
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
                      <span :class="badgeEstadoPdf(row.estado_encargado)" class="px-2.5 py-1 rounded-full text-[10px] font-black uppercase tracking-widest">{{ row.estado_encargado }}</span>
                    </td>
                    <td class="px-4 py-3 whitespace-nowrap">
                      <span :class="badgeEstadoPdf(row.estado_admin)" class="px-2.5 py-1 rounded-full text-[10px] font-black uppercase tracking-widest">{{ row.estado_admin }}</span>
                    </td>
                    <td class="px-4 py-3 text-slate-600 max-w-xs truncate" :title="row.comentario">{{ row.comentario || '—' }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div class="mt-6 bg-slate-50 border border-slate-200 rounded-2xl p-5">
              <h4 class="font-black text-blue-950 mb-4 uppercase tracking-widest text-sm">Resumen del Período</h4>
              <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                <div class="bg-white rounded-xl p-4 border border-slate-200 text-center shadow-sm">
                  <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Total Días</p>
                  <p class="text-2xl font-black text-blue-950">{{ datosVistaPrevia.length }}</p>
                </div>
                <div class="bg-white rounded-xl p-4 border border-slate-200 text-center shadow-sm">
                  <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Total Horas</p>
                  <p class="text-2xl font-black text-blue-950">{{ totalHorasVistaPrevia.toFixed(2) }}h</p>
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
                <button @click="generarPdfDesdeVistaPrevia" :disabled="descargando"
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

        <div v-else-if="busquedaRealizada && !cargandoPdf" class="bg-white border border-slate-200 rounded-2xl shadow-sm p-12 text-center">
          <div class="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-4 border border-slate-200">
            <svg class="w-8 h-8 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414A1 1 0 0119 9.414V19a2 2 0 01-2 2z"/>
            </svg>
          </div>
          <p class="text-slate-600 font-bold">No hay asistencias para este período</p>
          <p class="text-slate-400 text-sm mt-1">Selecciona otro período o registra tus asistencias primero</p>
        </div>

      </template>

    </main>

    <!-- MODAL REPORTE -->
    <transition name="modal">
      <div v-if="showModalReporte" class="fixed inset-0 z-[999] flex items-center justify-center px-4">
        <div class="absolute inset-0 bg-blue-950/70 backdrop-blur-sm" @click="showModalReporte = false"></div>
        <div class="relative bg-white w-full max-w-xl rounded-2xl shadow-2xl border border-blue-100 overflow-hidden">
          <div class="px-6 py-5 bg-gradient-to-r from-blue-950 to-blue-900 border-b-4 border-red-600">
            <h3 class="text-lg font-black text-white uppercase tracking-widest">Reporte del Día</h3>
            <p class="text-blue-200 text-sm mt-0.5">{{ asistenciaSeleccionada ? formatFecha(asistenciaSeleccionada.fecha) : '' }}</p>
          </div>
          <div class="p-6 space-y-3">
            <label class="block text-[10px] font-black text-slate-400 uppercase tracking-widest">Actividades realizadas</label>
            <textarea v-model="actividadesModal" rows="6" placeholder="Describe las tareas que realizaste..."
              class="w-full border border-slate-300 rounded-xl p-3.5 text-sm resize-none outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-slate-50 focus:bg-white transition-all"/>
            <p v-if="errorModal" class="text-red-600 text-sm bg-red-50 border border-red-200 p-3 rounded-xl font-medium">{{ errorModal }}</p>
          </div>
          <div class="px-6 pb-6 flex gap-3">
            <button @click="showModalReporte = false" class="flex-1 py-2.5 border border-slate-300 text-slate-600 rounded-xl text-sm font-bold hover:bg-slate-50 transition-colors">Cancelar</button>
            <button @click="guardarReporteModal" :disabled="isSubmittingModal || !actividadesModal.trim()"
              class="flex-1 py-2.5 bg-gradient-to-r from-blue-800 to-blue-950 text-white rounded-xl text-sm font-black hover:from-blue-700 hover:to-blue-900 transition-all disabled:opacity-50 shadow-lg shadow-blue-900/30">
              {{ isSubmittingModal ? 'Guardando...' : 'Guardar' }}
            </button>
          </div>
        </div>
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api, { API_ORIGIN } from '../services/api'
import { formatFecha, formatHora, formatHorasLegibles } from '../utils/formatters'

const router    = useRouter()
const authStore = useAuthStore()

const resolveStaticUrl = (url) => {
  if (!url) return null
  const s = String(url)
  if (s.startsWith('http://') || s.startsWith('https://')) return s
  if (s.startsWith('/')) return `${API_ORIGIN}${s}`
  return s
}

const seccion = ref('dashboard')

// ---- HISTORIAL ----
const historial  = ref([])
const isLoading  = ref(true)
const progreso   = ref({ meta_horas: 240, total_horas: 0, horas_verificadas: 0, horas_validadas: 0, horas_restantes: 240 })
const showModalReporte       = ref(false)
const asistenciaSeleccionada = ref(null)
const actividadesModal       = ref('')
const isSubmittingModal      = ref(false)
const errorModal             = ref('')

// ---- PDF ----
const tipoPdf               = ref('semanal')
const pdfFechaSemana        = ref('')
const pdfMes                = ref(new Date().getMonth() + 1)
const pdfAnio               = ref(new Date().getFullYear())
const datosVistaPrevia      = ref([])
const totalHorasVistaPrevia = ref(0)
const contadorEstados       = ref({})
const descargando           = ref(false)
const cargandoPdf           = ref(false)
const busquedaRealizada     = ref(false)
const errorDescarga         = ref('')
const errorVistaPrevia      = ref('')

watch(tipoPdf, () => {
  datosVistaPrevia.value = []
  busquedaRealizada.value = false
  errorVistaPrevia.value = ''
  pdfFechaSemana.value = ''
})

watch([pdfMes, pdfAnio], () => {
  datosVistaPrevia.value = []
  busquedaRealizada.value = false
  errorVistaPrevia.value = ''
})

watch(pdfFechaSemana, () => {
  datosVistaPrevia.value = []
  busquedaRealizada.value = false
  errorVistaPrevia.value = ''
})

const iniciales = computed(() => {
  const n = authStore.user?.nombres?.[0] ?? ''
  const a = authStore.user?.apellidos?.[0] ?? ''
  return (n + a).toUpperCase()
})

const stats = computed(() => {
  const conReporte = historial.value.filter(i => i.reporte).length
  const aprobados  = historial.value.filter(i => (i.reporte?.estado_admin || '').toUpperCase() === 'APROBADO').length
  const pendientes = historial.value.filter(i => !i.reporte?.estado_encargado).length
  const totalHoras = Math.round(historial.value.reduce((a, i) => a + (parseFloat(i.horas_trabajadas) || 0), 0) * 100) / 100
  return { totalDias: historial.value.length, totalHoras, totalConReporte: conReporte, reportesPendientes: pendientes, reportesAprobados: aprobados, pctAprobados: conReporte > 0 ? Math.round((aprobados / conReporte) * 100) : 0 }
})

const alerta20h = computed(() => Number(progreso.value?.horas_restantes ?? 0) > 0 && Number(progreso.value?.horas_restantes ?? 0) <= 20)

// ---- Resumen Semanal (solo los viernes) ----
const esViernes = computed(() => {
  const hoy = new Date()
  return hoy.getDay() === 5 // 5 = viernes
})

const inicioSemana = computed(() => {
  const hoy = new Date()
  const diaSemana = hoy.getDay()
  const diferencia = diaSemana === 0 ? -6 : 1 - diaSemana // Ajustar para que lunes sea 1
  const lunes = new Date(hoy)
  lunes.setDate(hoy.getDate() + diferencia)
  return lunes
})

const finSemana = computed(() => {
  const domingo = new Date(inicioSemana.value)
  domingo.setDate(inicioSemana.value.getDate() + 6)
  return domingo
})

const historialSemana = computed(() => {
  return historial.value.filter(item => {
    const fechaItem = new Date(item.fecha)
    return fechaItem >= inicioSemana.value && fechaItem <= finSemana.value
  })
})

const diasTrabajadosSemana = computed(() => {
  return historialSemana.value.filter(item => item.horas_trabajadas && item.horas_trabajadas > 0).length
})

const totalHorasSemana = computed(() => {
  return historialSemana.value.reduce((total, item) => {
    return total + (Number(item.horas_trabajadas) || 0)
  }, 0)
})

const reportesAprobadosSemana = computed(() => {
  return historialSemana.value.filter(item => 
    item.reporte && (item.reporte.estado_admin || '').toUpperCase() === 'APROBADO'
  ).length
})

const promedioHorasDiarias = computed(() => {
  if (diasTrabajadosSemana.value === 0) return 0
  return (totalHorasSemana.value / diasTrabajadosSemana.value).toFixed(1)
})

const actividadesDestacadasSemana = computed(() => {
  return historialSemana.value
    .filter(item => item.reporte && item.reporte.actividades_realizadas)
    .slice(-5) // Últimas 5 actividades de la semana
    .map(item => ({
      id: item.id,
      fecha: item.fecha,
      actividades_realizadas: item.reporte.actividades_realizadas
    }))
})

const badgeEncargado = (estado) => {
  const e = String(estado || '').toUpperCase()
  if (e === 'VERIFICADO')  return 'bg-blue-50 text-blue-700 border-blue-200'
  if (e === 'RECTIFICADO') return 'bg-purple-50 text-purple-700 border-purple-200'
  if (e === 'RECHAZADO')   return 'bg-rose-50 text-rose-700 border-rose-200'
  return 'bg-amber-50 text-amber-700 border-amber-200'
}

const badgeAdmin = (estado) => {
  const e = String(estado || '').toUpperCase()
  if (e === 'APROBADO')  return 'bg-emerald-50 text-emerald-700 border-emerald-200'
  if (e === 'RECHAZADO') return 'bg-rose-50 text-rose-700 border-rose-200'
  return 'bg-slate-50 text-slate-400 border-slate-200'
}

const extraerComentarioEncargado = (comentarios) => {
  if (!comentarios) return ''
  
  // Depuración - mostrar en consola qué se recibe
  console.log('Comentarios recibidos:', JSON.stringify(comentarios))
  
  // Dividir por diferentes separadores posibles
  const separadores = ['\n\n', '\n', ' | ', ' || ']
  let lineas = [comentarios]
  
  // Intentar dividir por cada separador
  for (const sep of separadores) {
    if (comentarios.includes(sep)) {
      lineas = comentarios.split(sep)
      break
    }
  }
  
  console.log('Líneas divididas:', lineas)
  
  // Buscar comentario del encargado
  const comentarioEncargado = lineas.find(linea => {
    const lineaLimpia = linea.trim()
    return lineaLimpia.includes('[ENCARGADO]') || 
           (!lineaLimpia.includes('[ADMINISTRADOR]') && lineaLimpia.length > 0)
  })
  
  console.log('Comentario encargado encontrado:', comentarioEncargado)
  
  if (comentarioEncargado) {
    let resultado = comentarioEncargado.trim()
    // Quitar etiqueta si existe
    if (resultado.includes('[ENCARGADO]')) {
      resultado = resultado.replace('[ENCARGADO]', '').trim()
    }
    console.log('Resultado final:', resultado)
    return resultado
  }
  
  return ''
}

const extraerComentarioAdmin = (comentarios) => {
  if (!comentarios) return ''
  const lineas = comentarios.split('\n\n')
  const comentarioAdmin = lineas.find(linea => linea.includes('[ADMINISTRADOR]'))
  if (comentarioAdmin) {
    return comentarioAdmin.replace('[ADMINISTRADOR] ', '').trim()
  }
  return ''
}

const badgeEstadoPdf = (estado) => {
  switch (String(estado || '').toUpperCase()) {
    case 'VERIFICADO': case 'APROBADO': return 'bg-emerald-100 text-emerald-800'
    case 'RECHAZADO': return 'bg-red-100 text-red-800'
    case 'PENDIENTE': return 'bg-amber-100 text-amber-800'
    default: return 'bg-slate-100 text-slate-600'
  }
}

const cargarHistorial = async () => {
  isLoading.value = true
  try {
    const { data } = await api.get('/asistencias/mis-asistencias')
    historial.value = data
    const pr = await api.get('/asistencias/mi-progreso')
    progreso.value = pr.data
  } catch (e) { if (e.response?.status === 401) cerrarSesion() }
  finally { isLoading.value = false }
}

const abrirModalReporte = (asistencia) => {
  // Verificar si el reporte ya fue verificado por el encargado
  if (asistencia.reporte && asistencia.reporte.estado_encargado) {
    const estadoEncargado = String(asistencia.reporte.estado_encargado).toUpperCase()
    if (estadoEncargado === 'VERIFICADO' || estadoEncargado === 'RECTIFICADO') {
      alert('Este reporte ya fue verificado por el encargado y no puede ser modificado. Contacta al encargado si necesitas hacer cambios.')
      return
    }
  }
  
  asistenciaSeleccionada.value = asistencia
  actividadesModal.value = asistencia.reporte?.actividades_realizadas || ''
  errorModal.value = ''
  showModalReporte.value = true
}

const crearReporteSemanal = () => {
  // Crear un reporte semanal combinando todas las actividades de la semana
  const actividadesSemana = historialSemana.value
    .filter(item => item.reporte && item.reporte.actividades_realizadas)
    .map(item => `${formatFecha(item.fecha)}: ${item.reporte.actividades_realizadas}`)
    .join('\n\n')
  
  // Crear una asistencia virtual para el reporte semanal
  const asistenciaVirtual = {
    id: 'semanal-' + Date.now(),
    fecha: new Date().toISOString().split('T')[0],
    reporte: {
      actividades_realizadas: actividadesSemana || 'No hay actividades registradas esta semana'
    }
  }
  
  asistenciaSeleccionada.value = asistenciaVirtual
  actividadesModal.value = actividadesSemana || ''
  errorModal.value = ''
  showModalReporte.value = true
}

const guardarReporteModal = async () => {
  if (!asistenciaSeleccionada.value || !actividadesModal.value.trim()) return
  isSubmittingModal.value = true; errorModal.value = ''
  try {
    // Si es un reporte semanal (ID empieza con 'semanal-'), mostrar mensaje especial
    if (asistenciaSeleccionada.value.id.toString().startsWith('semanal-')) {
      errorModal.value = 'Los reportes semanales deben ser creados desde la sección de Reportes. Esta función solo previsualiza tu resumen semanal.'
      return
    }
    
    await api.post('/reportes/subir', { asistencia_id: asistenciaSeleccionada.value.id, actividades_realizadas: actividadesModal.value.trim() })
    showModalReporte.value = false
    await cargarHistorial()
  } catch (e) { errorModal.value = e.response?.data?.detail || 'Error al guardar el reporte.' }
  finally { isSubmittingModal.value = false }
}

// ---- PDF ----
const puedeCargar = computed(() => tipoPdf.value === 'semanal' ? !!pdfFechaSemana.value : !!(pdfMes.value && pdfAnio.value))

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

const obtenerRangoFechasSemana = () => {
  if (!pdfFechaSemana.value) return ''
  const d = new Date(pdfFechaSemana.value + 'T12:00:00')
  const diaSem = (d.getDay() + 6) % 7
  const lunes = new Date(d); lunes.setDate(d.getDate() - diaSem)
  const viernes = new Date(lunes); viernes.setDate(lunes.getDate() + 4)
  return `${lunes.toLocaleDateString('es-BO', { day: '2-digit', month: '2-digit' })} — ${viernes.toLocaleDateString('es-BO', { day: '2-digit', month: '2-digit', year: 'numeric' })}`
}

const isoSemana = (date) => {
  const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()))
  const dayNum = d.getUTCDay() || 7
  d.setUTCDate(d.getUTCDate() + 4 - dayNum)
  const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1))
  return Math.ceil((((d - yearStart) / 86400000) + 1) / 7)
}

const cargarVistaPrevia = async () => {
  if (!puedeCargar.value) return
  cargandoPdf.value = true; busquedaRealizada.value = false
  datosVistaPrevia.value = []; totalHorasVistaPrevia.value = 0; contadorEstados.value = {}; errorVistaPrevia.value = ''
  try {
    const params = {}
    if (tipoPdf.value === 'semanal') {
      const d = new Date(pdfFechaSemana.value + 'T12:00:00')
      const diaSem = (d.getDay() + 6) % 7
      const lunes = new Date(d); lunes.setDate(d.getDate() - diaSem)
      params.semana = isoSemana(lunes); params.anio = lunes.getFullYear()
      console.log('[DEBUG FRONTEND] Parámetros semanales:', params)
      console.log('[DEBUG FRONTEND] Fecha seleccionada:', pdfFechaSemana.value)
      console.log('[DEBUG FRONTEND] Lunes calculado:', lunes)
    } else { 
      params.mes = pdfMes.value; 
      params.anio = pdfAnio.value 
      console.log('[DEBUG FRONTEND] Parámetros mensuales:', params)
    }

    console.log('[DEBUG FRONTEND] Enviando request con params:', params)
    const { data: asistencias } = await api.get('/asistencias/mis-asistencias', { params })
    console.log('[DEBUG FRONTEND] Respuesta recibida:', asistencias.length, 'asistencias')
    datosVistaPrevia.value = asistencias.map(asist => ({
      fecha:            new Date(asist.fecha).toLocaleDateString('es-BO', { day: '2-digit', month: '2-digit', year: 'numeric' }),
      entrada:          asist.hora_entrada ? new Date(asist.hora_entrada).toLocaleTimeString('es-BO', { hour: '2-digit', minute: '2-digit' }) : '—',
      salida:           asist.hora_salida  ? new Date(asist.hora_salida).toLocaleTimeString('es-BO', { hour: '2-digit', minute: '2-digit' }) : '—',
      horas:            asist.horas_trabajadas ? `${asist.horas_trabajadas}h` : '—',
      estado_encargado: asist.reporte?.estado_encargado ?? (asist.reporte ? 'PENDIENTE' : 'SIN REGISTRO'),
      estado_admin:     asist.reporte?.estado_admin     ?? (asist.reporte ? 'PENDIENTE' : 'SIN REGISTRO'),
      comentario:       asist.reporte?.actividades_realizadas || '',
    }))
    totalHorasVistaPrevia.value = Math.round(asistencias.reduce((acc, a) => acc + (parseFloat(a.horas_trabajadas) || 0), 0) * 100) / 100
    contadorEstados.value = asistencias.reduce((cnt, a) => { const e = a.reporte?.estado_admin ?? (a.reporte ? 'PENDIENTE' : 'SIN REGISTRO'); cnt[e] = (cnt[e] || 0) + 1; return cnt }, {})
  } catch (err) { errorVistaPrevia.value = err.response?.data?.detail || 'Error al cargar asistencias.' }
  finally { cargandoPdf.value = false; busquedaRealizada.value = true }
}

const generarPdfDesdeVistaPrevia = async () => {
  descargando.value = true; errorDescarga.value = ''
  try {
    const u = authStore.user || {}
    const script = document.createElement('script')
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js'
    document.head.appendChild(script)
    await new Promise(resolve => { script.onload = resolve })
    const { jsPDF } = window.jspdf
    const doc = new jsPDF()
    const pageWidth = doc.internal.pageSize.getWidth()
    const pageHeight = doc.internal.pageSize.getHeight()
    const margin = 15
    let y = 25

    doc.setFillColor(30, 58, 138); doc.rect(margin, y - 8, pageWidth - 2 * margin, 30, 'F')
    doc.setTextColor(255,255,255); doc.setFontSize(16); doc.setFont(undefined, 'bold')
    doc.text(`REPORTE ${tipoPdf.value === 'semanal' ? 'SEMANAL' : 'MENSUAL'}`, pageWidth / 2, y + 2, { align: 'center' })
    doc.setFontSize(10); doc.setFont(undefined, 'normal')
    doc.text(`Período: ${tipoPdf.value === 'semanal' ? obtenerRangoFechasSemana() : `${mesesNombres[pdfMes.value - 1]} ${pdfAnio.value}`}`, pageWidth / 2, y + 10, { align: 'center' })
    doc.setFontSize(7); doc.setFont(undefined, 'italic')
    doc.text(`Generado: ${new Date().toLocaleDateString('es-BO')}`, pageWidth / 2, y + 17, { align: 'center' })
    doc.setTextColor(0,0,0); y += 35

    doc.setDrawColor(30,58,138); doc.rect(margin, y - 6, pageWidth - 2 * margin, 35, 'F')
    doc.setTextColor(30,58,138); doc.setFontSize(12); doc.setFont(undefined, 'bold')
    doc.text('DATOS DEL USUARIO - FACULTAD DE CIENCIAS SOCIALES - UMSA', margin + 8, y + 3)
    doc.setLineWidth(0.5); doc.line(margin + 8, y + 8, pageWidth - margin - 8, y + 8)
    doc.setTextColor(55,65,81); doc.setFontSize(9); doc.setFont(undefined, 'normal')
    doc.text(`Nombre: ${u?.nombres || ''} ${u?.apellidos || ''}`, margin + 10, y + 15)
    doc.text(`C.I.: ${u?.carnet_identidad || '—'}`, margin + 95, y + 15)
    doc.text(`R.U.: ${u?.ru || '—'}`, margin + 10, y + 21)
    doc.text(`Carrera: ${u?.carrera_nombre || '—'}`, margin + 95, y + 21)
    doc.text(`Unidad Asignada: ${u?.unidad_asignada || '—'}`, margin + 10, y + 27)
    doc.text(`Usuario: ${u?.username || '—'}`, margin + 95, y + 27)
    y += 40

    doc.setTextColor(30,58,138); doc.setFontSize(12); doc.setFont(undefined, 'bold')
    doc.text('REGISTRO DE ASISTENCIAS', margin, y); y += 8
const headers = ['Fecha','Entrada','Salida','Horas','Est. Encargado','Est. Admin']
const colWidths = [30,25,25,20,35,35]
    doc.setFillColor(30,58,138); doc.rect(margin, y - 3, pageWidth - 2 * margin, 6, 'F')
    doc.setTextColor(255,255,255); doc.setFontSize(7); doc.setFont(undefined, 'bold')
    headers.forEach((h, i) => {
      const colStart = margin + colWidths.slice(0, i).reduce((a,b)=>a+b,0)
      const colCenter = colStart + colWidths[i] / 2
      doc.text(h, colCenter, y + 1, { align: 'center' })
    })
    y += 5
    datosVistaPrevia.value.slice(0, 10).forEach((row, idx) => {
      if (idx % 2 === 0) { doc.setFillColor(248,250,252); doc.rect(margin, y - 2, pageWidth - 2 * margin, 5, 'F') }
const rowData = [row.fecha, row.entrada, row.salida, row.horas, row.estado_encargado||'—', row.estado_admin||'—'];
      rowData.forEach((data, ci) => {
        const colStart = margin + colWidths.slice(0, ci).reduce((a,b)=>a+b,0)
        const colCenter = colStart + colWidths[ci] / 2
        if (ci === 4) { const e=String(data||'').toUpperCase(); doc.setTextColor(e==='VERIFICADO'?34:e==='RECHAZADO'?239:e==='PENDIENTE'?245:107, e==='VERIFICADO'?197:e==='RECHAZADO'?68:e==='PENDIENTE'?158:114, e==='VERIFICADO'?94:e==='RECHAZADO'?68:e==='PENDIENTE'?11:128) }
        else if (ci === 5) { const e=String(data||'').toUpperCase(); doc.setTextColor(e==='APROBADO'?34:e==='RECHAZADO'?239:e==='PENDIENTE'?245:107, e==='APROBADO'?197:e==='RECHAZADO'?68:e==='PENDIENTE'?158:114, e==='APROBADO'?94:e==='RECHAZADO'?68:e==='PENDIENTE'?11:128) }
        else doc.setTextColor(55,65,81)
        doc.text(data||'—', colCenter, y + 3, { align: 'center' })
      })
      y += 5
    })

    y += 5
    doc.setTextColor(55,65,81); doc.setFontSize(9); doc.setFont(undefined, 'normal')
    const resumenText = `RESUMEN: Total Días: ${datosVistaPrevia.value.length} | Total Horas: ${totalHorasVistaPrevia.value.toFixed(2)}h | Aprobados: ${contadorEstados.value['APROBADO']||0} | Pendientes: ${contadorEstados.value['PENDIENTE']||0}`
    doc.text(resumenText, margin, y); y += 8

    // Mini informe profesional con actividades
    doc.setFillColor(245,245,245); doc.rect(margin, y - 2, pageWidth - 2 * margin, 22, 'F')
    doc.setDrawColor(30,58,138); doc.setLineWidth(0.5); doc.rect(margin, y - 2, pageWidth - 2 * margin, 22)
    doc.setFontSize(7.5); doc.setFont(undefined, 'normal'); doc.setTextColor(30,58,138)
    doc.text('INFORME DE ACTIVIDADES', margin + 3, y + 1)
    doc.setFontSize(7.5); doc.setFont(undefined, 'normal'); doc.setTextColor(55,65,81)
    const periodoLabel = tipoPdf.value === 'semanal' ? `semana del ${obtenerRangoFechasSemana()}` : `mes de ${mesesNombres[pdfMes.value - 1]} de ${pdfAnio.value}`
    const actividades = datosVistaPrevia.value
      .filter(d => d.comentario || d.actividades)
      .map(d => (d.comentario || d.actividades || '').trim())
      .filter(Boolean)
      .slice(0, 5)
      .join('; ')
    const informeText = `${u?.nombres || ''} ${u?.apellidos || ''} confirma haber realizado durante la ${periodoLabel} las siguientes actividades: ${actividades || 'Actividades según lo reportado en el período.'}`
    doc.text(informeText, margin + 3, y + 5, { maxWidth: pageWidth - 2 * margin - 6, align: 'justify' }); y += 24

    // Sección de Firmas
    y += 8
    doc.setTextColor(107,114,128); doc.setFontSize(7); doc.setFont(undefined, 'italic')
    doc.text('Los estados reflejan la última actualización realizada por los responsables.', margin, y)
    y += 10

    const fw = (pageWidth - 2 * margin - 6) / 2
    const fh = 22
    
    // Firma del Pasante (izq-arriba)
    doc.setDrawColor(0,0,0); doc.rect(margin, y, fw, fh)
    doc.setTextColor(0,0,0); doc.setFontSize(7); doc.setFont(undefined, 'normal')
    doc.text('Firma del Pasante:', margin + 2, y + 3)
    doc.line(margin + 2, y + 18, margin + fw - 2, y + 18)
    doc.text('Fecha: ______________', margin + 2, y + 20)

    // Firma del Encargado (dcha-arriba)
    doc.rect(margin + fw + 3, y, fw, fh)
    doc.text('Firma del Encargado:', margin + fw + 5, y + 3)
    doc.line(margin + fw + 5, y + 18, margin + 2 * fw + 1, y + 18)
    doc.text('Fecha: ______________', margin + fw + 5, y + 20)

    y += fh + 3

    // Firma del Administrador (izq-abajo)
    doc.rect(margin, y, fw, fh)
    doc.text('Firma del Administrador:', margin + 2, y + 3)
    doc.line(margin + 2, y + 18, margin + fw - 2, y + 18)
    doc.text('Fecha: ______________', margin + 2, y + 20)

    // Sello Institucional (dcha-abajo)
    doc.rect(margin + fw + 3, y, fw, fh)
    doc.text('Sello Institucional:', margin + fw + 5, y + 3)
    doc.line(margin + fw + 5, y + 18, margin + 2 * fw + 1, y + 18)
    doc.text('Fecha: ______________', margin + fw + 5, y + 20)

    y = pageHeight - 12
    doc.setDrawColor(203,213,225); doc.line(margin, y, pageWidth - margin, y)
    doc.setTextColor(107,114,128); doc.setFontSize(6); doc.setFont(undefined, 'italic')
    doc.text('Sistema de Asistencias — UMSA Facultad de Ciencias Sociales', pageWidth / 2, y + 8, { align: 'center' })

    const nombre = `${u?.nombres||''}_${u?.apellidos||''}`.trim().replace(/\s+/g,'_') || 'pasante'
    doc.save(`reporte_${tipoPdf.value}_${nombre}_${new Date().toISOString().split('T')[0]}.pdf`)
  } catch { errorDescarga.value = 'Error al generar el PDF. Intenta nuevamente.' }
  finally { descargando.value = false }
}

const cerrarSesion = () => { authStore.logout(); router.push('/') }

onMounted(() => {
  cargarHistorial()
})
</script>

<style scoped>
.modal-enter-active, .modal-leave-active { transition: opacity 0.2s ease, transform 0.2s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; transform: scale(0.97); }
</style>
