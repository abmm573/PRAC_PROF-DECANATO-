<template>
  <div class="min-h-screen bg-slate-50 font-sans pb-12 selection:bg-red-500 selection:text-white">

    <header class="bg-white border-b border-slate-200 sticky top-0 z-50">
      <div class="absolute top-0 inset-x-0 h-1 bg-gradient-to-r from-blue-900 to-red-700"></div>
      <div class="max-w-[96rem] mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div class="flex justify-between h-16 items-center">
          
          <div class="flex items-center gap-4">
            <div class="w-10 h-10 bg-blue-950 rounded-lg flex items-center justify-center text-white font-black text-[11px] tracking-wider shadow-sm border border-blue-900">
              <span class="text-red-500 text-sm mr-0.5 leading-none">U</span>MSA
            </div>
            <div class="border-l border-slate-300 pl-4 py-1 hidden sm:block">
              <p class="text-[10px] text-red-700 font-black uppercase tracking-widest leading-none mb-1">Facultad de Cs. Sociales</p>
              <p class="text-sm font-extrabold text-slate-800 leading-none tracking-tight">Centro de Mando <span class="text-slate-400 font-medium ml-1">| Admin</span></p>
            </div>
          </div>

          <nav class="hidden lg:flex items-center gap-1.5 bg-slate-100/50 p-1 rounded-xl border border-slate-200">
            <button class="bg-white text-blue-900 px-5 py-2 rounded-lg text-sm font-bold shadow-sm border border-slate-200 flex items-center gap-2">
              <svg class="w-4 h-4 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
              Monitor
            </button>
            <button @click="router.push('/usuarios')" class="text-slate-500 hover:bg-white hover:text-blue-900 hover:shadow-sm px-5 py-2 rounded-lg text-sm font-semibold transition-all">Directorio</button>
            <button @click="router.push('/programas')" class="text-slate-500 hover:bg-white hover:text-blue-900 hover:shadow-sm px-5 py-2 rounded-lg text-sm font-semibold transition-all">Programas</button>
            <button @click="router.push('/carreras')" class="text-slate-500 hover:bg-white hover:text-blue-900 hover:shadow-sm px-5 py-2 rounded-lg text-sm font-semibold transition-all">Carreras</button>
          </nav>

          <div class="flex items-center gap-4">
            <div class="hidden sm:flex flex-col items-end">
              <span class="text-slate-800 text-sm font-bold leading-tight">{{ authStore.user?.nombres }}</span>
              <span class="text-[10px] font-black text-red-600 uppercase tracking-widest">Máxima Autoridad</span>
            </div>
            <button @click="router.push('/perfil')" title="Perfil" class="w-10 h-10 bg-slate-100 rounded-xl flex items-center justify-center text-blue-950 font-black text-sm border border-slate-200 hover:bg-blue-50 hover:text-blue-700 transition-all">
              {{ obtenerIniciales(authStore.user?.nombres, authStore.user?.apellidos) }}
            </button>
            <div class="h-6 w-px bg-slate-200 hidden sm:block"></div>
            <button @click="cerrarSesion" class="flex items-center gap-2 text-sm font-bold text-slate-400 hover:text-red-600 transition-colors group" title="Cerrar Sesión">
              <svg class="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/></svg>
            </button>
          </div>
        </div>
      </div>
    </header>

    <main class="max-w-[96rem] mx-auto py-8 px-4 sm:px-6 lg:px-8 space-y-8">

      <div class="relative bg-blue-950 rounded-[2rem] p-8 shadow-xl overflow-hidden border border-blue-900 flex justify-between items-center">
        <div class="absolute top-0 right-0 w-[30rem] h-[30rem] bg-red-600/20 rounded-full blur-[80px] -translate-y-1/2 translate-x-1/3 pointer-events-none"></div>
        <div class="absolute bottom-0 left-0 w-[20rem] h-[20rem] bg-blue-500/20 rounded-full blur-[60px] translate-y-1/3 -translate-x-1/4 pointer-events-none"></div>
        
        <div class="relative z-10">
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-lg bg-white/10 border border-white/20 backdrop-blur-md mb-4 shadow-sm">
            <span class="w-2 h-2 rounded-full bg-red-400 animate-pulse"></span>
            <p class="text-[10px] font-black text-white uppercase tracking-widest">Autorización Global</p>
          </div>
          <h1 class="text-3xl lg:text-4xl font-black text-white tracking-tight leading-tight">
            Monitor de <span class="text-transparent bg-clip-text bg-gradient-to-r from-red-400 to-red-500">Evaluaciones</span>
          </h1>
          <p class="text-blue-200 text-sm mt-2 font-medium">Supervisa el rendimiento de todas las carreras y emite la resolución final.</p>
        </div>

        <button @click="evaluarSiguienteVerificado" class="hidden md:flex relative z-10 px-8 py-4 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-500 hover:to-red-600 text-white text-sm font-black uppercase tracking-widest rounded-xl shadow-lg shadow-red-900/40 transition-all items-center gap-2 transform hover:-translate-y-0.5">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          Evaluar Siguiente
        </button>
      </div>

      <div class="grid grid-cols-2 lg:grid-cols-4 gap-6">
        <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm hover:shadow-md transition-shadow">
          <div class="flex items-center justify-between mb-4">
            <div class="w-12 h-12 bg-blue-50 rounded-xl flex items-center justify-center text-blue-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/></svg>
            </div>
            <span class="text-[10px] font-black text-blue-600 bg-blue-50 px-2 py-1 rounded uppercase tracking-widest border border-blue-100">GLOBAL</span>
          </div>
          <p class="text-3xl font-black text-slate-800">{{ stats.totalPasantes }}</p>
          <p class="text-xs font-bold text-slate-500 mt-1 uppercase tracking-wider">Pasantes Registrados</p>
        </div>

        <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm hover:shadow-md transition-shadow relative overflow-hidden">
          <div class="absolute bottom-0 inset-x-0 h-1 bg-emerald-500"></div>
          <div class="flex items-center justify-between mb-4">
            <div class="w-12 h-12 bg-emerald-50 rounded-xl flex items-center justify-center text-emerald-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            </div>
            <span class="text-xs font-black text-emerald-600">{{ stats.pctActivos }}%</span>
          </div>
          <p class="text-3xl font-black text-slate-800">{{ stats.activos }}</p>
          <p class="text-xs font-bold text-slate-500 mt-1 uppercase tracking-wider">Pasantes Activos</p>
        </div>

        <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm hover:shadow-md transition-shadow">
          <div class="flex items-center justify-between mb-4">
            <div class="w-12 h-12 bg-indigo-50 rounded-xl flex items-center justify-center text-indigo-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
            </div>
            <span class="text-[10px] font-black text-indigo-600 bg-indigo-50 px-2 py-1 rounded uppercase tracking-widest border border-indigo-100">TOTAL</span>
          </div>
          <p class="text-3xl font-black text-slate-800">{{ stats.totalReportes }}</p>
          <p class="text-xs font-bold text-slate-500 mt-1 uppercase tracking-wider">Reportes Recibidos</p>
        </div>

        <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm hover:shadow-md transition-shadow relative overflow-hidden">
          <div class="absolute bottom-0 inset-x-0 h-1 bg-amber-500"></div>
          <div class="flex items-center justify-between mb-4">
            <div class="w-12 h-12 bg-amber-50 rounded-xl flex items-center justify-center text-amber-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            </div>
            <span class="text-[10px] font-black text-amber-600 bg-amber-50 px-2 py-1 rounded uppercase tracking-widest border border-amber-100">ESPERA</span>
          </div>
          <p class="text-3xl font-black text-slate-800">{{ stats.verificados }}</p>
          <p class="text-xs font-bold text-slate-500 mt-1 uppercase tracking-wider">Por Evaluar (Admin)</p>
        </div>
      </div>

      <div class="grid lg:grid-cols-2 gap-6">
        
        <div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
          <div class="px-6 py-4 border-b border-slate-100">
            <h2 class="text-base font-black text-slate-800 uppercase tracking-tight">Estado de Pasantes</h2>
            <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Distribución a nivel Facultad</p>
          </div>
          <div class="p-6 flex items-center justify-center gap-10">
            <div class="relative w-36 h-36 flex-shrink-0">
              <svg class="w-36 h-36 -rotate-90 drop-shadow-sm" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="40" fill="none" stroke="#f1f5f9" stroke-width="12"/>
                <circle cx="50" cy="50" r="40" fill="none" stroke="#1e3a8a" stroke-width="12" stroke-linecap="round"
                  :stroke-dasharray="2 * 3.1416 * 40"
                  :stroke-dashoffset="(2 * 3.1416 * 40) * (1 - (stats.pctActivos / 100))"
                  class="transition-all duration-1000 ease-out" />
              </svg>
              <div class="absolute inset-0 flex flex-col items-center justify-center">
                <span class="text-2xl font-black text-blue-950">{{ stats.pctActivos }}%</span>
                <span class="text-[9px] font-bold text-slate-400 uppercase tracking-widest">Activos</span>
              </div>
            </div>
            
            <div class="flex-1 space-y-4">
              <div class="flex items-center justify-between p-3 bg-slate-50 rounded-xl border border-slate-100">
                <div class="flex items-center gap-3">
                  <div class="w-3.5 h-3.5 rounded-full bg-blue-900 shadow-sm"></div>
                  <span class="text-xs font-bold text-slate-600 uppercase tracking-wider">Activos</span>
                </div>
                <span class="font-black text-slate-800">{{ stats.activos }}</span>
              </div>
              <div class="flex items-center justify-between p-3 bg-slate-50 rounded-xl border border-slate-100">
                <div class="flex items-center gap-3">
                  <div class="w-3.5 h-3.5 rounded-full bg-slate-200 shadow-sm"></div>
                  <span class="text-xs font-bold text-slate-600 uppercase tracking-wider">Inactivos</span>
                </div>
                <span class="font-black text-slate-800">{{ stats.inactivos }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
          <div class="px-6 py-4 border-b border-slate-100">
            <h2 class="text-base font-black text-slate-800 uppercase tracking-tight">Resolución de Reportes</h2>
            <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Evaluación acumulada</p>
          </div>
          <div class="p-6 space-y-5">
            <div>
              <div class="flex items-center justify-between mb-1.5">
                <div class="flex items-center gap-2">
                  <div class="w-2.5 h-2.5 rounded-full bg-emerald-500"></div>
                  <span class="text-xs font-bold text-slate-700 uppercase tracking-wider">Aprobados</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="text-xs font-black text-slate-800">{{ stats.aprobados }}</span>
                  <span class="text-[10px] font-bold text-slate-400 w-8 text-right">({{ stats.pctAprobados }}%)</span>
                </div>
              </div>
              <div class="h-2.5 bg-slate-100 rounded-full overflow-hidden">
                <div class="h-full bg-emerald-500 rounded-full transition-all duration-1000" :style="{ width: stats.pctAprobados + '%' }"></div>
              </div>
            </div>
            <div>
              <div class="flex items-center justify-between mb-1.5">
                <div class="flex items-center gap-2">
                  <div class="w-2.5 h-2.5 rounded-full bg-red-500"></div>
                  <span class="text-xs font-bold text-slate-700 uppercase tracking-wider">Rechazados</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="text-xs font-black text-slate-800">{{ stats.rechazados }}</span>
                  <span class="text-[10px] font-bold text-slate-400 w-8 text-right">({{ stats.pctRechazados }}%)</span>
                </div>
              </div>
              <div class="h-2.5 bg-slate-100 rounded-full overflow-hidden">
                <div class="h-full bg-red-500 rounded-full transition-all duration-1000" :style="{ width: stats.pctRechazados + '%' }"></div>
              </div>
            </div>
            <div>
              <div class="flex items-center justify-between mb-1.5">
                <div class="flex items-center gap-2">
                  <div class="w-2.5 h-2.5 rounded-full bg-blue-500"></div>
                  <span class="text-xs font-bold text-slate-700 uppercase tracking-wider">Verificados (Espera)</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="text-xs font-black text-slate-800">{{ stats.verificados }}</span>
                  <span class="text-[10px] font-bold text-slate-400 w-8 text-right">({{ stats.pctVerificados }}%)</span>
                </div>
              </div>
              <div class="h-2.5 bg-slate-100 rounded-full overflow-hidden">
                <div class="h-full bg-blue-500 rounded-full transition-all duration-1000" :style="{ width: stats.pctVerificados + '%' }"></div>
              </div>
            </div>
            <div>
              <div class="flex items-center justify-between mb-1.5">
                <div class="flex items-center gap-2">
                  <div class="w-2.5 h-2.5 rounded-full bg-amber-500"></div>
                  <span class="text-xs font-bold text-slate-700 uppercase tracking-wider">Pendientes (Encargado)</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="text-xs font-black text-slate-800">{{ stats.pendientes }}</span>
                  <span class="text-[10px] font-bold text-slate-400 w-8 text-right">({{ stats.pctPendientes }}%)</span>
                </div>
              </div>
              <div class="h-2.5 bg-slate-100 rounded-full overflow-hidden">
                <div class="h-full bg-amber-500 rounded-full transition-all duration-1000" :style="{ width: stats.pctPendientes + '%' }"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        <div class="px-6 py-4 border-b border-slate-100 bg-slate-50/50">
          <h2 class="text-base font-black text-slate-800 uppercase tracking-tight">Accos Rápidos</h2>
        </div>
        <div class="p-6 grid grid-cols-2 md:grid-cols-4 gap-4">
          <button @click="router.push('/usuarios')" class="group p-5 rounded-xl border border-slate-200 hover:border-blue-300 hover:bg-blue-50/50 transition-all text-left">
            <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mb-3 group-hover:bg-blue-200 transition-colors">
              <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/></svg>
            </div>
            <p class="font-bold text-slate-700 text-sm group-hover:text-blue-700">Ver Pasantes</p>
            <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-1">{{ stats.totalPasantes }} Registrados</p>
          </button>
          
          <button @click="router.push('/programas')" class="group p-5 rounded-xl border border-slate-200 hover:border-indigo-300 hover:bg-indigo-50/50 transition-all text-left">
            <div class="w-10 h-10 bg-indigo-100 rounded-lg flex items-center justify-center mb-3 group-hover:bg-indigo-200 transition-colors">
              <svg class="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
            </div>
            <p class="font-bold text-slate-700 text-sm group-hover:text-indigo-700">Programas</p>
            <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-1">Gestionar</p>
          </button>
          
          <button @click="router.push('/carreras')" class="group p-5 rounded-xl border border-slate-200 hover:border-emerald-300 hover:bg-emerald-50/50 transition-all text-left">
            <div class="w-10 h-10 bg-emerald-100 rounded-lg flex items-center justify-center mb-3 group-hover:bg-emerald-200 transition-colors">
              <svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7"/></svg>
            </div>
            <p class="font-bold text-slate-700 text-sm group-hover:text-emerald-700">Carreras</p>
            <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-1">Catálogo</p>
          </button>
          
          <button @click="evaluarSiguienteVerificado" class="group p-5 rounded-xl border border-slate-200 hover:border-red-300 hover:bg-red-50/50 transition-all text-left">
            <div class="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center mb-3 group-hover:bg-red-200 transition-colors">
              <svg class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            </div>
            <p class="font-bold text-slate-700 text-sm group-hover:text-red-700">Evaluar</p>
            <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-1">{{ stats.verificados }} Esperando</p>
          </button>
        </div>
      </div>

      <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-3">
        <div class="flex flex-col lg:flex-row justify-between items-center gap-4">
          
          <div class="flex w-full lg:w-auto p-1.5 bg-slate-100 rounded-xl overflow-x-auto shadow-inner">
            <button @click="filtroActual = 'TODOS'" :class="filtroActual === 'TODOS' ? 'bg-white text-blue-950 shadow-sm' : 'text-slate-500 hover:text-slate-800'" class="px-5 py-2.5 rounded-lg text-xs font-black uppercase tracking-wider transition-all whitespace-nowrap">
              Todos
            </button>
            <button @click="filtroActual = 'VERIFICADO'" :class="filtroActual === 'VERIFICADO' ? 'bg-blue-600 text-white shadow-sm' : 'text-slate-500 hover:text-blue-700'" class="px-5 py-2.5 rounded-lg text-xs font-black uppercase tracking-wider transition-all whitespace-nowrap flex items-center gap-2">
              Para Aprobar
              <span v-if="totalVerificados > 0" :class="filtroActual === 'VERIFICADO' ? 'bg-white text-blue-700' : 'bg-blue-100 text-blue-700'" class="py-0.5 px-2 rounded-full text-[10px]">{{ totalVerificados }}</span>
            </button>
            <button @click="filtroActual = 'PENDIENTE'" :class="filtroActual === 'PENDIENTE' ? 'bg-amber-500 text-white shadow-sm' : 'text-slate-500 hover:text-amber-600'" class="px-5 py-2.5 rounded-lg text-xs font-black uppercase tracking-wider transition-all whitespace-nowrap">
              En revisión
            </button>
            <button @click="filtroActual = 'APROBADO'" :class="filtroActual === 'APROBADO' ? 'bg-emerald-500 text-white shadow-sm' : 'text-slate-500 hover:text-emerald-600'" class="px-5 py-2.5 rounded-lg text-xs font-black uppercase tracking-wider transition-all whitespace-nowrap">
              Histórico
            </button>
          </div>

          <div class="flex w-full lg:w-auto items-center gap-3">
            <div class="relative w-full lg:w-80">
              <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
              </div>
              <input v-model="searchQuery" type="text" placeholder="Buscar pasante, actividad..." 
                class="block w-full pl-11 pr-4 py-3 border border-slate-200 rounded-xl bg-slate-50 text-sm font-bold focus:bg-white focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all"/>
            </div>
            <button @click="recargarDatos" class="p-3 bg-white border border-slate-200 text-slate-400 hover:text-blue-600 hover:border-blue-300 rounded-xl shadow-sm transition-all" title="Actualizar datos">
              <svg class="w-5 h-5" :class="{'animate-spin text-blue-600': isLoading}" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
            </button>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-2xl shadow-md border border-slate-200 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-slate-200">
            <thead class="bg-slate-50">
              <tr>
                <th class="px-6 py-4 text-left text-[10px] font-black text-slate-500 uppercase tracking-widest">Pasante / Fecha</th>
                <th class="px-6 py-4 text-left text-[10px] font-black text-slate-500 uppercase tracking-widest w-1/3">Actividades Realizadas</th>
                <th class="px-6 py-4 text-center text-[10px] font-black text-slate-500 uppercase tracking-widest">Desglose (Hrs)</th>
                <th class="px-6 py-4 text-center text-[10px] font-black text-slate-500 uppercase tracking-widest">Resolución</th>
                <th class="px-6 py-4 text-right text-[10px] font-black text-slate-500 uppercase tracking-widest">Acciones</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-slate-100">
              
              <tr v-if="isLoading">
                <td colspan="5" class="px-6 py-24 text-center">
                  <div class="flex flex-col items-center justify-center text-blue-900">
                    <svg class="animate-spin h-10 w-10 mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                    <p class="font-black tracking-widest uppercase text-xs">Recuperando registros...</p>
                  </div>
                </td>
              </tr>

              <tr v-else-if="filteredReportes.length === 0">
                <td colspan="5" class="px-6 py-24 text-center text-slate-400">
                  <div class="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-4 border border-slate-200">
                    <svg class="w-8 h-8 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
                  </div>
                  <p class="font-black text-slate-600 text-lg">No hay reportes aquí</p>
                  <p class="text-sm mt-1 font-medium">Ajusta los filtros de búsqueda para ver resultados.</p>
                </td>
              </tr>

              <tr v-else v-for="reporte in filteredReportes" :key="reporte.id" class="hover:bg-blue-50/40 transition-colors group">
                <td class="px-6 py-5 whitespace-nowrap">
                  <div class="flex items-center gap-4">
                    <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-slate-100 to-slate-200 flex items-center justify-center text-blue-900 font-black text-sm border border-slate-300 shadow-sm shrink-0">
                      {{ obtenerIniciales(reporte.nombre_pasante, '') }}
                    </div>
                    <div class="flex flex-col">
                      <span class="text-sm font-black text-blue-950">{{ reporte.nombre_pasante || 'Desconocido' }}</span>
                      <span class="text-[11px] font-bold text-slate-400 mt-0.5 uppercase tracking-wider flex items-center gap-1.5">
                        <svg class="w-3 h-3 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                        {{ formatearSoloFecha(reporte.creado_en) }}
                      </span>
                    </div>
                  </div>
                </td>
                
                <td class="px-6 py-5">
                  <p class="text-xs text-slate-700 font-medium line-clamp-2 leading-relaxed" :title="reporte.actividades_realizadas">
                    {{ reporte.actividades_realizadas }}
                  </p>
                </td>

                <td class="px-6 py-5 whitespace-nowrap text-center">
                  <div class="inline-flex flex-col items-center bg-white px-3 py-1.5 rounded-lg border border-slate-200 shadow-sm">
                    <span class="text-sm font-black text-slate-800 border-b border-slate-100 pb-1 mb-1 w-full text-center">
                      {{ reporte.horas_trabajadas ?? '0' }} <span class="text-[9px] text-slate-400 font-bold uppercase tracking-widest">Hoy</span>
                    </span>
                    <div class="flex gap-2 text-[10px]">
                      <span class="font-black text-blue-600" title="Verificadas">{{ reporte.horas_verificadas ?? '0' }}v</span>
                      <span class="text-slate-200">|</span>
                      <span class="font-black text-emerald-600" title="Aprobadas">{{ reporte.horas_validadas ?? '0' }}a</span>
                    </div>
                  </div>
                </td>

                <td class="px-6 py-5 whitespace-nowrap text-center">
                  <span :class="estadoBadgeClass(reporte.estado_encargado)" class="px-3 py-1.5 inline-flex items-center gap-2 text-[10px] font-black rounded-lg uppercase tracking-widest border shadow-sm">
                    <span class="w-1.5 h-1.5 rounded-full" :class="estadoDotClass(reporte.estado_encargado)"></span>
                    {{ reporte.estado_encargado || 'PENDIENTE' }}
                  </span>
                </td>

                <td class="px-6 py-4 whitespace-nowrap text-right">
  <div class="flex justify-end gap-3 items-center">
    

    <button @click.stop="abrirHistorial(reporte)" 
      class="p-2 text-slate-400 hover:text-blue-600 hover:bg-blue-50 rounded-xl transition-all border border-transparent hover:border-blue-100" 
      title="Ver Auditoría">
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
      </svg>
    </button>

    <button @click.stop="abrirModalEvaluar(reporte)"
      :class="(reporte.estado_admin === 'APROBADO' || reporte.estado_admin === 'RECHAZADO') 
        ? 'bg-slate-100 text-slate-400 cursor-not-allowed border-slate-200' 
        : (reporte.estado_encargado || '').toUpperCase() === 'VERIFICADO' 
          ? 'bg-blue-600 text-white hover:bg-blue-700 shadow-lg shadow-blue-200 border-transparent' 
          : 'bg-white text-slate-600 hover:bg-slate-50 border-slate-200'"
      :disabled="reporte.estado_admin === 'APROBADO' || reporte.estado_admin === 'RECHAZADO'"
      class="px-4 py-2 rounded-xl border text-[10px] font-black uppercase tracking-widest transition-all shadow-sm">
      {{ (reporte.estado_admin === 'APROBADO' || reporte.estado_admin === 'RECHAZADO') 
        ? 'Evaluado' 
        : (reporte.estado_encargado || '').toUpperCase() === 'VERIFICADO' ? 'Aprobar' : 'Ver' }}
    </button>

      <div class="w-px h-3 bg-red-200"></div>
      <button @click.stop="descargarPDFSemanal(reporte)" class="px-2.5 py-1.5 text-[9px] font-black uppercase tracking-widest text-red-600 hover:bg-red-600 hover:text-white rounded-lg transition-colors" title="Reporte Semanal">
        Sem
      </button>
      <div class="w-px h-3 bg-red-200"></div>
      <button @click.stop="descargarPDFMensual(reporte)" class="px-2.5 py-1.5 text-[9px] font-black uppercase tracking-widest text-red-600 hover:bg-red-600 hover:text-white rounded-lg transition-colors" title="Reporte Mensual">
        Mes
      </button>

  </div>
</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>

    <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center bg-blue-950/80 px-4 backdrop-blur-sm overflow-y-auto">
      <div class="relative bg-white rounded-3xl shadow-2xl w-full max-w-xl my-8 overflow-hidden transform transition-all border border-blue-100">
        
        <div class="px-8 py-5 bg-gradient-to-r from-blue-950 to-blue-900 flex justify-between items-center border-b-4 border-red-600">
          <h3 class="text-lg font-black text-white tracking-widest uppercase flex items-center gap-2">
            <svg class="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            Resolución Oficial
          </h3>
          <button @click="showModal = false" class="text-blue-300 hover:text-white transition-colors bg-white/10 p-1.5 rounded-lg"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12"/></svg></button>
        </div>

        <div class="p-8">
          <div v-if="false" class="mb-6 bg-amber-50 border border-amber-200 p-4 rounded-xl flex gap-3 text-amber-800 text-sm shadow-inner">
            <svg class="w-6 h-6 shrink-0 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
            <div>
              <p class="font-bold mb-0.5">Acción Restringida</p>
              <p class="text-xs">El reporte está "PENDIENTE". El Encargado de la carrera debe verificarlo primero.</p>
            </div>
          </div>
          
          <div class="mb-6 bg-slate-50 p-5 rounded-2xl border border-slate-200">
             <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Datos del Pasante</p>
             <p class="text-xl font-black text-blue-950">{{ reporteAEvaluar?.nombre_pasante }}</p>
             <p class="text-xs text-red-600 font-bold mb-4 mt-0.5">{{ reporteAEvaluar?.proyecto_nombre || 'Sin proyecto asignado' }}</p>
             
             <div class="bg-white p-4 rounded-xl border border-slate-100 shadow-sm">
               <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-2">Actividades</p>
               <p class="text-sm text-slate-700 font-medium leading-relaxed">{{ reporteAEvaluar?.actividades_realizadas }}</p>
             </div>
          </div>

          <form @submit.prevent="guardarEvaluacion" class="space-y-6">
            <div>
              <label class="block text-xs font-black text-blue-950 uppercase tracking-widest mb-3">Decisión de Autoridad</label>
              <div class="flex gap-4">
                <label class="flex-1 cursor-pointer">
                  <input type="radio" v-model="formEvaluacion.estado" value="APROBADO" class="peer sr-only">
                  <div class="text-center p-4 rounded-2xl border-2 border-slate-200 peer-checked:border-emerald-500 peer-checked:bg-emerald-50 text-slate-400 peer-checked:text-emerald-700 transition-all peer-disabled:opacity-50 peer-disabled:cursor-not-allowed bg-white shadow-sm hover:shadow-md">
                    <p class="font-black text-sm uppercase tracking-widest">Aprobar</p>
                    <p class="text-[10px] font-bold mt-1">Validar Horas</p>
                  </div>
                </label>
                <label class="flex-1 cursor-pointer">
                  <input type="radio" v-model="formEvaluacion.estado" value="RECHAZADO" class="peer sr-only">
                  <div class="text-center p-4 rounded-2xl border-2 border-slate-200 peer-checked:border-red-500 peer-checked:bg-red-50 text-slate-400 peer-checked:text-red-700 transition-all bg-white shadow-sm hover:shadow-md">
                    <p class="font-black text-sm uppercase tracking-widest">Rechazar</p>
                    <p class="text-[10px] font-bold mt-1">Anular Reporte</p>
                  </div>
                </label>
              </div>
            </div>
            <div>
              <div class="flex justify-between items-end mb-2">
                <label class="block text-xs font-black text-blue-950 uppercase tracking-widest">Comentario / Justificación</label>
                <span class="text-[9px] font-black text-white bg-red-600 px-2 py-0.5 rounded uppercase tracking-widest">Obligatorio</span>
              </div>
              <textarea v-model="formEvaluacion.comentarios_director" rows="3" required class="w-full border border-slate-300 rounded-xl p-4 focus:border-blue-600 focus:ring-2 focus:ring-blue-200 outline-none text-sm font-medium resize-none shadow-inner bg-slate-50 focus:bg-white transition-all" placeholder="Redacta la observación oficial..."></textarea>
            </div>
            
            <div v-if="mensajeError" class="text-red-700 bg-red-50 p-4 text-sm rounded-xl border border-red-200 font-bold flex items-center gap-2">
              <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
              {{ mensajeError }}
            </div>

            <div class="flex justify-end gap-3 pt-4 border-t border-slate-100">
              <button type="button" @click="showModal = false" class="px-6 py-3 border border-slate-300 rounded-xl text-slate-600 text-sm font-bold hover:bg-slate-50 transition-colors">Cancelar</button>
              <button type="submit" :disabled="isSubmitting || !formEvaluacion.comentarios_director.trim()" class="px-8 py-3 bg-gradient-to-r from-blue-800 to-blue-950 text-white rounded-xl text-sm font-black uppercase tracking-widest hover:from-blue-700 hover:to-blue-900 disabled:opacity-50 flex items-center gap-2 shadow-lg shadow-blue-900/30 transition-all">
                {{ isSubmitting ? 'Procesando...' : 'Confirmar' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div v-if="showHistorialModal" class="fixed inset-0 z-[100] flex items-center justify-center bg-slate-900/80 px-4 overflow-y-auto py-10">
  <div class="relative bg-white rounded-3xl shadow-2xl w-full max-w-2xl overflow-hidden flex flex-col max-h-full border border-slate-200 animate-in fade-in duration-200">
    
    <div class="px-8 py-5 bg-slate-50 border-b border-slate-200 flex justify-between items-center shrink-0">
      <div>
        <h3 class="text-lg font-black text-blue-950 uppercase tracking-widest">Auditoría del Registro</h3>
        <p class="text-[10px] font-bold text-slate-400 mt-0.5">{{ historialTitulo }}</p>
      </div>
      <div class="flex items-center gap-2">
        <!-- Botón de descarga PDF -->
        
        <button @click="showHistorialModal = false" class="p-2 text-slate-400 hover:text-red-600 bg-white border border-slate-200 rounded-xl shadow-sm transition-all hover:rotate-90">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>
    </div>

    <div class="p-8 overflow-y-auto custom-scrollbar bg-slate-50/30">
      <div v-if="isLoadingHistorial" class="py-12 text-center text-blue-900 font-bold uppercase tracking-widest text-xs">
        Sincronizando trazabilidad...
      </div>
      <div v-else-if="historialItems.length === 0" class="py-12 text-center font-bold text-slate-400 border border-dashed border-slate-300 rounded-2xl bg-white shadow-inner">
        No hay movimientos registrados.
      </div>
      
      <div v-else class="space-y-6 relative before:absolute before:inset-y-0 before:left-5 before:w-0.5 before:bg-slate-200">
        <div v-for="h in historialItems" :key="h.id" class="relative pl-12 group">
          <div class="absolute left-3 top-1 w-4 h-4 rounded-full border-4 border-white bg-blue-600 shadow-sm z-10"></div>
          
          <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm group-hover:border-blue-300 group-hover:shadow-md transition-all">
            <div class="flex justify-between items-center mb-3 pb-3 border-b border-slate-100">
              <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest">{{ formatearFechaHora(h.creado_en) }}</span>
              <span :class="estadoBadgeClass(h.estado_nuevo)" class="px-2 py-0.5 rounded text-[9px] font-black uppercase tracking-widest border">
                {{ h.estado_nuevo }}
              </span>
            </div>
            <p class="font-black text-sm text-blue-950 flex items-center gap-2 mb-2">
               <svg class="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
               {{ h.actor_nombre }}
            </p>
            <div class="bg-slate-50 p-3 rounded-xl border border-slate-100 italic text-xs text-slate-600 font-medium leading-relaxed">
              "{{ h.comentarios }}"
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="px-8 py-4 bg-white border-t border-slate-100 flex justify-end shrink-0">
       <button @click="showHistorialModal = false" class="px-6 py-2.5 bg-slate-900 text-white rounded-xl text-xs font-black uppercase tracking-widest hover:bg-slate-800 transition-all shadow-lg">Cerrar</button>
    </div>
  </div>
</div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

const router    = useRouter()
const authStore = useAuthStore()

const reportes     = ref([])
const usuarios     = ref([])
const searchQuery  = ref('')
const filtroActual = ref('TODOS')
const isLoading    = ref(true)

const showModal    = ref(false)
const isSubmitting = ref(false)
const mensajeError = ref('')
const reporteAEvaluar = ref(null)
const formEvaluacion  = ref({ estado: 'APROBADO', comentarios_director: '' })

const showHistorialModal = ref(false)
const historialItems = ref([])
const isLoadingHistorial = ref(false)
const errorHistorial = ref('')
const historialTitulo = ref('')

// ESTADÍSTICAS GLOBALES
const stats = computed(() => {
  const pasantes = usuarios.value.filter(u => u.rol === 'PASANTE')
  const totalPasantes = pasantes.length
  const activos = pasantes.filter(u => u.estado).length
  const inactivos = totalPasantes - activos
  const pctActivos = totalPasantes > 0 ? Math.round((activos / totalPasantes) * 100) : 0

  const totalReportes = reportes.value.length
  const aprobados = reportes.value.filter(r => r.estado_admin === 'APROBADO').length
  const rechazados = reportes.value.filter(r => r.estado_admin === 'RECHAZADO' || r.estado_encargado === 'RECHAZADO').length
  const pendientes = reportes.value.filter(r => !r.estado_encargado && !r.estado_admin).length
  const verificados = reportes.value.filter(r => r.estado_encargado === 'VERIFICADO').length

  return {
    totalPasantes, activos, inactivos, pctActivos,
    totalReportes, aprobados, rechazados, pendientes, verificados,
    pctAprobados: pct(aprobados, totalReportes),
    pctVerificados: pct(verificados, totalReportes),
    pctRechazados: pct(rechazados, totalReportes),
    pctPendientes: pct(pendientes, totalReportes)
  }
})

const totalPendientes = computed(() => stats.value.pendientes)
const totalVerificados = computed(() => stats.value.verificados)
const totalAprobados  = computed(() => stats.value.aprobados)

const pct = (valor, total) => {
  if (total === 0) return 0;
  return Math.round((valor / total) * 100);
}

const obtenerIniciales = (nombres, apellidos) => {
  const n = nombres ? nombres.trim().charAt(0) : ''
  const a = apellidos ? apellidos.trim().charAt(0) : ''
  if (!a && nombres) return nombres.substring(0, 2).toUpperCase()
  return (n + a).toUpperCase() || 'A'
}

const filteredReportes = computed(() => {
  let resultado = reportes.value
  if (filtroActual.value !== 'TODOS') {
    if (filtroActual.value === 'PENDIENTE') {
      resultado = resultado.filter(r => !r.estado_encargado && !r.estado_admin)
    } else if (filtroActual.value === 'VERIFICADO') {
      resultado = resultado.filter(r => r.estado_encargado === 'VERIFICADO')
    } else if (filtroActual.value === 'APROBADO') {
      resultado = resultado.filter(r => r.estado_admin === 'APROBADO')
    } else if (filtroActual.value === 'RECHAZADO') {
      resultado = resultado.filter(r => r.estado_admin === 'RECHAZADO' || r.estado_encargado === 'RECHAZADO')
    }
  }
  if (searchQuery.value) {
    const lower = searchQuery.value.toLowerCase()
    resultado = resultado.filter(r =>
      (r.nombre_pasante || '').toLowerCase().includes(lower) ||
      (r.proyecto_nombre || '').toLowerCase().includes(lower) ||
      (r.actividades_realizadas || '').toLowerCase().includes(lower) ||
      (r.estado_encargado || '').toLowerCase().includes(lower) ||
      (r.estado_admin || '').toLowerCase().includes(lower)
    )
  }
  return resultado
})

const estadoBadgeClass = (estado) => {
  if (estado === 'APROBADO')  return 'bg-emerald-50 text-emerald-700 border-emerald-200'
  if (estado === 'VERIFICADO') return 'bg-blue-50 text-blue-700 border-blue-200'
  if (estado === 'RECHAZADO') return 'bg-red-50 text-red-700 border-red-200'
  return 'bg-amber-50 text-amber-700 border-amber-200'
}

const estadoDotClass = (estado) => {
  if (estado === 'APROBADO') return 'bg-emerald-500'
  if (estado === 'VERIFICADO') return 'bg-blue-500'
  if (estado === 'RECHAZADO') return 'bg-red-500'
  return 'bg-amber-500'
}

onMounted(async () => {
  await recargarDatos()
})

const recargarDatos = async () => {
  isLoading.value = true
  try {
    await Promise.all([cargarReportes(), cargarUsuarios()])
  } finally {
    isLoading.value = false
  }
}

const cargarReportes = async () => {
  try {
    const response = await api.get('/reportes/listar')
    reportes.value = response.data
  } catch (error) {
    console.error('Error al cargar reportes:', error)
  }
}

const cargarUsuarios = async () => {
  try {
    const response = await api.get('/usuarios/listar')
    usuarios.value = response.data
  } catch (error) {
    console.error('Error al cargar usuarios:', error)
  }
}

const evaluarSiguienteVerificado = () => {
  const listoParaAprobar = reportes.value.find(r => r.estado_encargado === 'VERIFICADO')
  if (listoParaAprobar) abrirModalEvaluar(listoParaAprobar)
  else alert('No hay reportes verificados listos para aprobar.')
}

const abrirModalEvaluar = (reporte) => {
  // Verificar si el reporte ya fue evaluado por el administrador
  if (reporte.estado_admin && (reporte.estado_admin === 'APROBADO' || reporte.estado_admin === 'RECHAZADO')) {
    alert('Este reporte ya fue evaluado por el administrador y no puede ser modificado.')
    return
  }
  
  reporteAEvaluar.value = reporte
  // Set initial state based on user role
  const userStr = localStorage.getItem('user') || '{}'
  const user = JSON.parse(userStr)
  const userRol = user?.rol?.nombre || ''
  const initialState = userRol === 'ENCARGADO' ? 'VERIFICADO' : 'APROBADO'
  
  // Cargar comentarios existentes si el reporte ya fue evaluado por el admin
  let comentarioExistente = ''
  if (userRol === 'ADMINISTRADOR' && reporte.estado_admin) {
    // Extraer solo los comentarios del administrador
    const todosComentarios = reporte.comentarios_director || ''
    const lineasComentarios = todosComentarios.split('\n\n')
    const comentarioAdmin = lineasComentarios.find(linea => linea.includes('[ADMINISTRADOR]'))
    if (comentarioAdmin) {
      // Quitar el prefijo [ADMINISTRADOR] para mostrar solo el contenido
      comentarioExistente = comentarioAdmin.replace('[ADMINISTRADOR] ', '').trim()
    }
  }
  
  formEvaluacion.value = { 
    estado: reporte.estado_admin || initialState, 
    comentarios_director: comentarioExistente, 
    es_rectificacion: false 
  }
  mensajeError.value = ''
  showModal.value = true
}

const guardarEvaluacion = async () => {
  if (!formEvaluacion.value.comentarios_director?.trim()) {
    mensajeError.value = 'El comentario es obligatorio para mantener la trazabilidad.'
    return
  }
  
  isSubmitting.value = true; mensajeError.value = ''
  try {
    const response = await api.put(`/reportes/evaluar/${reporteAEvaluar.value.id}`, {
      estado: formEvaluacion.value.estado,
      comentarios_director: formEvaluacion.value.comentarios_director.trim(),
      es_rectificacion: formEvaluacion.value.es_rectificacion,
    })
    showModal.value = false
    await recargarDatos()
  } catch (error) {
    mensajeError.value = error.response?.data?.detail || 'Error al evaluar.'
  } finally {
    isSubmitting.value = false
  }
}

const formatearSoloFecha = (dt) => dt ? new Date(dt).toLocaleDateString('es-BO', { day: '2-digit', month: 'short', year: 'numeric' }) : '—'
const formatearFechaHora = (dt) => dt ? new Date(dt).toLocaleString('es-BO', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' }) : '—'

const abrirHistorial = async (reporte) => {
  reporteAEvaluar.value = reporte
  showHistorialModal.value = true
  historialItems.value = []
  errorHistorial.value = ''
  historialTitulo.value = `Reporte de ${reporte?.nombre_pasante} (${formatearSoloFecha(reporte?.creado_en)})`
  isLoadingHistorial.value = true
  try {
    const { data } = await api.get(`/reportes/historial/${reporte.id}`)
    historialItems.value = data || []
  } catch (e) {
    errorHistorial.value = 'No se pudo cargar la auditoría.'
  } finally {
    isLoadingHistorial.value = false
  }
}

// Función para descargar PDF del reporte
const descargarPdfReporte = async (reporte) => {
  if (!reporte) return
  
  try {
    // Obtener la fecha del reporte para determinar el tipo de reporte
    const fechaReporte = new Date(reporte.fecha)
    const diaSem = (fechaReporte.getDay() + 6) % 7
    const lunes = new Date(fechaReporte); lunes.setDate(fechaReporte.getDate() - diaSem)
    const anio = lunes.getFullYear()
    const semana = isoSemana(lunes)
    
    // Descargar PDF diario del reporte específico
    const url = `/asistencias/reporte-pdf/diario?reporte_id=${reporte.id}`
    const filename = `reporte_diario_${reporte.id}_${fechaReporte.toISOString().split('T')[0]}.pdf`
    
    const response = await api.get(url, { responseType: 'blob' })
    const blob = new Blob([response.data], { type: 'application/pdf' })
    const blobUrl = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = blobUrl
    link.setAttribute('download', filename)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(blobUrl)
    
  } catch (error) {
    console.error('Error descargando PDF:', error)
    alert('Error al descargar el PDF. Intenta nuevamente.')
  }
}

// Función auxiliar para calcular semana ISO
const isoSemana = (date) => {
  const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()))
  const dayNum = d.getUTCDay() || 7
  d.setUTCDate(d.getUTCDate() + 4 - dayNum)
  const yearStart = new Date(Date.UTC(d.getUTCFullYear(),0,1))
  return Math.ceil((((d - yearStart) / 86400000) + 1)/7)
}
const procesarDescarga = (data, filename) => {
  const blob = new Blob([data], { type: 'application/pdf' });
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', filename);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
}

const descargarPDFDiario = async (reporte) => {
  try {
    const response = await api.get(`/reportes/descargar/${reporte.id}`, { responseType: 'blob' });
    const fecha = new Date(reporte.creado_en || Date.now()).toISOString().slice(0, 10);
    procesarDescarga(response.data, `Reporte_Diario_${fecha}_${reporte.nombre_pasante.replace(/\s+/g, '_')}.pdf`);
  } catch (error) {
    alert('No se pudo descargar el reporte diario.');
  }
}

const descargarPDFSemanal = async (reporte) => {
  try {
    if (!reporte.pasante_id) return alert("Error: Faltan datos del pasante. Refresca la página.");
    
    // Calcular año y número de semana (ISO Week)
    const date = new Date(reporte.creado_en || Date.now());
    const anio = date.getFullYear();
    const target = new Date(date.valueOf());
    const dayNr = (date.getDay() + 6) % 7;
    target.setDate(target.getDate() - dayNr + 3);
    const firstThursday = target.valueOf();
    target.setMonth(0, 1);
    if (target.getDay() !== 4) target.setMonth(0, 1 + ((4 - target.getDay()) + 7) % 7);
    const semana = 1 + Math.ceil((firstThursday - target) / 604800000);

    const response = await api.get(`/reportes/admin/pdf/semanal/${reporte.pasante_id}?anio=${anio}&semana=${semana}`, { responseType: 'blob' });
    procesarDescarga(response.data, `Reporte_Semanal_Sem${semana}_${anio}_${reporte.nombre_pasante.replace(/\s+/g, '_')}.pdf`);
  } catch (error) {
    alert('No se pudo descargar el reporte semanal.');
  }
}

const descargarPDFMensual = async (reporte) => {
  try {
    if (!reporte.pasante_id) return alert("Error: Faltan datos del pasante. Refresca la página.");
    
    // Calcular año y mes
    const date = new Date(reporte.creado_en || Date.now());
    const anio = date.getFullYear();
    const mes = date.getMonth() + 1; // getMonth es 0-11, sumamos 1

    const response = await api.get(`/reportes/admin/pdf/mensual/${reporte.pasante_id}?anio=${anio}&mes=${mes}`, { responseType: 'blob' });
    procesarDescarga(response.data, `Reporte_Mensual_Mes${mes}_${anio}_${reporte.nombre_pasante.replace(/\s+/g, '_')}.pdf`);
  } catch (error) {
    alert('No se pudo descargar el reporte mensual.');
  }
}

const cerrarSesion = () => { authStore.logout(); router.push('/login') }
</script>
<style scoped>
.custom-scrollbar::-webkit-scrollbar { width: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
</style>