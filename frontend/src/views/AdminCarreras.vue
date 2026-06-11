<template>
  <div class="min-h-screen bg-slate-50 font-sans pb-12">

    <header class="bg-[#0b1a33] border-b border-[#0b1a33] sticky top-0 z-50">
      <div class="max-w-[96rem] mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16 items-center">
          
          <div class="flex items-center gap-4">
            <div class="h-8 px-2 bg-white rounded flex items-center justify-center font-black text-xs tracking-widest shadow-sm">
              <span class="text-[#cc0000]">U</span><span class="text-[#0b1a33]">MSA</span>
            </div>
            <div class="border-l border-slate-600 pl-4 py-1 hidden sm:block">
              <p class="text-[10px] text-[#cc0000] font-bold uppercase tracking-widest leading-none mb-1">Facultad de Cs. Sociales</p>
              <p class="text-sm font-extrabold text-white leading-none">Centro de Mando <span class="text-slate-400 font-medium ml-1">| Admin</span></p>
            </div>
          </div>

          <nav class="hidden lg:flex items-center gap-2">
            <button @click="router.push('/admin')" class="text-slate-300 hover:bg-[#152a4f] hover:text-white px-4 py-2 rounded-md text-sm font-semibold transition-all">Monitor</button>
            <button @click="router.push('/usuarios')" class="text-slate-300 hover:bg-[#152a4f] hover:text-white px-4 py-2 rounded-md text-sm font-semibold transition-all">Usuarios</button>
            <button @click="router.push('/programas')" class="text-slate-300 hover:bg-[#152a4f] hover:text-white px-4 py-2 rounded-md text-sm font-semibold transition-all">Programas</button>
            <button class="bg-[#15469e] text-white px-5 py-2 rounded-md text-sm font-bold shadow-md flex items-center gap-2">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>
              Unidades
            </button>
          </nav>

          <div class="flex items-center gap-4">
            <div class="hidden sm:flex flex-col items-end">
              <span class="text-white text-sm font-bold leading-tight">Admin</span>
              <span class="text-[10px] font-bold text-[#cc0000] uppercase tracking-widest">Máxima Autoridad</span>
            </div>
            <button @click="router.push('/perfil')" class="w-9 h-9 bg-[#cc0000] rounded-md flex items-center justify-center text-white font-bold text-sm shadow-md hover:bg-red-700 transition-colors">
              {{ obtenerIniciales(authStore.user?.nombres, authStore.user?.apellidos) }}
            </button>
            <div class="h-5 w-px bg-slate-600 hidden sm:block"></div>
            <button @click="cerrarSesion" class="text-slate-400 hover:text-white transition-colors" title="Cerrar Sesión">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/></svg>
            </button>
          </div>
        </div>
      </div>
    </header>

    <main class="max-w-5xl mx-auto py-8 px-4 sm:px-6 space-y-8">

      <div>
        <div class="flex items-center gap-2 mb-2">
          <svg class="w-5 h-5 text-[#15469e]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>
          <span class="text-[10px] font-bold text-[#15469e] uppercase tracking-widest">Catálogo Institucional</span>
        </div>
        <h1 class="text-3xl font-black text-[#0b1a33] tracking-tight">Unidades Académicas</h1>
        <p class="text-slate-500 text-sm mt-1">Registra y administra las unidades y sus logos institucionales.</p>
      </div>

      <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <div class="bg-[#182b52] border-b-4 border-[#cc0000] px-6 py-4 flex items-center gap-2">
          <svg class="w-4 h-4 text-[#cc0000]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M12 4v16m8-8H4"/></svg>
          <h2 class="text-sm font-bold text-white uppercase tracking-wider">Registrar Unidad</h2>
        </div>
        
        <div class="p-6">
          <div class="flex flex-col sm:flex-row gap-5 items-start sm:items-end">
            <div class="flex-1 w-full">
              <label class="block text-[10px] font-bold text-[#4a5f87] uppercase tracking-widest mb-1.5 ml-1">Nombre Oficial <span class="text-[#cc0000]">*</span></label>
              <input v-model="nueva.nombre" type="text" placeholder="Ej. Trabajo Social" class="w-full bg-slate-50 border border-slate-200 rounded-lg p-3 outline-none focus:border-[#15469e] focus:bg-white focus:ring-1 focus:ring-[#15469e] transition-all text-sm font-medium text-[#0b1a33]" />
            </div>
            <div class="flex-1 w-full">
              <label class="block text-[10px] font-bold text-[#4a5f87] uppercase tracking-widest mb-1.5 ml-1">Descripción</label>
              <input v-model="nueva.descripcion" type="text" placeholder="Detalles de la unidad..." class="w-full bg-slate-50 border border-slate-200 rounded-lg p-3 outline-none focus:border-[#15469e] focus:bg-white focus:ring-1 focus:ring-[#15469e] transition-all text-sm font-medium text-[#0b1a33]" />
            </div>
            <button @click="crear" :disabled="creando" class="w-full sm:w-auto px-8 py-3 bg-[#cc0000] text-white rounded-lg text-sm font-bold hover:bg-[#a30000] transition-colors disabled:opacity-50">
              {{ creando ? 'Procesando...' : 'CREAR UNIDAD' }}
            </button>
          </div>
          <div v-if="error" class="mt-4 text-[#cc0000] text-sm font-bold flex items-center gap-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            {{ error }}
          </div>
        </div>
      </div>

      <div v-if="isLoading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-slate-200 border-t-[#15469e] mb-4"></div>
        <p class="text-[#4a5f87] font-medium">Cargando unidades...</p>
      </div>
      <div v-else-if="carreras.length === 0" class="text-center py-16 bg-white rounded-xl border border-slate-200">
        <p class="text-slate-400 font-medium">No hay unidades registradas.</p>
      </div>
      
      <div v-else class="grid grid-cols-1 gap-5">
        <div v-for="c in carreras" :key="c.id" class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden flex flex-col md:flex-row relative">
          
          <button @click="eliminar(c)" class="absolute top-5 right-5 text-slate-300 hover:text-[#cc0000] transition-colors z-10 p-1 bg-white rounded-md border border-transparent hover:border-red-100 hover:bg-red-50" title="Eliminar Unidad">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
          </button>

          <div class="md:w-48 bg-slate-50 border-r border-slate-100 flex flex-col items-center justify-center p-6 shrink-0">
            <div class="w-24 h-24 bg-white border border-slate-200 rounded-lg flex items-center justify-center overflow-hidden mb-4 shadow-sm">
              <img v-if="c.logo_url" :src="resolveStaticUrl(c.logo_url)" class="w-full h-full object-contain p-2" />
              <div v-else class="flex flex-col items-center justify-center text-slate-300">
                <span class="text-[10px] font-bold">SIN LOGO</span>
              </div>
            </div>
            
            <label class="px-4 py-1.5 bg-white border border-slate-200 hover:border-[#15469e] text-[#15469e] rounded text-xs font-bold cursor-pointer transition-colors flex items-center gap-2">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"/></svg>
              Seleccionar Logo
              <input type="file" accept="image/*" @change="(e) => onFileChange(c, e)" class="hidden" />
            </label>
          </div>

          <div class="p-6 pr-14 flex-1 flex flex-col justify-between">
            
            <div class="flex items-center gap-3 mb-4">
              <span class="text-[10px] font-mono text-slate-400 bg-slate-100 px-2 py-1 rounded border border-slate-200">#{{ c.id }}</span>
              <span v-if="c._edit.estado" class="text-[10px] font-bold text-emerald-700 bg-emerald-100 px-2.5 py-1 rounded tracking-widest">ACTIVO</span>
              <span v-else class="text-[10px] font-bold text-slate-500 bg-slate-200 px-2.5 py-1 rounded tracking-widest">INACTIVO</span>
            </div>

            <div class="space-y-4">
              <div>
                <label class="block text-[10px] font-bold text-[#4a5f87] uppercase tracking-widest mb-1">Nombre Oficial</label>
                <input v-model="c._edit.nombre" class="font-black text-xl text-[#0b1a33] bg-transparent border-b-2 border-transparent hover:border-slate-300 focus:border-[#15469e] outline-none w-full transition-colors pb-1" />
              </div>
              
              <div>
                <label class="block text-[10px] font-bold text-[#4a5f87] uppercase tracking-widest mb-1">Descripción de la Unidad</label>
                <input v-model="c._edit.descripcion" placeholder="Añadir una descripción a esta unidad..." class="text-sm text-slate-600 bg-transparent border-b border-transparent hover:border-slate-300 focus:border-[#15469e] outline-none w-full transition-colors pb-1" />
              </div>
            </div>

            <div class="flex items-center justify-between gap-4 mt-8 pt-4 border-t border-slate-100">
              <label class="flex items-center gap-2 text-xs font-bold text-slate-600 cursor-pointer hover:text-[#0b1a33]">
                <input type="checkbox" v-model="c._edit.estado" class="w-4 h-4 rounded text-[#15469e] focus:ring-[#15469e] border-slate-300" />
                Unidad habilitada para pasantías
              </label>

              <button @click="guardar(c)" class="px-5 py-2 bg-white border border-slate-200 hover:border-[#0b1a33] text-[#0b1a33] text-xs font-bold rounded-lg transition-all shadow-sm">
                GUARDAR CAMBIOS
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
// Lógica de Vue y API inalterada
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api, { API_ORIGIN } from '../services/api'

const router = useRouter()
const authStore = useAuthStore()

const carreras = ref([]); const nueva = ref({ nombre: '', descripcion: '' })
const creando = ref(false); const isLoading = ref(true); const error = ref('')

const obtenerIniciales = (nombres, apellidos) => {
  const n = nombres ? nombres.trim().charAt(0) : ''; const a = apellidos ? apellidos.trim().charAt(0) : ''
  if (!a && nombres) return nombres.substring(0, 2).toUpperCase()
  return (n + a).toUpperCase() || 'A'
}

const resolveStaticUrl = (url) => {
  if (!url) return null; const s = String(url);
  if (s.startsWith('http://') || s.startsWith('https://')) return s;
  if (s.startsWith('/')) return `${API_ORIGIN}${s}`; return s
}

const cerrarSesion = () => { authStore.logout(); router.push('/login') }

const cargar = async () => {
  isLoading.value = true; error.value = ''
  try {
    const res = await api.get('/carreras/')
    carreras.value = (res.data || []).map(c => ({ ...c, _edit: { nombre: c.nombre, descripcion: c.descripcion || '', logo_url: c.logo_url || '', estado: !!c.estado } }))
  } catch (e) { error.value = 'Error al cargar.'; carreras.value = [] } finally { isLoading.value = false }
}

const crear = async () => {
  if (!nueva.value.nombre?.trim()) { error.value = 'Nombre obligatorio.'; return }
  creando.value = true; error.value = ''
  try { await api.post('/carreras/', { nombre: nueva.value.nombre, descripcion: nueva.value.descripcion || null, estado: true }); nueva.value = { nombre: '', descripcion: '' }; await cargar() } catch (e) { error.value = 'Error al crear.' } finally { creando.value = false }
}

const guardar = async (c) => {
  try { await api.put(`/carreras/${c.id}`, { nombre: c._edit.nombre, descripcion: c._edit.descripcion, logo_url: c._edit.logo_url || null, estado: c._edit.estado }); await cargar() } catch (e) { alert('Error al guardar') }
}

const eliminar = async (c) => {
  if (confirm(`¿Desactivar ${c.nombre}?`)) { try { await api.delete(`/carreras/${c.id}`); await cargar() } catch (e) { alert('Error') } }
}

const onFileChange = async (c, event) => {
  const file = event?.target?.files?.[0]; if (!file) return
  try { const fd = new FormData(); fd.append('file', file); const res = await api.post(`/carreras/${c.id}/logo`, fd); c._edit.logo_url = res.data.logo_url || ''; await guardar(c) } catch (e) { alert('Error al subir logo') }
}

onMounted(cargar)
</script>