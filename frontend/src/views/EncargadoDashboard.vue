<template>
  <div class="min-h-screen bg-slate-100 font-sans pb-12">

    <header class="bg-blue-950 border-b-4 border-red-700 sticky top-0 z-50 shadow-2xl">
      <div class="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-5 pointer-events-none"></div>
      <div class="max-w-[96rem] mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div class="flex justify-between h-16 items-center">

          <div class="flex items-center gap-4">
            <div class="w-12 h-12 bg-gradient-to-br from-white to-slate-200 rounded-xl flex items-center justify-center text-blue-950 font-black text-xs shadow-lg border border-white/20 overflow-hidden">
              <img v-if="authStore.user?.carrera_logo_url" :src="resolveStaticUrl(authStore.user.carrera_logo_url)" alt="Logo" class="w-full h-full object-contain p-1" />
              <span v-else><span class="text-red-700 text-lg mr-0.5 leading-none">U</span>MSA</span>
            </div>
            <div class="border-l-2 border-white/10 pl-4 py-1 hidden sm:block">
              <p class="text-[10px] text-red-400 font-black uppercase tracking-widest leading-none mb-1">Facultad de Cs. Sociales</p>
              <p class="text-sm font-extrabold text-white leading-none tracking-tight">
                Sistema de Pasantías
                <span class="text-blue-300/50 font-medium ml-1">| Encargado</span>
              </p>
              <p v-if="authStore.user?.carrera_nombre" class="text-[10px] text-blue-300/70 mt-0.5">{{ authStore.user.carrera_nombre }}</p>
            </div>
          </div>

          <nav class="hidden lg:flex items-center gap-1.5 bg-blue-900/50 p-1 rounded-xl border border-white/5">
            <button @click="seccion = 'dashboard'"
              :class="seccion === 'dashboard' ? 'bg-blue-800 text-white shadow-md' : 'text-blue-200 hover:bg-blue-800/50 hover:text-white'"
              class="px-5 py-2 rounded-lg text-sm font-semibold transition-all">Dashboard</button>
            <button @click="seccion = 'reportes'"
              :class="seccion === 'reportes' ? 'bg-blue-800 text-white shadow-md' : 'text-blue-200 hover:bg-blue-800/50 hover:text-white'"
              class="px-5 py-2 rounded-lg text-sm font-semibold transition-all">Reportes</button>
            <button @click="seccion = 'horas'"
              :class="seccion === 'horas' ? 'bg-blue-800 text-white shadow-md' : 'text-blue-200 hover:bg-blue-800/50 hover:text-white'"
              class="px-5 py-2 rounded-lg text-sm font-semibold transition-all">Horas</button>
            <button @click="seccion = 'usuarios'"
              :class="seccion === 'usuarios' ? 'bg-blue-800 text-white shadow-md' : 'text-blue-200 hover:bg-blue-800/50 hover:text-white'"
              class="px-5 py-2 rounded-lg text-sm font-semibold transition-all">Pasantes</button>
          </nav>

          <div class="flex items-center gap-4">
            <div class="hidden sm:flex flex-col items-end">
              <span class="text-white text-sm font-bold leading-tight">{{ authStore.user?.nombres }}</span>
              <span class="text-[10px] font-black text-red-400 uppercase tracking-widest">Encargado</span>
            </div>
            <button @click="router.push('/perfil')" title="Perfil"
              class="w-10 h-10 bg-gradient-to-br from-red-600 to-red-800 rounded-xl flex items-center justify-center text-white font-bold text-sm border border-red-500 hover:shadow-lg hover:shadow-red-600/30 transition-all">
              {{ getIniciales(authStore.user?.nombres || '', authStore.user?.apellidos || '') }}
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

      <!-- Navegacion Movil -->
      <div class="lg:hidden border-t border-white/10 bg-blue-900/50 px-4 py-2 flex gap-2">
        <button @click="seccion = 'dashboard'"
          :class="seccion === 'dashboard' ? 'bg-blue-800 text-white' : 'text-blue-200'"
          class="flex-1 px-3 py-2 rounded-lg text-xs font-semibold transition-all">Dashboard</button>
        <button @click="seccion = 'reportes'"
          :class="seccion === 'reportes' ? 'bg-blue-800 text-white' : 'text-blue-200'"
          class="flex-1 px-3 py-2 rounded-lg text-xs font-semibold transition-all">Reportes</button>
        <button @click="seccion = 'horas'"
          :class="seccion === 'horas' ? 'bg-blue-800 text-white' : 'text-blue-200'"
          class="flex-1 px-3 py-2 rounded-lg text-xs font-semibold transition-all">Horas</button>
        <button @click="seccion = 'usuarios'"
          :class="seccion === 'usuarios' ? 'bg-blue-800 text-white' : 'text-blue-200'"
          class="flex-1 px-3 py-2 rounded-lg text-xs font-semibold transition-all">Pasantes</button>
      </div>
    </header>

    <!-- CONTENIDO PRINCIPAL -->
    <main class="max-w-[96rem] mx-auto px-4 sm:px-6 lg:px-8 py-8">

      <!-- DASHBOARD -->
      <template v-if="seccion === 'dashboard'">
        <div class="space-y-8">

          <div class="bg-gradient-to-r from-blue-950 to-blue-900 rounded-2xl p-8 text-white shadow-lg relative overflow-hidden border border-blue-900">
            <div class="absolute top-0 right-0 w-32 h-32 bg-white/5 rounded-full blur-2xl -translate-y-1/2 translate-x-1/2"></div>
            <div class="absolute bottom-0 left-0 w-24 h-24 bg-white/5 rounded-full blur-xl translate-y-1/2 -translate-x-1/2"></div>
            <div class="relative z-10">
              <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
                <div class="flex-1">
                  <p class="text-blue-200 text-sm font-medium uppercase tracking-wider mb-1">Bienvenido(a) Encargado</p>
                  <h1 class="text-3xl font-bold mb-2">{{ authStore.user?.nombres }}</h1>
                  <p class="text-blue-100 text-sm mb-3">Panel de Control — Sistema de Gestion de Pasantias</p>
                  
                </div>
                <div class="flex items-center gap-4">
                  <div class="text-center px-6 py-3 bg-white/10 rounded-xl backdrop-blur-sm border border-white/20">
                    <p class="text-3xl font-bold">{{ stats.totalPasantes }}</p>
                    <p class="text-xs text-blue-200 uppercase tracking-wider">Pasantes</p>
                  </div>
                  <div class="text-center px-6 py-3 bg-white/10 rounded-xl backdrop-blur-sm border border-white/20">
                    <p class="text-3xl font-bold">{{ stats.pendientes }}</p>
                    <p class="text-xs text-blue-200 uppercase tracking-wider">Pendientes</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-2 lg:grid-cols-4 gap-6">
            <div class="bg-white rounded-xl border border-slate-200 p-6 hover:shadow-lg hover:border-blue-200 transition-all duration-300">
              <div class="flex items-start justify-between">
                <div class="w-12 h-12 bg-blue-50 rounded-xl flex items-center justify-center">
                  <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/></svg>
                </div>
                <span class="text-xs font-medium text-blue-600 bg-blue-50 px-2 py-1 rounded-full">TOTAL</span>
              </div>
              <div class="mt-4">
                <p class="text-3xl font-bold text-slate-800">{{ stats.totalPasantes }}</p>
                <p class="text-sm text-slate-500 mt-1">Pasantes registrados</p>
              </div>
            </div>

            <div class="bg-white rounded-xl border border-slate-200 p-6 hover:shadow-lg hover:border-emerald-200 transition-all duration-300">
              <div class="flex items-start justify-between">
                <div class="w-12 h-12 bg-emerald-50 rounded-xl flex items-center justify-center">
                  <svg class="w-6 h-6 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                </div>
                <span class="text-xs font-medium text-emerald-600 bg-emerald-50 px-2 py-1 rounded-full">{{ stats.pctActivos }}%</span>
              </div>
              <div class="mt-4">
                <p class="text-3xl font-bold text-slate-800">{{ stats.activos }}</p>
                <p class="text-sm text-slate-500 mt-1">Pasantes activos</p>
              </div>
              <div class="mt-3 h-1.5 bg-slate-100 rounded-full overflow-hidden">
                <div class="h-full bg-emerald-500 rounded-full" :style="{ width: stats.pctActivos + '%' }"></div>
              </div>
            </div>

            <div class="bg-white rounded-xl border border-slate-200 p-6 hover:shadow-lg hover:border-violet-200 transition-all duration-300">
              <div class="flex items-start justify-between">
                <div class="w-12 h-12 bg-violet-50 rounded-xl flex items-center justify-center">
                  <svg class="w-6 h-6 text-violet-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
                </div>
                <span class="text-xs font-medium text-violet-600 bg-violet-50 px-2 py-1 rounded-full">TOTAL</span>
              </div>
              <div class="mt-4">
                <p class="text-3xl font-bold text-slate-800">{{ stats.totalReportes }}</p>
                <p class="text-sm text-slate-500 mt-1">Reportes recibidos</p>
              </div>
            </div>

            <div class="bg-white rounded-xl border border-slate-200 p-6 hover:shadow-lg hover:border-amber-200 transition-all duration-300">
              <div class="flex items-start justify-between">
                <div class="w-12 h-12 bg-amber-50 rounded-xl flex items-center justify-center">
                  <svg class="w-6 h-6 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                </div>
                <span class="text-xs font-medium text-amber-600 bg-amber-50 px-2 py-1 rounded-full">PENDIENTE</span>
              </div>
              <div class="mt-4">
                <p class="text-3xl font-bold text-slate-800">{{ stats.pendientes }}</p>
                <p class="text-sm text-slate-500 mt-1">Por evaluar</p>
              </div>
            </div>
          </div>

          <div class="grid lg:grid-cols-2 gap-6">
            <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
              <div class="px-6 py-4 border-b border-slate-100 bg-slate-50/50">
                <h2 class="text-lg font-semibold text-slate-800">Estado de Pasantes</h2>
                <p class="text-sm text-slate-500">Distribucion por estado actual</p>
              </div>
              <div class="p-6">
                <div class="flex items-center gap-8">
                  <div class="relative w-32 h-32 flex-shrink-0">
                    <svg class="w-32 h-32 -rotate-90" viewBox="0 0 100 100">
                      <circle cx="50" cy="50" r="40" fill="none" stroke="#f1f5f9" stroke-width="12"/>
                      <circle cx="50" cy="50" r="40" fill="none" stroke="#1e3a5f" stroke-width="12" stroke-linecap="round"
                        :stroke-dasharray="2 * 3.1416 * 40"
                        :stroke-dashoffset="2 * 3.1416 * 40 * (1 - stats.pctActivos / 100)"
                        class="transition-all duration-1000"/>
                    </svg>
                    <div class="absolute inset-0 flex flex-col items-center justify-center">
                      <span class="text-2xl font-bold text-slate-800">{{ stats.pctActivos }}%</span>
                      <span class="text-xs text-slate-400">Activos</span>
                    </div>
                  </div>
                  <div class="flex-1 space-y-4">
                    <div class="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
                      <div class="flex items-center gap-3">
                        <div class="w-3 h-3 rounded-full bg-blue-900"></div>
                        <span class="text-sm text-slate-600">Activos</span>
                      </div>
                      <span class="font-semibold text-slate-800">{{ stats.activos }}</span>
                    </div>
                    <div class="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
                      <div class="flex items-center gap-3">
                        <div class="w-3 h-3 rounded-full bg-slate-300"></div>
                        <span class="text-sm text-slate-600">Inactivos</span>
                      </div>
                      <span class="font-semibold text-slate-800">{{ stats.inactivos }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
              <div class="px-6 py-4 border-b border-slate-100 bg-slate-50/50">
                <h2 class="text-lg font-semibold text-slate-800">Estado de Reportes</h2>
                <p class="text-sm text-slate-500">Evaluacion de reportes diarios</p>
              </div>
              <div class="p-6 space-y-4">
                <div>
                  <div class="flex items-center justify-between mb-2">
                    <div class="flex items-center gap-2">
                      <div class="w-2.5 h-2.5 rounded-full bg-blue-500"></div>
                      <span class="text-sm text-slate-600">Verificados</span>
                    </div>
                    <div class="flex items-center gap-2">
                      <span class="text-sm font-semibold text-slate-800">{{ stats.verificados }}</span>
                      <span class="text-xs text-slate-400">({{ stats.pctVerificados }}%)</span>
                    </div>
                  </div>
                  <div class="h-2 bg-slate-100 rounded-full overflow-hidden">
                    <div class="h-full bg-blue-500 rounded-full transition-all duration-500" :style="{ width: stats.pctVerificados + '%' }"></div>
                  </div>
                </div>
                <div>
                  <div class="flex items-center justify-between mb-2">
                    <div class="flex items-center gap-2">
                      <div class="w-2.5 h-2.5 rounded-full bg-purple-500"></div>
                      <span class="text-sm text-slate-600">Rectificados</span>
                    </div>
                    <div class="flex items-center gap-2">
                      <span class="text-sm font-semibold text-slate-800">{{ stats.rectificados }}</span>
                      <span class="text-xs text-slate-400">({{ stats.pctRectificados }}%)</span>
                    </div>
                  </div>
                  <div class="h-2 bg-slate-100 rounded-full overflow-hidden">
                    <div class="h-full bg-purple-500 rounded-full transition-all duration-500" :style="{ width: stats.pctRectificados + '%' }"></div>
                  </div>
                </div>
                <div>
                  <div class="flex items-center justify-between mb-2">
                    <div class="flex items-center gap-2">
                      <div class="w-2.5 h-2.5 rounded-full bg-amber-500"></div>
                      <span class="text-sm text-slate-600">Pendientes</span>
                    </div>
                    <div class="flex items-center gap-2">
                      <span class="text-sm font-semibold text-slate-800">{{ stats.pendientes }}</span>
                      <span class="text-xs text-slate-400">({{ stats.pctPendientes }}%)</span>
                    </div>
                  </div>
                  <div class="h-2 bg-slate-100 rounded-full overflow-hidden">
                    <div class="h-full bg-amber-500 rounded-full transition-all duration-500" :style="{ width: stats.pctPendientes + '%' }"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
            <div class="px-6 py-4 border-b border-slate-100 bg-slate-50/50">
              <h2 class="text-lg font-semibold text-slate-800">Acciones Rapidas</h2>
            </div>
            <div class="p-6">
              <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <button @click="seccion = 'reportes'" class="group p-5 rounded-xl border border-slate-200 hover:border-blue-300 hover:bg-blue-50/50 transition-all duration-200 text-left">
                  <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mb-3 group-hover:bg-blue-200 transition-colors">
                    <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
                  </div>
                  <p class="font-semibold text-slate-700 group-hover:text-blue-700">Ver Reportes</p>
                  <p class="text-xs text-slate-400 mt-1">{{ stats.totalReportes }} reportes</p>
                </button>
                <button @click="seccion = 'usuarios'" class="group p-5 rounded-xl border border-slate-200 hover:border-emerald-300 hover:bg-emerald-50/50 transition-all duration-200 text-left">
                  <div class="w-10 h-10 bg-emerald-100 rounded-lg flex items-center justify-center mb-3 group-hover:bg-emerald-200 transition-colors">
                    <svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/></svg>
                  </div>
                  <p class="font-semibold text-slate-700 group-hover:text-emerald-700">Ver Pasantes</p>
                  <p class="text-xs text-slate-400 mt-1">{{ stats.totalPasantes }} registrados</p>
                </button>
                <button @click="abrirModalCrear" class="group p-5 rounded-xl border border-slate-200 hover:border-violet-300 hover:bg-violet-50/50 transition-all duration-200 text-left">
                  <div class="w-10 h-10 bg-violet-100 rounded-lg flex items-center justify-center mb-3 group-hover:bg-violet-200 transition-colors">
                    <svg class="w-5 h-5 text-violet-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"/></svg>
                  </div>
                  <p class="font-semibold text-slate-700 group-hover:text-violet-700">Nuevo Pasante</p>
                  <p class="text-xs text-slate-400 mt-1">Registrar</p>
                </button>
                <button @click="evaluarPendiente" class="group p-5 rounded-xl border border-slate-200 hover:border-amber-300 hover:bg-amber-50/50 transition-all duration-200 text-left">
                  <div class="w-10 h-10 bg-amber-100 rounded-lg flex items-center justify-center mb-3 group-hover:bg-amber-200 transition-colors">
                    <svg class="w-5 h-5 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/></svg>
                  </div>
                  <p class="font-semibold text-slate-700 group-hover:text-amber-700">Evaluar</p>
                  <p class="text-xs text-slate-400 mt-1">{{ stats.pendientes }} pendientes</p>
                </button>
              </div>
            </div>
          </div>

        </div>
      </template>

      <EncargadoReportes v-if="seccion === 'reportes'" />
      <EncargadoHoras v-if="seccion === 'horas'" />
      <EncargadoUsuarios v-if="seccion === 'usuarios'" />

    </main>

    <!-- MODAL: VER PASANTE -->
    <div v-if="showModalVer" class="fixed inset-0 z-50 flex items-center justify-center bg-blue-950/80 px-4 backdrop-blur-sm">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden border border-blue-100">
        <div class="px-8 py-5 bg-gradient-to-r from-blue-950 to-blue-900 flex justify-between items-center border-b-4 border-red-600">
          <div>
            <p class="text-blue-200 text-xs font-medium uppercase tracking-wider">Informacion del Pasante</p>
            <h3 class="text-xl font-bold text-white mt-1">{{ pasanteSeleccionado?.nombres }} {{ pasanteSeleccionado?.apellidos }}</h3>
          </div>
          <button @click="showModalVer = false" class="text-blue-300 hover:text-white transition-colors bg-white/10 p-1.5 rounded-lg">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12"/></svg>
          </button>
        </div>
        <div class="p-6" v-if="pasanteSeleccionado">
          <div v-if="historial.length" class="mb-6">
            <h4 class="text-sm font-semibold mb-2">Historial de asistencias</h4>
            <ul class="text-xs space-y-1">
              <li v-for="a in historial" :key="a.id">{{ a.fecha }} {{ a.hora_entrada }} — {{ a.hora_salida || '---' }}</li>
            </ul>
          </div>
          <div v-else class="mb-6 text-xs text-slate-500">Sin asistencias registradas.</div>
          <div class="flex items-center gap-4 mb-6">
            <div class="w-16 h-16 bg-gradient-to-br from-blue-800 to-blue-950 rounded-xl flex items-center justify-center text-white font-bold text-xl shadow-md">
              {{ getIniciales(pasanteSeleccionado.nombres, pasanteSeleccionado.apellidos) }}
            </div>
            <span :class="pasanteSeleccionado.estado ? 'bg-emerald-50 text-emerald-600' : 'bg-red-50 text-red-600'" class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium">
              <span :class="pasanteSeleccionado.estado ? 'bg-emerald-500' : 'bg-red-500'" class="w-1.5 h-1.5 rounded-full mr-1.5"></span>
              {{ pasanteSeleccionado.estado ? 'Activo' : 'Inactivo' }}
            </span>
          </div>
          <div class="space-y-3">
            <div class="flex items-center gap-3 p-3 bg-slate-50 rounded-lg">
              <svg class="w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
              <div><p class="text-xs text-slate-400">Username</p><p class="font-mono text-sm font-semibold text-blue-600">{{ pasanteSeleccionado.username }}</p></div>
            </div>
            <div class="flex items-center gap-3 p-3 bg-slate-50 rounded-lg">
              <svg class="w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
              <div><p class="text-xs text-slate-400">Correo Electronico</p><p class="text-sm font-semibold text-slate-700">{{ pasanteSeleccionado.email }}</p></div>
            </div>
            <div class="flex items-center gap-3 p-3 bg-slate-50 rounded-lg">
              <svg class="w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V8a2 2 0 00-2-2h-5m-4 0V5a2 2 0 114 0v1m-4 0a2 2 0 104 0"/></svg>
              <div><p class="text-xs text-slate-400">Carnet de Identidad</p><p class="text-sm font-semibold text-slate-700">{{ pasanteSeleccionado.carnet_identidad || '—' }}</p></div>
            </div>
          </div>
        </div>
        <div class="px-6 py-4 bg-slate-50 border-t border-slate-100 flex justify-end gap-3">
          <button @click="showModalVer = false" class="px-4 py-2 text-sm font-medium text-slate-600 border border-slate-300 rounded-xl hover:bg-slate-100 transition-colors">Cerrar</button>
          <button @click="abrirModalEditar(pasanteSeleccionado); showModalVer = false" class="px-5 py-2 bg-gradient-to-r from-blue-800 to-blue-950 text-white text-sm font-black rounded-xl hover:from-blue-700 hover:to-blue-900 transition-all shadow-md">Editar Pasante</button>
        </div>
      </div>
    </div>

    <!-- MODAL: EDITAR PASANTE -->
    <div v-if="showModalEditar" class="fixed inset-0 z-50 flex items-center justify-center bg-blue-950/80 px-4 backdrop-blur-sm overflow-y-auto">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg my-8 border border-blue-100">
        <div class="px-8 py-5 bg-gradient-to-r from-blue-950 to-blue-900 flex justify-between items-center border-b-4 border-red-600">
          <div>
            <p class="text-blue-200 text-xs font-medium uppercase tracking-wider">Formulario de Edicion</p>
            <h3 class="text-xl font-bold text-white mt-1">{{ pasanteSeleccionado?.nombres }} {{ pasanteSeleccionado?.apellidos }}</h3>
          </div>
          <button @click="showModalEditar = false" class="text-blue-300 hover:text-white transition-colors bg-white/10 p-1.5 rounded-lg">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12"/></svg>
          </button>
        </div>
        <form @submit.prevent="guardarEdicion" class="p-6">
          <p class="text-xs text-slate-400 mb-6">Deja vacio cualquier campo que no desees modificar.</p>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1.5">Nombres</label>
              <input v-model="formEditar.nombres" type="text" class="w-full border border-slate-300 rounded-xl p-3.5 outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-200 text-sm font-bold bg-slate-50 focus:bg-white transition-all" />
            </div>
            <div>
              <label class="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1.5">Apellidos</label>
              <input v-model="formEditar.apellidos" type="text" class="w-full border border-slate-300 rounded-xl p-3.5 outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-200 text-sm font-bold bg-slate-50 focus:bg-white transition-all" />
            </div>
            <div>
              <label class="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1.5">Carnet de Identidad</label>
              <input v-model="formEditar.carnet_identidad" type="text" class="w-full border border-slate-300 rounded-xl p-3.5 outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-200 text-sm font-bold bg-slate-50 focus:bg-white transition-all" />
            </div>
            <div>
              <label class="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1.5">Correo Electronico</label>
              <input v-model="formEditar.email" type="email" class="w-full border border-slate-300 rounded-xl p-3.5 outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-200 text-sm font-bold bg-slate-50 focus:bg-white transition-all" />
            </div>
          </div>
          <div v-if="mensajeErrorEditar" class="mt-4 p-3 bg-red-50 border border-red-200 rounded-xl">
            <p class="text-red-600 text-sm font-bold">{{ mensajeErrorEditar }}</p>
          </div>
          <div class="mt-6 pt-4 border-t border-slate-100 flex justify-end gap-3">
            <button type="button" @click="showModalEditar = false" class="px-6 py-3 border border-slate-300 rounded-xl text-slate-600 text-sm font-bold hover:bg-slate-50 transition-colors">Cancelar</button>
            <button type="submit" :disabled="isSubmittingEditar" class="px-6 py-2.5 bg-gradient-to-r from-blue-800 to-blue-950 text-white text-sm font-black uppercase tracking-widest rounded-xl hover:from-blue-700 hover:to-blue-900 disabled:opacity-50 shadow-lg shadow-blue-900/30 transition-all">
              {{ isSubmittingEditar ? 'Guardando...' : 'Guardar Cambios' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- MODAL: CREAR PASANTE -->
    <div v-if="showModalCrear" class="fixed inset-0 z-50 flex items-center justify-center bg-blue-950/80 px-4 backdrop-blur-sm overflow-y-auto">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg my-8 border border-blue-100">
        <div class="px-8 py-5 bg-gradient-to-r from-blue-950 to-blue-900 flex justify-between items-center border-b-4 border-red-600">
          <div>
            <p class="text-blue-200 text-xs font-medium uppercase tracking-wider">Registro de Pasante</p>
            <h3 class="text-xl font-bold text-white mt-1">Nuevo Pasante</h3>
          </div>
          <button @click="showModalCrear = false" class="text-blue-300 hover:text-white transition-colors bg-white/10 p-1.5 rounded-lg">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12"/></svg>
          </button>
        </div>
        <form @submit.prevent="registrarPasante" class="p-6">
          <div v-if="usernamePreview" class="mb-4 p-4 bg-blue-50 border border-blue-200 rounded-xl flex items-center justify-between">
            <span class="text-sm text-blue-700 font-bold">Username automático:</span>
            <strong class="font-mono bg-white px-3 py-1 rounded-lg border border-blue-200 text-red-700 tracking-wider shadow-sm">{{ usernamePreview }}</strong>
          </div>
          <div class="mb-4 p-4 bg-amber-50 border border-amber-200 rounded-xl">
            <div class="flex items-center gap-2">
              <svg class="w-5 h-5 text-amber-600 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
              <span class="text-sm text-amber-700">El pasante sera asignado a la carrera <strong>ID: {{ authStore.user?.carrera_id }}</strong></span>
            </div>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1.5">Nombres <span class="text-red-500">*</span></label>
              <input v-model="formulario.nombres" type="text" required class="w-full border border-slate-300 rounded-xl p-3.5 outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-200 text-sm font-bold bg-slate-50 focus:bg-white transition-all" />
            </div>
            <div>
              <label class="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1.5">Apellidos <span class="text-red-500">*</span></label>
              <input v-model="formulario.apellidos" type="text" required class="w-full border border-slate-300 rounded-xl p-3.5 outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-200 text-sm font-bold bg-slate-50 focus:bg-white transition-all" />
            </div>
            <div>
              <label class="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1.5">Carnet de Identidad <span class="text-red-500">*</span></label>
              <input v-model="formulario.carnet_identidad" type="text" required class="w-full border border-slate-300 rounded-xl p-3.5 outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-200 text-sm font-bold bg-slate-50 focus:bg-white transition-all" />
            </div>
            <div>
              <label class="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1.5">Correo Electronico <span class="text-red-500">*</span></label>
              <input v-model="formulario.email" type="email" required class="w-full border border-slate-300 rounded-xl p-3.5 outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-200 text-sm font-bold bg-slate-50 focus:bg-white transition-all" />
            </div>
            <div>
              <label class="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1.5">Celular <span class="text-red-500">*</span></label>
              <input v-model="formulario.celular" type="tel" required placeholder="Ej. 70123456" class="w-full border border-slate-300 rounded-xl p-3.5 outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-200 text-sm font-bold bg-slate-50 focus:bg-white transition-all" />
            </div>
            <div class="md:col-span-2">
              <label class="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1.5">Contrasena Temporal <span class="text-red-500">*</span></label>
              <input v-model="formulario.password" type="password" required placeholder="Minimo 6 caracteres" class="w-full border border-slate-300 rounded-xl p-3.5 outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-200 text-sm font-bold bg-slate-50 focus:bg-white transition-all" />
            </div>
          </div>
          <div v-if="mensajeError" class="mt-4 p-3 bg-red-50 border border-red-200 rounded-xl">
            <p class="text-red-600 text-sm font-bold">{{ mensajeError }}</p>
          </div>
          <div class="mt-6 pt-4 border-t border-slate-100 flex justify-end gap-3">
            <button type="button" @click="showModalCrear = false" class="px-6 py-3 border border-slate-300 rounded-xl text-slate-600 text-sm font-bold hover:bg-slate-50 transition-colors">Cancelar</button>
            <button type="submit" :disabled="isSubmittingCrear" class="px-6 py-2.5 bg-gradient-to-r from-blue-800 to-blue-950 text-white text-sm font-black uppercase tracking-widest rounded-xl hover:from-blue-700 hover:to-blue-900 disabled:opacity-50 shadow-lg shadow-blue-900/30 transition-all">
              {{ isSubmittingCrear ? 'Registrando...' : 'Registrar Pasante' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- MODAL: CONFIRMAR CAMBIO DE ESTADO -->
    <div v-if="showModalBaja" class="fixed inset-0 z-50 flex items-center justify-center bg-blue-950/80 px-4 backdrop-blur-sm">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-sm overflow-hidden border border-blue-100">
        <div class="px-8 py-5 bg-gradient-to-r from-blue-950 to-blue-900 border-b-4 border-red-600">
          <h3 class="text-lg font-black text-white uppercase tracking-widest">{{ pasanteSeleccionado?.estado ? 'Dar de Baja' : 'Reactivar Pasante' }}</h3>
        </div>
        <div class="p-6 text-center">
          <div :class="pasanteSeleccionado?.estado ? 'bg-red-100' : 'bg-emerald-100'" class="w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg v-if="pasanteSeleccionado?.estado" class="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
            <svg v-else class="w-8 h-8 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          </div>
          <h4 class="text-lg font-semibold text-slate-800 mb-2">
            {{ pasanteSeleccionado?.estado ? '¿Dar de baja a este pasante?' : '¿Reactivar a este pasante?' }}
          </h4>
          <p class="text-slate-600 font-medium">{{ pasanteSeleccionado?.nombres }} {{ pasanteSeleccionado?.apellidos }}</p>
          <p class="text-sm text-slate-400 mt-2">
            {{ pasanteSeleccionado?.estado ? 'Su cuenta quedara inactiva y no podra acceder al sistema.' : 'Su cuenta volvera a estar activa.' }}
          </p>
        </div>
        <div class="px-6 py-4 bg-slate-50 border-t border-slate-100 flex justify-center gap-3">
          <button @click="showModalBaja = false" class="px-4 py-2 text-sm font-bold text-slate-600 border border-slate-300 rounded-xl hover:bg-slate-100 transition-colors">Cancelar</button>
          <button @click="ejecutarCambioEstado" :disabled="isSubmittingBaja"
            :class="pasanteSeleccionado?.estado ? 'bg-red-600 hover:bg-red-700' : 'bg-emerald-600 hover:bg-emerald-700'"
            class="px-5 py-2 text-white text-sm font-black rounded-xl disabled:opacity-50 transition-colors shadow-md">
            {{ isSubmittingBaja ? 'Procesando...' : (pasanteSeleccionado?.estado ? 'Si, dar de baja' : 'Si, reactivar') }}
          </button>
        </div>
      </div>
    </div>

    <!-- MODAL: EVALUAR REPORTE -->
    <div v-if="showModalEvaluacion" class="fixed inset-0 z-50 flex items-center justify-center bg-blue-950/80 px-4 backdrop-blur-sm">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg overflow-hidden border border-blue-100">
        <div class="px-8 py-5 bg-gradient-to-r from-blue-950 to-blue-900 flex justify-between items-center border-b-4 border-red-600">
          <div>
            <p class="text-blue-200 text-xs font-medium uppercase tracking-wider">Evaluacion</p>
            <h3 class="text-xl font-bold text-white mt-1">Reporte #{{ reporteSeleccionado?.id }}</h3>
          </div>
          <button @click="cerrarModalEvaluacion" class="text-blue-300 hover:text-white transition-colors bg-white/10 p-1.5 rounded-lg">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12"/></svg>
          </button>
        </div>
        <div class="p-6">
          <div class="mb-4 bg-slate-50 p-4 rounded-xl border border-slate-200">
            <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Pasante</p>
            <p class="font-black text-blue-950">{{ reporteSeleccionado?.nombre_pasante }}</p>
          </div>
          <div class="mb-5">
            <label class="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-2">Actividades Realizadas</label>
            <div class="p-4 bg-slate-50 border border-slate-200 rounded-xl text-sm text-slate-600 whitespace-pre-wrap max-h-40 overflow-y-auto">
              {{ reporteSeleccionado?.actividades_realizadas }}
            </div>
          </div>
          <div v-if="reporteSeleccionado?.comentarios_director" class="mb-5">
            <label class="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-2">Comentario Anterior</label>
            <div class="bg-blue-50 border border-blue-200 rounded-xl p-4 text-sm text-blue-700">
              {{ reporteSeleccionado.comentarios_director }}
            </div>
          </div>
          <div class="space-y-4">
            <div>
              <label class="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-2">Decision</label>
              <select v-model="evaluacion.estado" class="w-full border border-slate-300 rounded-xl p-3.5 bg-white cursor-pointer focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm font-bold outline-none">
                <option value="VERIFICADO">Verificar reporte</option>
                <option v-if="yaEvaluado(reporteSeleccionado)" value="RECTIFICADO">Rectificar reporte</option>
              </select>
            </div>
            <div>
              <label class="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-2">Comentario <span class="text-red-500 normal-case font-black">(obligatorio)</span></label>
              <textarea v-model="evaluacion.comentarios" rows="3" placeholder="Retroalimentacion para el pasante..." class="w-full border border-slate-300 rounded-xl p-3.5 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm outline-none resize-none bg-slate-50 focus:bg-white transition-all"></textarea>
            </div>
          </div>
        </div>
        <div class="px-6 py-4 bg-slate-50 border-t border-slate-100 flex justify-end gap-3">
          <button @click="cerrarModalEvaluacion" class="px-6 py-3 border border-slate-300 rounded-xl text-slate-600 text-sm font-bold hover:bg-slate-100 transition-colors">Cancelar</button>
          <button @click="enviarEvaluacion" :disabled="isSubmittingEval || !evaluacion.comentarios.trim()"
            class="px-6 py-2.5 bg-gradient-to-r from-blue-800 to-blue-950 text-white text-sm font-black uppercase tracking-widest rounded-xl hover:from-blue-700 hover:to-blue-900 disabled:opacity-50 shadow-lg shadow-blue-900/30 transition-all">
            {{ isSubmittingEval ? 'Guardando...' : 'Guardar Evaluacion' }}
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api, { API_ORIGIN } from '../services/api'

import EncargadoReportes from '../components/EncargadoReportes.vue'
import EncargadoHoras from '../components/EncargadoHoras.vue'
import EncargadoUsuarios from '../components/EncargadoUsuarios.vue'

const router = useRouter()
const authStore = useAuthStore()

const resolveStaticUrl = (url) => {
  if (!url) return null
  const s = String(url)
  if (s.startsWith('http://') || s.startsWith('https://')) return s
  if (s.startsWith('/')) return `${API_ORIGIN}${s}`
  return s
}

const seccion = ref('dashboard')
const reportes = ref([])
const isLoadingReportes = ref(true)
const showModalEvaluacion = ref(false)
const reporteSeleccionado = ref(null)
const isSubmittingEval = ref(false)
const evaluacion = ref({ estado: 'VERIFICADO', comentarios: '' })

const usuarios = ref([])
const isLoadingUsuarios = ref(false)
const pasanteSeleccionado = ref(null)

const showModalVer = ref(false)
const showModalEditar = ref(false)
const showModalCrear = ref(false)
const showModalBaja = ref(false)
const historial = ref([])

const cargarHistorial = async (userId) => {
  try {
    const { data } = await api.get('/asistencias/mis-asistencias', { params: { pasante_id: userId } })
    historial.value = data
  } catch (e) { historial.value = [] }
}

const formEditar = ref({ nombres: '', apellidos: '', carnet_identidad: '', email: '' })
const formulario = ref({ nombres: '', apellidos: '', carnet_identidad: '', email: '', celular: '', password: '', rol_id: 3, carrera_id: null })

const isSubmittingEditar = ref(false)
const isSubmittingCrear = ref(false)
const isSubmittingBaja = ref(false)
const isDownloadingPDF = ref(false)
const isDownloadingPeriodo = ref(false)
const showMenuPeriodos = ref(false)
const mensajeErrorEditar = ref('')
const mensajeError = ref('')

const stats = computed(() => {
  const pasantes = usuarios.value.filter(u => String(u.rol || '').toUpperCase() === 'PASANTE')
  const totalPasantes = pasantes.length
  const activos = pasantes.filter(u => u.estado).length
  const inactivos = totalPasantes - activos
  const pctActivos = totalPasantes > 0 ? Math.round((activos / totalPasantes) * 100) : 0
  const totalReportes = reportes.value.length
  const verificados = reportes.value.filter(r => r.estado_encargado === 'VERIFICADO').length
  const rectificados = reportes.value.filter(r => r.estado_encargado === 'RECTIFICADO').length
  const pendientes = reportes.value.filter(r => !r.estado_encargado && !r.estado_admin).length
  return {
    totalPasantes, activos, inactivos, pctActivos, totalReportes, verificados, rectificados, pendientes,
    pctVerificados: totalReportes > 0 ? Math.round((verificados / totalReportes) * 100) : 0,
    pctRectificados: totalReportes > 0 ? Math.round((rectificados / totalReportes) * 100) : 0,
    pctPendientes: totalReportes > 0 ? Math.round((pendientes / totalReportes) * 100) : 0
  }
})

const usernamePreview = computed(() => {
  const n = formulario.value.nombres?.trim()
  const a = formulario.value.apellidos?.trim()
  const ci = formulario.value.carnet_identidad?.trim()
  if (!n || !a || !ci) return ''
  return `${n[0].toLowerCase()}${a[0].toLowerCase()}${ci}`
})

const getIniciales = (nombres, apellidos) => `${nombres?.[0] || ''}${apellidos?.[0] || ''}`.toUpperCase()

const cargarReportes = async () => {
  isLoadingReportes.value = true
  try {
    const { data } = await api.get('/reportes/listar', { timeout: 30000 })
    reportes.value = data
  } catch (e) {
    if (e.response?.status === 401) cerrarSesion()
  } finally { isLoadingReportes.value = false }
}

const cargarUsuarios = async () => {
  isLoadingUsuarios.value = true
  try {
    const { data } = await api.get('/usuarios/listar', { timeout: 30000 })
    usuarios.value = data
  } catch (e) {
    console.error('Error al cargar usuarios:', e)
  } finally { isLoadingUsuarios.value = false }
}

const abrirModalEvaluacion = (reporte) => {
  if (yaRectificado(reporte)) return
  reporteSeleccionado.value = reporte
  evaluacion.value.estado = yaEvaluado(reporte) ? 'RECTIFICADO' : (reporte.estado_encargado || 'VERIFICADO')
  evaluacion.value.comentarios = reporte.comentarios_director || ''
  showModalEvaluacion.value = true
}

const cerrarModalEvaluacion = () => { showModalEvaluacion.value = false; reporteSeleccionado.value = null }

const enviarEvaluacion = async () => {
  if (!evaluacion.value.comentarios?.trim()) { alert('El comentario es obligatorio.'); return }
  if (yaEvaluado(reporteSeleccionado.value) && evaluacion.value.estado !== 'RECTIFICADO') { alert('Este reporte ya fue evaluado.'); return }
  if (yaRectificado(reporteSeleccionado.value)) { alert('Este reporte ya fue rectificado.'); return }
  isSubmittingEval.value = true
  try {
    await api.put(`/reportes/evaluar/${reporteSeleccionado.value.id}`, {
      estado: evaluacion.value.estado,
      comentarios_director: evaluacion.value.comentarios.trim(),
      es_rectificacion: yaEvaluado(reporteSeleccionado.value)
    })
    await cargarReportes()
    cerrarModalEvaluacion()
  } catch { alert('Error al guardar la evaluación.') }
  finally { isSubmittingEval.value = false }
}

const yaEvaluado = (reporte) => { if (!reporte) return false; const e = reporte.estado_encargado || ''; return e !== '' && e !== 'RECTIFICADO' }
const yaRectificado = (reporte) => reporte?.estado_encargado === 'RECTIFICADO'
const evaluarPendiente = () => { const p = reportes.value.find(r => !r.estado_encargado && !r.estado_admin); if (p) abrirModalEvaluacion(p); else alert('No hay reportes pendientes.') }
const abrirModalVer = (user) => { pasanteSeleccionado.value = user; showModalVer.value = true; cargarHistorial(user.id) }
const abrirModalEditar = (user) => { pasanteSeleccionado.value = user; formEditar.value = { nombres: user.nombres, apellidos: user.apellidos, carnet_identidad: user.carnet_identidad || '', email: user.email }; mensajeErrorEditar.value = ''; showModalEditar.value = true }

const guardarEdicion = async () => {
  isSubmittingEditar.value = true; mensajeErrorEditar.value = ''
  try {
    const payload = {}
    Object.entries(formEditar.value).forEach(([k, v]) => { if (v && v.toString().trim() !== '') payload[k] = v })
    await api.put(`/usuarios/editar/${pasanteSeleccionado.value.id}`, payload)
    await cargarUsuarios(); showModalEditar.value = false; alert('Datos actualizados correctamente.')
  } catch (e) { mensajeErrorEditar.value = e.response?.data?.detail || 'Error al guardar.' }
  finally { isSubmittingEditar.value = false }
}

const confirmarCambioEstado = (user) => { pasanteSeleccionado.value = user; showModalBaja.value = true }

const ejecutarCambioEstado = async () => {
  isSubmittingBaja.value = true
  try {
    if (pasanteSeleccionado.value.estado) { await api.delete(`/usuarios/desactivar/${pasanteSeleccionado.value.id}`) }
    else { await api.put(`/usuarios/editar/${pasanteSeleccionado.value.id}`, { estado: true }) }
    await cargarUsuarios(); showModalBaja.value = false
  } catch (e) { alert(e.response?.data?.detail || 'Error al cambiar estado.') }
  finally { isSubmittingBaja.value = false }
}

const toggleMenuPeriodos = () => { showMenuPeriodos.value = !showMenuPeriodos.value }
const descargarPDFPeriodo = async (tipo) => { showMenuPeriodos.value = false }

const abrirModalCrear = () => { formulario.value = { nombres: '', apellidos: '', carnet_identidad: '', email: '', celular: '', password: '', rol_id: 3, carrera_id: authStore.user?.carrera_id }; mensajeError.value = ''; showModalCrear.value = true }

const registrarPasante = async () => {
  isSubmittingCrear.value = true; mensajeError.value = ''
  try {
    await api.post('/usuarios/registro', { ...formulario.value, rol_id: 3, carrera_id: authStore.user?.carrera_id })
    alert('Pasante registrado exitosamente.'); showModalCrear.value = false; await cargarUsuarios()
  } catch (e) { mensajeError.value = e.response?.data?.detail || 'Error al registrar.' }
  finally { isSubmittingCrear.value = false }
}

const cerrarSesion = () => { authStore.logout(); router.push('/') }

onMounted(async () => {
  try {
    await cargarReportes()
    await new Promise(resolve => setTimeout(resolve, 500))
    await cargarUsuarios()
  } catch (e) { console.error('Error al cargar datos iniciales:', e) }
})
</script>