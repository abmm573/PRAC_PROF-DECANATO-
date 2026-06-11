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
            <button @click="router.push('/usuarios')" class="text-blue-200 hover:bg-blue-800/50 hover:text-white px-5 py-2 rounded-lg text-sm font-semibold transition-all">Usuarios</button>
            <button class="bg-blue-800 text-white px-5 py-2 rounded-lg text-sm font-bold shadow-md flex items-center gap-2">
              <svg class="w-4 h-4 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>
              Programas
            </button>
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
            <svg class="w-3.5 h-3.5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>
            <p class="text-[10px] font-bold text-blue-800 uppercase tracking-widest">Catálogo Institucional</p>
          </div>
          <h1 class="text-4xl font-black text-slate-800 tracking-tight">Programas de Pasantía</h1>
          <p class="text-slate-500 text-sm mt-2 max-w-xl">Crea y administra los convenios o programas institucionales para asignarlos a los pasantes.</p>
        </div>
      </div>

      <div class="grid grid-cols-1 xl:grid-cols-3 gap-8">
        
        <div class="xl:col-span-1">
          <div class="bg-white rounded-2xl shadow-lg border border-slate-200 overflow-hidden sticky top-24">
            <div class="bg-gradient-to-r from-blue-950 to-blue-900 px-6 py-5 border-b-4 border-red-600">
              <h2 class="text-white font-black uppercase tracking-widest text-sm flex items-center gap-2">
                <svg class="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4"/></svg>
                Registrar Programa
              </h2>
            </div>
            
            <div class="p-6">
              <div class="space-y-5">
                <div>
                  <label class="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1.5 ml-1">Nombre Oficial <span class="text-red-500">*</span></label>
                  <input v-model="nuevo.nombre" type="text" placeholder="Ej. Pasantía Informática 2026" class="w-full border border-slate-300 rounded-xl p-3.5 outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-200 text-sm font-bold text-blue-950 bg-slate-50 focus:bg-white transition-all" />
                </div>
                <div>
                  <label class="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1.5 ml-1">Gestión / Año <span class="text-red-500">*</span></label>
                  <input v-model="nuevo.gestion" type="text" placeholder="2026" class="w-full border border-slate-300 rounded-xl p-3.5 outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-200 text-sm font-bold text-blue-950 bg-slate-50 focus:bg-white transition-all" />
                </div>
                <div>
                  <label class="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1.5 ml-1">Descripción</label>
                  <textarea v-model="nuevo.descripcion" rows="3" placeholder="Detalles del programa..." class="w-full border border-slate-300 rounded-xl p-3.5 outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-200 text-sm font-medium text-slate-700 bg-slate-50 focus:bg-white transition-all resize-none"></textarea>
                </div>
              </div>

              <div v-if="error" class="mt-4 text-red-700 bg-red-50 p-3 text-xs rounded-lg border border-red-200 font-bold flex items-center gap-2">
                <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                {{ error }}
              </div>

              <button @click="crear" :disabled="creando" class="mt-6 w-full bg-gradient-to-r from-red-600 to-red-700 text-white rounded-xl py-3.5 text-sm font-black uppercase tracking-widest hover:from-red-500 hover:to-red-600 shadow-lg shadow-red-900/20 disabled:opacity-50 transition-all flex items-center justify-center gap-2">
                <span v-if="creando" class="w-4 h-4 border-2 border-white/40 border-t-white rounded-full animate-spin"></span>
                {{ creando ? 'Guardando...' : 'Crear Programa' }}
              </button>
            </div>
          </div>
        </div>

        <div class="xl:col-span-2">
          
          <div v-if="isLoading" class="bg-white p-12 rounded-2xl border border-slate-200 text-center shadow-sm">
            <div class="w-8 h-8 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mx-auto mb-4"></div>
            <p class="text-slate-500 font-bold text-sm tracking-wider uppercase">Cargando programas...</p>
          </div>
          
          <div v-else-if="!programas.length" class="bg-white p-16 rounded-2xl border border-dashed border-slate-300 text-center shadow-sm flex flex-col items-center justify-center">
            <svg class="w-16 h-16 text-slate-300 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>
            <p class="text-slate-500 font-bold text-lg">Catálogo vacío</p>
            <p class="text-slate-400 text-sm mt-1">Registra tu primer programa en el formulario lateral.</p>
          </div>
          
          <div v-else class="space-y-5">
            <div v-for="p in programas" :key="p.id" class="bg-white rounded-2xl shadow-sm border border-slate-200 hover:border-blue-300 hover:shadow-md transition-all overflow-hidden group">
              
              <div class="px-6 py-4 bg-slate-50 border-b border-slate-100 flex justify-between items-center group-hover:bg-blue-50/30 transition-colors">
                <div class="flex items-center gap-3">
                  <span class="text-[10px] font-black font-mono text-slate-400 bg-white border border-slate-200 px-2 py-1 rounded-md shadow-sm">#{{ p.id }}</span>
                  <span :class="p.estado ? 'bg-emerald-100 text-emerald-800 border-emerald-200' : 'bg-slate-200 text-slate-600 border-slate-300'" class="text-[9px] px-2.5 py-1 rounded-md uppercase font-black tracking-widest border shadow-sm">
                    {{ p.estado ? 'Activo' : 'Inactivo' }}
                  </span>
                </div>
                <button @click="desactivar(p)" class="text-slate-400 hover:text-red-600 bg-white p-1.5 rounded-lg border border-slate-200 hover:border-red-200 hover:bg-red-50 transition-all shadow-sm" title="Desactivar/Eliminar">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
                </button>
              </div>
              
              <div class="p-6">
                <div class="flex flex-col sm:flex-row gap-5 mb-5">
                  <div class="flex-1">
                    <label class="block text-[9px] font-bold text-slate-400 uppercase tracking-widest mb-1">Nombre Oficial</label>
                    <input v-model="p._edit.nombre" type="text" class="w-full border-b-2 border-slate-200 py-1.5 outline-none focus:border-blue-600 text-lg font-black text-blue-950 bg-transparent transition-colors" />
                  </div>
                  <div class="w-full sm:w-32">
                    <label class="block text-[9px] font-bold text-slate-400 uppercase tracking-widest mb-1 sm:text-center">Gestión</label>
                    <input v-model="p._edit.gestion" type="text" class="w-full border-b-2 border-slate-200 py-1.5 outline-none focus:border-blue-600 text-lg font-bold text-slate-600 bg-transparent sm:text-center transition-colors" />
                  </div>
                </div>
                
                <div class="mb-5">
                  <label class="block text-[9px] font-bold text-slate-400 uppercase tracking-widest mb-1.5">Descripción del Programa</label>
                  <textarea v-model="p._edit.descripcion" rows="2" class="w-full border border-slate-200 rounded-xl bg-slate-50 p-3.5 text-sm font-medium text-slate-600 resize-none outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-100 focus:bg-white transition-all"></textarea>
                </div>
                
                <div class="flex flex-col sm:flex-row items-center justify-between pt-5 border-t border-slate-100 gap-4">
                  <div class="flex flex-wrap items-center gap-3 w-full sm:w-auto">
                    
                    <a v-if="p.documento_url" :href="resolveStaticUrl(p.documento_url)" target="_blank" class="flex items-center gap-1.5 px-3 py-1.5 bg-red-50 text-red-700 hover:bg-red-100 border border-red-200 rounded-lg text-xs font-black uppercase tracking-wider transition-colors shadow-sm">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"/></svg>
                      Ver PDF
                    </a>
                    <span v-else class="text-[11px] font-bold text-slate-400 bg-slate-100 px-3 py-1.5 rounded-lg border border-slate-200">Sin archivo adjunto</span>
                    
                    <div class="relative flex items-center group/file">
                      <input type="file" accept="application/pdf,image/*" @change="(e) => onFileChange(p, e)" class="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10" />
                      <button class="flex items-center gap-1.5 px-3 py-1.5 bg-blue-50 text-blue-700 border border-blue-200 rounded-lg text-xs font-bold transition-colors group-hover/file:bg-blue-100">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"/></svg>
                        Seleccionar
                      </button>
                    </div>
                    
                    <span v-if="p._file" class="text-[10px] text-emerald-600 font-bold truncate max-w-[100px]">{{ p._file.name }}</span>
                    
                    <button v-if="p._file" @click="subirDocumento(p)" class="flex items-center gap-1 bg-slate-800 text-white px-3 py-1.5 rounded-lg text-xs font-bold hover:bg-slate-900 shadow-sm transition-colors">
                      <span v-if="subiendoId === p.id" class="w-3 h-3 border-2 border-white/40 border-t-white rounded-full animate-spin"></span>
                      Subir
                    </button>
                  </div>
                  
                  <button @click="guardar(p)" class="w-full sm:w-auto px-6 py-2.5 bg-white border-2 border-slate-200 hover:border-blue-600 hover:text-blue-700 text-slate-600 text-xs font-black uppercase tracking-widest rounded-xl transition-all shadow-sm">
                    Guardar Cambios
                  </button>
                </div>
                
              </div>
            </div>
          </div>
          
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api, { API_ORIGIN } from '../services/api'

const router = useRouter()
const authStore = useAuthStore()

const programas = ref([]); const nuevo = ref({ nombre: '', descripcion: '', gestion: '' })
const creando = ref(false); const isLoading = ref(true); const error = ref(''); const subiendoId = ref(null)

const obtenerIniciales = (nombres, apellidos) => {
  const n = nombres ? nombres.trim().charAt(0) : ''; const a = apellidos ? apellidos.trim().charAt(0) : ''
  if (!a && nombres) return nombres.substring(0, 2).toUpperCase()
  return (n + a).toUpperCase() || 'A'
}

const resolveStaticUrl = (url) => {
  if (!url) return null; const s = String(url)
  if (s.startsWith('http://') || s.startsWith('https://')) return s
  if (s.startsWith('/')) return `${API_ORIGIN}${s}`; return s
}

const cerrarSesion = () => { authStore.logout(); router.push('/login') }

const cargar = async () => {
  isLoading.value = true; error.value = ''
  try {
    const res = await api.get('/programas/listar', { params: { incluir_inactivos: true } })
    programas.value = (res.data || []).map(p => ({ ...p, _edit: { nombre: p.nombre, descripcion: p.descripcion || '', gestion: p.gestion || '', estado: !!p.estado }, _file: null }))
  } catch (e) { error.value = 'Error al cargar los programas.'; programas.value = [] } finally { isLoading.value = false }
}

const crear = async () => {
  if (!nuevo.value.nombre?.trim()) { error.value = 'El nombre oficial es obligatorio.'; return }
  if (!nuevo.value.gestion?.trim()) { error.value = 'Debes especificar una gestión.'; return }
  creando.value = true; error.value = ''
  try {
    await api.post('/programas/crear', { nombre: nuevo.value.nombre, descripcion: nuevo.value.descripcion || null, gestion: nuevo.value.gestion || null, estado: true })
    nuevo.value = { nombre: '', descripcion: '', gestion: '' }; await cargar()
  } catch (e) { error.value = 'Hubo un error al crear el programa.' } finally { creando.value = false }
}

const guardar = async (p) => {
  try { await api.put(`/programas/editar/${p.id}`, { nombre: p._edit.nombre, descripcion: p._edit.descripcion || null, gestion: p._edit.gestion || null, estado: p._edit.estado }); await cargar() } catch (e) { alert('Error al guardar los cambios.') }
}

const desactivar = async (p) => {
  if (confirm(`¿Estás seguro de desactivar o eliminar el programa "${p.nombre}"?`)) { try { await api.delete(`/programas/desactivar/${p.id}`); await cargar() } catch (e) { alert('Error al intentar desactivar el programa.') } }
}

const onFileChange = (p, event) => { p._file = event?.target?.files?.[0] || null }

const subirDocumento = async (p) => {
  if (!p._file) return; subiendoId.value = p.id
  try { const fd = new FormData(); fd.append('archivo', p._file); await api.post(`/programas/documento/${p.id}`, fd); p._file = null; await cargar() } catch (e) { alert('Error al subir el documento.') } finally { subiendoId.value = null }
}

onMounted(cargar)
</script>