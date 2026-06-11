<template>
  <div class="min-h-screen bg-slate-100 font-sans pb-12 selection:bg-red-500 selection:text-white">

    <header class="bg-blue-950 border-b-4 border-red-700 sticky top-0 z-50 shadow-2xl">
      <div class="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-5 pointer-events-none"></div>
      <div class="max-w-[96rem] mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div class="flex justify-between h-16 items-center">
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 bg-gradient-to-br from-white to-slate-200 rounded-xl flex items-center justify-center text-blue-950 font-black text-xs shadow-lg border border-white/20">
              <span class="text-red-700 text-lg mr-0.5 leading-none">U</span>MSA
            </div>
            <div class="border-l-2 border-white/10 pl-4 py-1 hidden sm:block">
              <p class="text-[10px] text-red-400 font-black uppercase tracking-widest leading-none mb-1">Facultad de Cs. Sociales</p>
              <p class="text-sm font-extrabold text-white leading-none tracking-tight">Centro de Mando <span class="text-blue-300/50 font-medium ml-1">| Admin</span></p>
            </div>
          </div>
          <nav class="hidden lg:flex items-center gap-1.5 bg-blue-900/50 p-1 rounded-xl border border-white/5">
            <button @click="router.push('/admin')" class="text-blue-200 hover:bg-blue-800/50 hover:text-white px-5 py-2 rounded-lg text-sm font-semibold transition-all">Monitor</button>
            <button class="bg-blue-800 text-white px-5 py-2 rounded-lg text-sm font-bold shadow-md flex items-center gap-2">
              <svg class="w-4 h-4 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/></svg>
              Directorio
            </button>
            <button @click="router.push('/programas')" class="text-blue-200 hover:bg-blue-800/50 hover:text-white px-5 py-2 rounded-lg text-sm font-semibold transition-all">Programas</button>
            <button @click="router.push('/carreras')" class="text-blue-200 hover:bg-blue-800/50 hover:text-white px-5 py-2 rounded-lg text-sm font-semibold transition-all">Carreras</button>
          </nav>
          <div class="flex items-center gap-4">
            <div class="hidden sm:flex flex-col items-end">
              <span class="text-white text-sm font-bold leading-tight">{{ authStore.user?.nombres }}</span>
              <span class="text-[10px] font-black text-red-400 uppercase tracking-widest">Máxima Autoridad</span>
            </div>
            <button @click="router.push('/perfil')" class="w-10 h-10 bg-gradient-to-br from-red-600 to-red-800 rounded-xl flex items-center justify-center text-white font-bold text-sm border border-red-500 hover:shadow-lg hover:shadow-red-600/30 transition-all">{{ obtenerIniciales(authStore.user?.nombres, authStore.user?.apellidos) }}</button>
            <div class="h-6 w-px bg-white/10 hidden sm:block"></div>
            <button @click="cerrarSesion" class="text-blue-300 hover:text-red-400 transition-colors"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/></svg></button>
          </div>
        </div>
      </div>
    </header>

    <main class="max-w-[96rem] mx-auto py-8 px-4 sm:px-6 lg:px-8 space-y-8">
      
      <div class="flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div>
          <div class="inline-flex items-center gap-2 px-2.5 py-1 rounded-md bg-blue-50 border border-blue-100 mb-3">
            <svg class="w-3.5 h-3.5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/></svg>
            <p class="text-[10px] font-bold text-blue-800 uppercase tracking-widest">Gestión de Accesos</p>
          </div>
          <h1 class="text-4xl font-black text-slate-800 tracking-tight">Directorio Institucional</h1>
          <p class="text-slate-500 text-sm mt-2 max-w-xl">Administra las cuentas, roles y estados de los estudiantes y el personal administrativo.</p>
        </div>
        <button @click="abrirModalCrear" class="bg-gradient-to-r from-red-600 to-red-700 hover:from-red-500 hover:to-red-600 text-white px-6 py-3.5 rounded-xl shadow-lg shadow-red-900/20 font-black uppercase tracking-widest text-sm flex items-center justify-center gap-2 transition-all transform hover:-translate-y-0.5">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4"/></svg>
          Nuevo Usuario
        </button>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="bg-white border border-slate-200 p-6 rounded-2xl shadow-sm flex flex-col justify-center relative overflow-hidden">
          <div class="absolute right-0 top-0 w-24 h-24 bg-slate-50 rounded-full -mr-8 -mt-8"></div>
          <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-2 relative z-10">Total Plataforma</p>
          <p class="text-4xl font-black text-slate-800 relative z-10">{{ usuarios.length }}</p>
        </div>
        <div class="bg-blue-50 border border-blue-100 p-6 rounded-2xl shadow-sm flex flex-col justify-center relative overflow-hidden">
          <div class="absolute right-0 top-0 w-24 h-24 bg-blue-100/50 rounded-full -mr-8 -mt-8"></div>
          <p class="text-[10px] font-black text-blue-600 uppercase tracking-widest mb-2 relative z-10">Total Pasantes</p>
          <p class="text-4xl font-black text-blue-800 relative z-10">{{ totalPasantes }}</p>
        </div>
        <div class="bg-red-50 border border-red-100 p-6 rounded-2xl shadow-sm flex flex-col justify-center relative overflow-hidden">
          <div class="absolute right-0 top-0 w-24 h-24 bg-red-100/50 rounded-full -mr-8 -mt-8"></div>
          <p class="text-[10px] font-black text-red-600 uppercase tracking-widest mb-2 relative z-10">Cuentas Inactivas</p>
          <p class="text-4xl font-black text-red-700 relative z-10">{{ totalInactivos }}</p>
        </div>
      </div>

      <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-3">
        <div class="flex flex-col xl:flex-row justify-between items-center gap-4">
          <div class="flex w-full xl:w-auto p-1.5 bg-slate-100 rounded-xl overflow-x-auto shadow-inner">
            <button @click="filtroRol = 'TODOS'" :class="filtroRol === 'TODOS' ? 'bg-white text-blue-950 shadow-sm' : 'text-slate-500 hover:text-slate-800'" class="px-5 py-2.5 rounded-lg text-xs font-black uppercase tracking-wider transition-all whitespace-nowrap">Todos</button>
            <button @click="filtroRol = 'ADMINISTRADOR'" :class="filtroRol === 'ADMINISTRADOR' ? 'bg-blue-950 text-white shadow-sm' : 'text-slate-500 hover:text-slate-800'" class="px-5 py-2.5 rounded-lg text-xs font-black uppercase tracking-wider transition-all whitespace-nowrap">Administradores</button>
            <button @click="filtroRol = 'ENCARGADO'" :class="filtroRol === 'ENCARGADO' ? 'bg-blue-600 text-white shadow-sm' : 'text-slate-500 hover:text-blue-700'" class="px-5 py-2.5 rounded-lg text-xs font-black uppercase tracking-wider transition-all whitespace-nowrap">Encargados</button>
            <button @click="filtroRol = 'PASANTE'" :class="filtroRol === 'PASANTE' ? 'bg-emerald-600 text-white shadow-sm' : 'text-slate-500 hover:text-emerald-700'" class="px-5 py-2.5 rounded-lg text-xs font-black uppercase tracking-wider transition-all whitespace-nowrap">Pasantes</button>
          </div>
          
          <div class="flex w-full xl:w-auto gap-3 items-center">
            <div class="relative w-full xl:w-80">
              <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
              </div>
              <input v-model="searchQuery" type="text" placeholder="Buscar por CI, correo o nombre..." class="block w-full pl-11 pr-4 py-3 border border-slate-200 rounded-xl bg-slate-50 text-sm font-bold focus:bg-white focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all"/>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-2xl shadow-md border border-slate-200 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-slate-200">
            <thead class="bg-slate-50">
              <tr>
                <th class="px-6 py-4 text-left text-[10px] font-black text-slate-500 uppercase tracking-widest">Identidad</th>
                <th class="px-6 py-4 text-left text-[10px] font-black text-slate-500 uppercase tracking-widest">Credenciales</th>
                <th class="px-6 py-4 text-center text-[10px] font-black text-slate-500 uppercase tracking-widest">Carrera Asignada</th>
                <th class="px-6 py-4 text-center text-[10px] font-black text-slate-500 uppercase tracking-widest">Estado</th>
                <th class="px-6 py-4 text-right text-[10px] font-black text-slate-500 uppercase tracking-widest">Opciones</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-slate-100">
              
              <tr v-if="isLoading"><td colspan="5" class="px-6 py-20 text-center font-bold text-slate-400">Recuperando directorio...</td></tr>
              <tr v-else-if="filteredUsuarios.length === 0"><td colspan="5" class="px-6 py-20 text-center font-bold text-slate-400">No se encontraron usuarios.</td></tr>
              
              <tr v-else v-for="user in filteredUsuarios" :key="user.id" class="hover:bg-blue-50/40 transition-colors group">
                <td class="px-6 py-5 whitespace-nowrap">
                  <div class="flex items-center gap-4">
                    <div class="flex-shrink-0 h-11 w-11 bg-gradient-to-br from-slate-100 to-slate-200 rounded-xl flex items-center justify-center text-blue-950 font-black text-sm border border-slate-300 shadow-sm">
                      {{ obtenerIniciales(user.nombres, user.apellidos) }}
                    </div>
                    <div class="flex flex-col">
                      <span class="text-sm font-black text-blue-950">{{ user.nombres }} {{ user.apellidos }}</span>
                      <span class="text-[11px] text-slate-500 font-bold mt-0.5">{{ user.email }}</span>
                    </div>
                  </div>
                </td>
                
                <td class="px-6 py-5 whitespace-nowrap">
                  <div class="flex flex-col items-start gap-1.5">
                    <span class="text-[11px] font-mono font-bold text-blue-700 bg-blue-50 px-2.5 py-1 rounded-md border border-blue-100">{{ user.username }}</span>
                    <span :class="rolBadgeClass(user.rol)" class="px-2 py-0.5 inline-flex text-[9px] font-black rounded uppercase tracking-widest border">
                      {{ user.rol || 'Sin rol' }}
                    </span>
                  </div>
                </td>
                
                <td class="px-6 py-5 text-center">
                  <p class="text-[11px] font-bold text-slate-600 truncate max-w-[200px] mx-auto" :title="obtenerNombreCarrera(user.carrera_id)">
                    {{ obtenerNombreCarrera(user.carrera_id) }}
                  </p>
                </td>
                
                <td class="px-6 py-5 whitespace-nowrap text-center">
                  <span :class="user.estado ? 'text-emerald-700 bg-emerald-50 border-emerald-200' : 'text-red-700 bg-red-50 border-red-200'" class="px-2.5 py-1 text-[9px] font-black tracking-widest rounded-md border uppercase shadow-sm inline-flex items-center gap-1.5">
                    <span class="w-1.5 h-1.5 rounded-full" :class="user.estado ? 'bg-emerald-500' : 'bg-red-500'"></span>
                    {{ user.estado ? 'Activo' : 'Inactivo' }}
                  </span>
                </td>
                
                <td class="px-6 py-5 whitespace-nowrap text-right">
                  <div class="flex justify-end gap-2 opacity-100 lg:opacity-30 group-hover:opacity-100 transition-opacity">
                    <button @click="verDetallesUsuario(user)" class="p-2 text-slate-500 bg-white border border-slate-200 hover:text-emerald-700 hover:border-emerald-300 hover:bg-emerald-50 rounded-xl transition-all shadow-sm" title="Ver más">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
                    </button>
                    <button @click="abrirModalEditar(user)" class="p-2 text-slate-500 bg-white border border-slate-200 hover:text-blue-700 hover:border-blue-300 hover:bg-blue-50 rounded-xl transition-all shadow-sm" title="Editar">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
                    </button>
                    <button @click="confirmarCambioEstado(user)" class="p-2 bg-white border border-slate-200 rounded-xl transition-all shadow-sm" :class="user.estado ? 'text-slate-500 hover:text-red-600 hover:bg-red-50 hover:border-red-200' : 'text-slate-500 hover:text-emerald-600 hover:bg-emerald-50 hover:border-emerald-200'" :title="user.estado ? 'Desactivar Cuenta' : 'Activar Cuenta'">
                      <svg v-if="user.estado" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"/></svg>
                      <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>

    <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center bg-blue-950/80 px-4 py-8 backdrop-blur-sm overflow-y-auto">
      <div class="relative bg-white rounded-3xl shadow-2xl w-full max-w-2xl overflow-hidden flex flex-col max-h-[calc(100vh-4rem)] border border-blue-100">
        
        <div class="px-8 py-5 bg-gradient-to-r from-blue-950 to-blue-900 flex justify-between items-center border-b-4 border-red-600">
          <h3 class="text-lg font-black text-white tracking-widest uppercase flex items-center gap-2">
            <svg class="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
            {{ isEditing ? 'Ficha de Usuario' : 'Nuevo Registro' }}
          </h3>
          <button @click="cerrarModal" class="text-blue-300 hover:text-white transition-colors bg-white/10 p-1.5 rounded-lg"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12"/></svg></button>
        </div>

        <div class="p-8 overflow-y-auto">
          <div v-if="!isEditing && usernamePreview" class="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-xl text-sm text-blue-900 flex items-center justify-between shadow-inner">
            <div class="flex items-center gap-2">
               <svg class="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
               <span class="font-bold">Username automático:</span>
            </div>
            <strong class="font-mono bg-white px-3 py-1 rounded-lg border border-blue-200 text-red-700 tracking-wider shadow-sm">{{ usernamePreview }}</strong>
          </div>

          <form @submit.prevent="guardarUsuario" class="space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
              <div>
                <label class="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1.5 ml-1">Nombres <span class="text-red-500">*</span></label>
                <input v-model="formulario.nombres" type="text" required placeholder="Ej. Juan Carlos" class="w-full border border-slate-300 rounded-xl p-3.5 outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-200 text-sm font-bold text-blue-950 bg-slate-50 focus:bg-white transition-all"/>
              </div>
              <div>
                <label class="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1.5 ml-1">Apellidos <span class="text-red-500">*</span></label>
                <input v-model="formulario.apellidos" type="text" required placeholder="Ej. Pérez Gómez" class="w-full border border-slate-300 rounded-xl p-3.5 outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-200 text-sm font-bold text-blue-950 bg-slate-50 focus:bg-white transition-all"/>
              </div>
              <div>
                <label class="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1.5 ml-1">C.I. <span class="text-red-500">*</span></label>
                <input v-model="formulario.carnet_identidad" type="text" required placeholder="Nro. Documento" class="w-full border border-slate-300 rounded-xl p-3.5 outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-200 text-sm font-bold text-blue-950 bg-slate-50 focus:bg-white transition-all"/>
              </div>
              <div>
                <label class="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1.5 ml-1">Email Institucional <span class="text-red-500">*</span></label>
                <input v-model="formulario.email" type="email" required placeholder="correo@umsa.bo" class="w-full border border-slate-300 rounded-xl p-3.5 outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-200 text-sm font-bold text-blue-950 bg-slate-50 focus:bg-white transition-all"/>
              </div>
              
              <div class="col-span-1 md:col-span-2 h-px bg-slate-200 my-2"></div>

              <div>
                <label class="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1.5 ml-1">Rol del Sistema <span class="text-red-500">*</span></label>
                <select v-if="!isEditing" v-model="formulario.rol_id" required class="w-full border border-slate-300 rounded-xl p-3.5 outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-200 text-sm font-bold text-blue-950 bg-slate-50 focus:bg-white transition-all">
                  <option :value="1">Administrador</option>
                  <option :value="2">Encargado</option>
                  <option :value="3">Pasante</option>
                </select>
                <input v-else type="text" :value="formulario.rol_nombre" disabled class="w-full border border-slate-200 rounded-xl p-3.5 bg-slate-100 text-slate-500 text-sm font-bold cursor-not-allowed"/>
              </div>
              <div>
                <label class="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1.5 ml-1">Carrera Asignada</label>
                <select v-if="requiereCarrera" v-model.number="formulario.carrera_id" required class="w-full border border-slate-300 rounded-xl p-3.5 outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-200 text-sm font-bold text-blue-950 bg-slate-50 focus:bg-white transition-all">
                  <option :value="null" disabled>Seleccionar carrera...</option>
                  <option v-for="c in carreras" :key="c.id" :value="c.id">{{ c.nombre }}</option>
                </select>
                <input v-else type="text" value="N/A (Acceso Global)" disabled class="w-full border border-slate-200 rounded-xl p-3.5 bg-slate-100 text-slate-500 text-sm font-bold cursor-not-allowed"/>
              </div>

              <div v-if="formulario.rol_id === 3">
                <label class="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1.5 ml-1">Programa de Pasantía <span class="text-red-500">*</span></label>
                <select v-model.number="formulario.programa_id" required class="w-full border border-slate-300 rounded-xl p-3.5 outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-200 text-sm font-bold text-blue-950 bg-slate-50 focus:bg-white transition-all">
                  <option :value="null" disabled>Seleccionar programa...</option>
                  <option v-for="p in programas" :key="p.id" :value="p.id">{{ p.nombre }} {{ p.gestion ? `(${p.gestion})` : '' }}</option>
                </select>
              </div>
              <div>
                <label class="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1.5 ml-1">Celular <span class="text-red-500">*</span></label>
                <input v-model="formulario.celular" type="tel" required placeholder="70123456" class="w-full border border-slate-300 rounded-xl p-3.5 outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-200 text-sm font-bold text-blue-950 bg-slate-50 focus:bg-white transition-all"/>
              </div>

              <div v-if="formulario.rol_id === 3">
                <label class="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1.5 ml-1">Registro Univ. (RU)</label>
                <input v-model="formulario.ru" type="text" placeholder="Ej. 1754321" class="w-full border border-slate-300 rounded-xl p-3.5 outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-200 text-sm font-bold text-blue-950 bg-slate-50 focus:bg-white transition-all"/>
              </div>
              <div v-if="formulario.rol_id === 3">
                <label class="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1.5 ml-1">Unidad Asignada</label>
                <input v-model="formulario.unidad_asignada" type="text" placeholder="Ej. Biblioteca Central" class="w-full border border-slate-300 rounded-xl p-3.5 outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-200 text-sm font-bold text-blue-950 bg-slate-50 focus:bg-white transition-all"/>
              </div>
              
              <div class="col-span-1 md:col-span-2">
                <label class="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1.5 ml-1 flex justify-between">
                  Contraseña de Acceso
                  <span v-if="isEditing" class="text-[9px] bg-red-100 text-red-600 px-1.5 rounded uppercase tracking-wider">Vacío = Mantener actual</span>
                </label>
                <input v-model="formulario.password" type="password" :required="!isEditing" placeholder="Mín. 6 caracteres" class="w-full border border-slate-300 rounded-xl p-3.5 outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-200 text-sm font-bold text-blue-950 bg-slate-50 focus:bg-white transition-all"/>
              </div>
            </div>

            <div v-if="mensajeError" class="text-red-700 bg-red-50 p-4 text-sm rounded-xl border border-red-200 font-bold flex items-center gap-2">
              <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
              {{ mensajeError }}
            </div>

            <div class="flex justify-end gap-3 pt-6 border-t border-slate-100">
              <button type="button" @click="cerrarModal" class="px-6 py-3 border border-slate-300 rounded-xl text-slate-600 text-sm font-bold hover:bg-slate-50 transition-colors">Cancelar</button>
              <button type="submit" :disabled="isSubmitting" class="px-8 py-3 bg-gradient-to-r from-blue-800 to-blue-950 text-white rounded-xl text-sm font-black uppercase tracking-widest hover:from-blue-700 hover:to-blue-900 disabled:opacity-50 shadow-lg shadow-blue-900/30 transition-all flex items-center gap-2">
                <span v-if="isSubmitting" class="w-4 h-4 border-2 border-white/40 border-t-white rounded-full animate-spin"></span>
                {{ isSubmitting ? 'Procesando...' : (isEditing ? 'Guardar Cambios' : 'Registrar') }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modal para ver detalles del usuario -->
    <div v-if="showModalDetalles" class="fixed inset-0 z-50 flex items-center justify-center bg-blue-950/80 px-4 py-8 backdrop-blur-sm overflow-y-auto">
      <div class="relative bg-white rounded-3xl shadow-2xl w-full max-w-3xl overflow-hidden flex flex-col max-h-[calc(100vh-4rem)] border border-blue-100">
        
        <div class="px-8 py-5 bg-gradient-to-r from-blue-950 to-blue-900 flex justify-between items-center border-b-4 border-red-600">
          <h3 class="text-lg font-black text-white tracking-widest uppercase flex items-center gap-2">
            <svg class="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
            Detalles del Usuario
          </h3>
          <button @click="cerrarModalDetalles" class="text-blue-300 hover:text-white transition-colors bg-white/10 p-1.5 rounded-lg"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12"/></svg></button>
        </div>

        <div class="p-8 overflow-y-auto">
          <div v-if="usuarioSeleccionado" class="space-y-6">
            <!-- Información principal -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="bg-gradient-to-br from-slate-50 to-slate-100 p-6 rounded-2xl border border-slate-200">
                <h4 class="text-sm font-black text-slate-600 uppercase tracking-widest mb-4 flex items-center gap-2">
                  <svg class="w-4 h-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
                  Información Personal
                </h4>
                <div class="space-y-3">
                  <div class="flex justify-between items-center">
                    <span class="text-xs font-bold text-slate-500">Nombre Completo:</span>
                    <span class="text-sm font-black text-slate-800">{{ usuarioSeleccionado.nombres }} {{ usuarioSeleccionado.apellidos }}</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-xs font-bold text-slate-500">C.I.:</span>
                    <span class="text-sm font-mono font-bold text-blue-700 bg-blue-50 px-2 py-1 rounded">{{ usuarioSeleccionado.carnet_identidad }}</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-xs font-bold text-slate-500">Email:</span>
                    <span class="text-sm font-bold text-slate-700">{{ usuarioSeleccionado.email }}</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-xs font-bold text-slate-500">Celular:</span>
                    <span class="text-sm font-bold text-slate-700">{{ usuarioSeleccionado.celular || 'No registrado' }}</span>
                  </div>
                </div>
              </div>

              <div class="bg-gradient-to-br from-blue-50 to-blue-100 p-6 rounded-2xl border border-blue-200">
                <h4 class="text-sm font-black text-blue-600 uppercase tracking-widest mb-4 flex items-center gap-2">
                  <svg class="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V8a2 2 0 00-2-2h-5m-4 0V5a2 2 0 114 0v1m-4 0a2 2 0 104 0m-5 8a2 2 0 100-4 2 2 0 000 4zm0 0c1.306 0 2.417.835 2.83 2M9 14a3 3 0 00-2.83 2"/></svg>
                  Credenciales
                </h4>
                <div class="space-y-3">
                  <div class="flex justify-between items-center">
                    <span class="text-xs font-bold text-blue-500">Username:</span>
                    <span class="text-sm font-mono font-black text-blue-700 bg-white px-2 py-1 rounded border border-blue-200">{{ usuarioSeleccionado.username }}</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-xs font-bold text-blue-500">Rol:</span>
                    <span :class="rolBadgeClass(usuarioSeleccionado.rol)" class="px-3 py-1 text-[10px] font-black rounded uppercase tracking-widest border">
                      {{ usuarioSeleccionado.rol || 'Sin rol' }}
                    </span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-xs font-bold text-blue-500">Estado:</span>
                    <span :class="usuarioSeleccionado.estado ? 'text-emerald-700 bg-emerald-50 border-emerald-200' : 'text-red-700 bg-red-50 border-red-200'" class="px-2.5 py-1 text-[9px] font-black tracking-widest rounded-md border uppercase shadow-sm inline-flex items-center gap-1.5">
                      <span class="w-1.5 h-1.5 rounded-full" :class="usuarioSeleccionado.estado ? 'bg-emerald-500' : 'bg-red-500'"></span>
                      {{ usuarioSeleccionado.estado ? 'Activo' : 'Inactivo' }}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Información académica/laboral -->
            <div class="bg-gradient-to-br from-emerald-50 to-emerald-100 p-6 rounded-2xl border border-emerald-200">
              <h4 class="text-sm font-black text-emerald-600 uppercase tracking-widest mb-4 flex items-center gap-2">
                <svg class="w-4 h-4 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>
                Información Académica/Laboral
              </h4>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div class="bg-white p-4 rounded-xl border border-emerald-200">
                  <span class="text-xs font-bold text-emerald-500 block mb-1">Carrera:</span>
                  <span class="text-sm font-black text-slate-800">{{ obtenerNombreCarrera(usuarioSeleccionado.carrera_id) }}</span>
                </div>
                <div class="bg-white p-4 rounded-xl border border-emerald-200">
                  <span class="text-xs font-bold text-emerald-500 block mb-1">RU:</span>
                  <span class="text-sm font-mono font-bold text-slate-800">{{ usuarioSeleccionado.ru || 'No aplica' }}</span>
                </div>
                <div class="bg-white p-4 rounded-xl border border-emerald-200">
                  <span class="text-xs font-bold text-emerald-500 block mb-1">Unidad Asignada:</span>
                  <span class="text-sm font-black text-slate-800">{{ usuarioSeleccionado.unidad_asignada || 'No asignada' }}</span>
                </div>
              </div>
            </div>

            <!-- Información adicional para pasantes -->
            <div v-if="usuarioSeleccionado.rol === 'PASANTE'" class="bg-gradient-to-br from-purple-50 to-purple-100 p-6 rounded-2xl border border-purple-200">
              <h4 class="text-sm font-black text-purple-600 uppercase tracking-widest mb-4 flex items-center gap-2">
                <svg class="w-4 h-4 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
                Información de Pasantía
              </h4>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="bg-white p-4 rounded-xl border border-purple-200">
                  <span class="text-xs font-bold text-purple-500 block mb-1">Programa:</span>
                  <span class="text-sm font-black text-slate-800">{{ obtenerNombrePrograma(usuarioSeleccionado.programa_id) }}</span>
                </div>
                <div class="bg-white p-4 rounded-xl border border-purple-200">
                  <span class="text-xs font-bold text-purple-500 block mb-1">Meta de Horas:</span>
                  <span class="text-sm font-black text-slate-800">{{ usuarioSeleccionado.meta_horas_pasantia || 240 }} horas</span>
                </div>
              </div>
            </div>
          </div>

          <div class="flex justify-end gap-3 pt-6 border-t border-slate-100">
            <button @click="abrirModalEditar(usuarioSeleccionado)" class="px-6 py-3 bg-blue-600 text-white rounded-xl text-sm font-bold hover:bg-blue-700 transition-colors flex items-center gap-2">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
              Editar Usuario
            </button>
            <button @click="cerrarModalDetalles" class="px-6 py-3 border border-slate-300 rounded-xl text-slate-600 text-sm font-bold hover:bg-slate-50 transition-colors">Cerrar</button>
          </div>
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

const usuarios     = ref([])
const searchQuery  = ref('')
const filtroRol    = ref('TODOS')
const isLoading    = ref(true)
const showModal    = ref(false)
const showModalDetalles = ref(false)
const isEditing    = ref(false)
const idEditando   = ref(null)
const isSubmitting = ref(false)
const mensajeError = ref('')
const usuarioSeleccionado = ref(null)

const carreras  = ref([])
const programas = ref([])

const requiereCarrera = computed(() => {
  const rolId = Number(formulario.value.rol_id)
  return rolId === 3 || rolId === 2 // Pasante o Encargado
})

const formulario = ref({
  nombres: '', apellidos: '', carnet_identidad: '', ru: '', unidad_asignada: '',
  programa_id: null, meta_horas_pasantia: 240, email: '', celular: '', password: '', 
  rol_id: 3, carrera_id: null, rol_nombre: ''
})

const totalPasantes  = computed(() => usuarios.value.filter(u => u.rol === 'PASANTE').length)
const totalInactivos = computed(() => usuarios.value.filter(u => !u.estado).length)

const obtenerIniciales = (nombres, apellidos) => {
  const n = nombres ? nombres.trim().charAt(0) : ''
  const a = apellidos ? apellidos.trim().charAt(0) : ''
  if (!a && nombres) return nombres.substring(0, 2).toUpperCase()
  return (n + a).toUpperCase() || 'U'
}

const obtenerNombreCarrera = (carreraId) => {
  if (!carreraId) return 'No aplica'
  const carrera = carreras.value.find(c => c.id === carreraId)
  return carrera ? carrera.nombre : `ID: ${carreraId}`
}

const usernamePreview = computed(() => {
  const n  = formulario.value.nombres?.trim()
  const a  = formulario.value.apellidos?.trim()
  const ci = formulario.value.carnet_identidad?.trim()
  if (!n || !a || !ci) return ''
  return `${n[0].toLowerCase()}${a[0].toLowerCase()}${ci}`
})

const filteredUsuarios = computed(() => {
  let resultado = usuarios.value
  if (filtroRol.value !== 'TODOS') resultado = resultado.filter(u => u.rol === filtroRol.value)
  if (searchQuery.value) {
    const lower = searchQuery.value.toLowerCase()
    resultado = resultado.filter(u =>
      (u.nombres + ' ' + u.apellidos).toLowerCase().includes(lower) ||
      u.username.toLowerCase().includes(lower) ||
      u.email.toLowerCase().includes(lower)
    )
  }
  return resultado
})

const rolBadgeClass = (rol) => {
  if (rol === 'ADMINISTRADOR') return 'bg-blue-950 text-white border-blue-900'
  if (rol === 'ENCARGADO')     return 'bg-blue-100 text-blue-800 border-blue-200'
  if (rol === 'PASANTE')       return 'bg-emerald-100 text-emerald-800 border-emerald-200'
  return 'bg-slate-100 text-slate-700 border-slate-200'
}

onMounted(async () => {
  await Promise.all([cargarUsuarios(), cargarCarreras(), cargarProgramas()])
})

const cargarUsuarios = async () => {
  isLoading.value = true
  try { const res = await api.get('/usuarios/listar'); usuarios.value = res.data }
  finally { isLoading.value = false }
}

const cargarCarreras = async () => {
  try { const res = await api.get('/carreras/'); carreras.value = res.data || [] } catch (e) {}
}

const cargarProgramas = async () => {
  try { const res = await api.get('/programas/listar'); programas.value = res.data || [] } catch (e) {}
}

const abrirModalCrear = () => {
  isEditing.value  = false; idEditando.value = null
  formulario.value = { 
    nombres: '', apellidos: '', carnet_identidad: '', 
    ru: '', unidad_asignada: '', programa_id: null, 
    meta_horas_pasantia: 240, email: '', celular: '', 
    password: '', rol_id: 3, carrera_id: null 
  }
  mensajeError.value = ''; showModal.value = true
}

const abrirModalEditar = (usuario) => {
  isEditing.value  = true; idEditando.value = usuario.id
  let rId = 3; if(usuario.rol === 'ADMINISTRADOR') rId=1; if(usuario.rol === 'ENCARGADO') rId=2;
  
  formulario.value = { 
    nombres: usuario.nombres, 
    apellidos: usuario.apellidos, 
    carnet_identidad: usuario.carnet_identidad, 
    ru: usuario.ru || '', 
    unidad_asignada: usuario.unidad_asignada || '', 
    programa_id: usuario.programa_id ?? null, 
    meta_horas_pasantia: Number(usuario.meta_horas_pasantia ?? 240), 
    email: usuario.email, 
    celular: usuario.celular || '', 
    password: '', 
    rol_id: rId, 
    carrera_id: usuario.carrera_id, 
    rol_nombre: usuario.rol 
  }
  mensajeError.value = ''; showModal.value = true
}

const cerrarModal = () => { showModal.value = false }

const guardarUsuario = async () => {
  isSubmitting.value = true; mensajeError.value = ''
  try {
    if (requiereCarrera.value && !formulario.value.carrera_id) { mensajeError.value = 'Selecciona una carrera.'; return }
    
    // Validar programa si es pasante
    if (formulario.value.rol_id === 3 && !formulario.value.programa_id) { 
      mensajeError.value = 'Selecciona un programa para el pasante.'; return 
    }
    
    if (isEditing.value) {
      const payload = { 
        nombres: formulario.value.nombres, 
        apellidos: formulario.value.apellidos, 
        carnet_identidad: formulario.value.carnet_identidad, 
        email: formulario.value.email, 
        celular: formulario.value.celular, 
        carrera_id: formulario.value.carrera_id || null,
        ru: formulario.value.ru,
        unidad_asignada: formulario.value.unidad_asignada,
        programa_id: formulario.value.programa_id || null
      }
      if (formulario.value.password) payload.password = formulario.value.password
      await api.put(`/usuarios/editar/${idEditando.value}`, payload)
    } else {
      const datos = { ...formulario.value }; 
      delete datos.rol_nombre; 
      if (!datos.carrera_id) datos.carrera_id = null;
      if (!datos.programa_id) datos.programa_id = null;
      await api.post('/usuarios/registro', datos)
    }
    cerrarModal(); await cargarUsuarios()
  } catch (error) { mensajeError.value = error.response?.data?.detail || 'Error al procesar la solicitud.' }
  finally { isSubmitting.value = false }
}

const obtenerNombrePrograma = (programaId) => {
  if (!programaId) return 'No aplica'
  const programa = programas.value.find(p => p.id === programaId)
  return programa ? programa.nombre : `ID: ${programaId}`
}

const formatearFecha = (fecha) => {
  if (!fecha) return 'No registrada'
  const d = new Date(fecha)
  return d.toLocaleDateString('es-BO', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const verDetallesUsuario = (usuario) => {
  usuarioSeleccionado.value = usuario
  showModalDetalles.value = true
}

const cerrarModalDetalles = () => {
  showModalDetalles.value = false
  usuarioSeleccionado.value = null
}

const confirmarCambioEstado = async (usuario) => {
  if (confirm(`¿Deseas ${usuario.estado ? 'desactivar' : 'habilitar'} a ${usuario.username}?`)) {
    try { await api.put(`/usuarios/editar/${usuario.id}`, { estado: !usuario.estado }); await cargarUsuarios() } catch (error) {}
  }
}

const cerrarSesion = () => { authStore.logout(); router.push('/login') }
</script>