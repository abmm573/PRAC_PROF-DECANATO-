<template>
  <div class="min-h-screen bg-slate-50 font-sans text-slate-800 pb-20">
    
    <div class="relative bg-slate-900 py-12 md:py-16 overflow-hidden border-b border-[#7a1b2e]/30">
      <div class="absolute inset-0 z-0">
        <img src="https://images.unsplash.com/photo-1541339907198-e08759df9a04?q=80&w=2000&auto=format&fit=crop" 
             class="w-full h-full object-cover opacity-10">
        <div class="absolute inset-0 bg-gradient-to-br from-slate-900/95 via-[#7a1b2e]/50 to-slate-900/95 backdrop-blur-sm"></div>
      </div>

      <div class="relative z-10 max-w-[1400px] mx-auto px-4 md:px-8 flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
        
        <div class="flex items-center gap-5">
          <div class="w-16 h-16 bg-white rounded-2xl flex items-center justify-center text-blue-600 text-2xl font-black shadow-[0_0_20px_rgba(37,99,235,0.4)] border border-white/20">
            {{ nombreAdmin.charAt(0).toUpperCase() }}
          </div>
          <div>
            <div class="flex items-center gap-3 mb-1">
              <h1 class="text-3xl font-black text-white tracking-tight drop-shadow-md">
                {{ nombreAdmin }}
              </h1>
              <span class="bg-blue-600/30 backdrop-blur-md text-blue-200 text-[10px] font-black px-3 py-1.5 rounded-lg uppercase tracking-widest border border-blue-400/30 shadow-sm flex items-center gap-1.5">
                <span class="w-1.5 h-1.5 rounded-full bg-blue-400 animate-pulse"></span> Administrador
              </span>
            </div>
            
            <p class="text-sm text-slate-300 font-medium flex items-center gap-4">
              Facultad de Ciencias Sociales • Control Total del Sistema
              
              <button @click="cambiarMiContrasena" class="text-xs text-blue-300 hover:text-white font-bold flex items-center gap-1 bg-white/5 hover:bg-white/20 px-2 py-1 rounded-md transition border border-white/10">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4v-3.21l5.586-5.586A6 6 0 0115 9z" /></svg>
                Cambiar clave
              </button>
            </p>
          </div>
        </div>

        <div class="flex bg-slate-800/50 p-1.5 rounded-2xl backdrop-blur-md border border-white/10 shadow-lg">
          <button 
            @click="pestana = 'usuarios'" 
            :class="pestana === 'usuarios' ? 'bg-white text-slate-900 shadow-md' : 'text-slate-300 hover:text-white hover:bg-white/10'"
            class="px-5 py-2.5 rounded-xl transition-all duration-300 text-sm font-bold flex items-center gap-2"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" /></svg>
            Usuarios
          </button>
          <button 
            @click="pestana = 'categorias'" 
            :class="pestana === 'categorias' ? 'bg-[#7a1b2e] text-white shadow-md border border-[#7a1b2e]/50' : 'text-slate-300 hover:text-white hover:bg-white/10'"
            class="px-5 py-2.5 rounded-xl transition-all duration-300 text-sm font-bold flex items-center gap-2"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" /></svg>
            Categorías
          </button>
        </div>
      </div>
    </div>

    <div class="max-w-[1400px] mx-auto px-4 md:px-8 -mt-8 relative z-20 space-y-6">

      <div v-if="pestana === 'usuarios'" class="animate-fade-in space-y-6">
        <div class="bg-white p-4 rounded-[1.5rem] shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-100 flex flex-col md:flex-row justify-between items-center gap-4">
          <div class="relative w-full md:w-96">
            <span class="absolute left-4 top-3.5 text-slate-400">🔍</span>
            <input 
              v-model="busquedaUsuario" 
              type="text" 
              placeholder="Buscar por nombre o correo..." 
              class="w-full pl-12 pr-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 outline-none transition-all font-medium text-slate-700"
            >
            <button v-if="busquedaUsuario" @click="busquedaUsuario = ''" class="absolute right-4 top-3.5 text-slate-400 hover:text-slate-600 font-bold">✕</button>
          </div>
          <button @click="abrirModalUsuario" class="w-full md:w-auto bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-bold px-6 py-3 rounded-xl hover:shadow-lg hover:shadow-blue-500/30 transition-all duration-300 flex items-center justify-center gap-2">
            <span>➕</span> Nuevo Usuario
          </button>
        </div>

        <div class="bg-white rounded-[2rem] shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-100 overflow-hidden">
          <div class="px-8 py-6 flex justify-between items-center bg-slate-50/50 border-b border-slate-100">
            <div>
              <h3 class="text-xl font-black text-slate-800 flex items-center gap-2">🛡️ Control de Accesos</h3>
              <p class="text-sm text-slate-500 mt-1">Mostrando {{ usuariosFiltrados.length }} usuarios.</p>
            </div>
            <button @click="cargarUsuarios" class="text-slate-500 bg-white hover:bg-slate-50 px-4 py-2.5 rounded-xl text-sm font-bold transition flex items-center gap-2 border border-slate-200 shadow-sm">
              <span :class="{'animate-spin': cargandoUsuarios}">🔄</span> Refrescar
            </button>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full text-left text-sm">
              <thead class="text-slate-400 uppercase tracking-wider text-[11px] font-black bg-white">
                <tr>
                  <th class="px-8 py-5">Usuario</th>
                  <th class="px-8 py-5 text-center">Rol de Acceso</th>
                  <th class="px-8 py-5 text-center">Estado</th>
                  <th class="px-8 py-5 text-right">Acciones</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                <tr v-for="usuario in usuariosFiltrados" :key="usuario.id" class="hover:bg-slate-50/50 transition">
                  <td class="px-8 py-4">
                    <div class="flex items-center gap-4">
                      <div class="w-10 h-10 rounded-full bg-blue-50 text-blue-600 font-bold flex items-center justify-center border border-blue-100 shrink-0">
                        {{ usuario.nombre.charAt(0).toUpperCase() }}
                      </div>
                      <div>
                        <p class="font-black text-slate-800 text-base mb-0.5">{{ usuario.nombre }}</p>
                        <p class="text-xs text-slate-500 font-medium">{{ usuario.correo }}</p>
                      </div>
                    </div>
                  </td>
                  <td class="px-8 py-4 text-center">
                    <span :class="{'bg-slate-100 text-slate-600': usuario.rol === 'AUTOR','bg-emerald-50 text-emerald-600': usuario.rol === 'MODERADOR','bg-blue-50 text-blue-700': usuario.rol === 'ADMINISTRADOR'}" class="px-3 py-1.5 rounded-lg text-[10px] font-black uppercase tracking-widest inline-block border border-black/5">
                      {{ usuario.rol }}
                    </span>
                  </td>
                  <td class="px-8 py-4">
                    <div class="flex items-center justify-center gap-3">
                      <span :class="usuario.activo ? 'text-emerald-500' : 'text-slate-400'" class="text-xs font-bold w-12 text-right">
                        {{ usuario.activo ? 'Activo' : 'Inactivo' }}
                      </span>
                      <button @click="cambiarEstadoUsuario(usuario)" :class="usuario.activo ? 'bg-emerald-500' : 'bg-slate-300'" class="relative inline-flex h-6 w-11 items-center rounded-full transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2">
                        <span :class="usuario.activo ? 'translate-x-6' : 'translate-x-1'" class="inline-block h-4 w-4 transform rounded-full bg-white transition shadow-sm"></span>
                      </button>
                    </div>
                  </td>
                  <td class="px-8 py-4 text-right space-x-2">
                    <button @click="abrirModalEditar(usuario)" class="text-slate-400 hover:text-blue-600 hover:bg-blue-50 p-2.5 rounded-xl transition" title="Editar">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
                    </button>
                    <button @click="confirmarEliminarUsuario(usuario.id, usuario.nombre)" class="text-slate-400 hover:text-rose-600 hover:bg-rose-50 p-2.5 rounded-xl transition" title="Eliminar Permanentemente">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div v-else-if="pestana === 'categorias'" class="animate-fade-in space-y-6">
        <div class="bg-white p-4 rounded-[1.5rem] shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-100 flex flex-col md:flex-row justify-between items-center gap-4">
          <div class="relative w-full md:w-96">
            <span class="absolute left-4 top-3.5 text-slate-400">🔍</span>
            <input 
              v-model="busquedaCategoria" 
              type="text" 
              placeholder="Buscar categoría..." 
              class="w-full pl-12 pr-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:border-[#7a1b2e] focus:ring-4 focus:ring-[#7a1b2e]/10 outline-none transition-all font-medium text-slate-700"
            >
          </div>
          <button @click="abrirModalCategoria" class="w-full md:w-auto bg-[#7a1b2e] text-white font-bold px-6 py-3 rounded-xl hover:shadow-lg hover:shadow-[#7a1b2e]/30 transition-all duration-300 flex items-center justify-center gap-2">
            <span>➕</span> Nueva Categoría
          </button>
        </div>

        <div class="bg-white rounded-[2rem] shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-100 overflow-hidden">
          <div class="px-8 py-6 flex justify-between items-center bg-slate-50/50 border-b border-slate-100">
            <div>
              <h3 class="text-xl font-black text-slate-800 flex items-center gap-2">🏷️ Gestión de Clasificaciones</h3>
              <p class="text-sm text-slate-500 mt-1">Líneas de investigación y temáticas de las revistas.</p>
            </div>
            <button @click="cargarCategorias" class="text-slate-500 bg-white hover:bg-slate-50 px-4 py-2.5 rounded-xl text-sm font-bold transition flex items-center gap-2 border border-slate-200 shadow-sm">
              <span :class="{'animate-spin': cargandoCategorias}">🔄</span> Refrescar
            </button>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full text-left text-sm">
              <thead class="text-slate-400 uppercase tracking-wider text-[11px] font-black bg-white">
                <tr>
                  <th class="px-8 py-5">Nombre de Categoría</th>
                  <th class="px-8 py-5">Descripción</th>
                  <th class="px-8 py-5 text-right">Acciones</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                <tr v-for="cat in categoriasFiltradas" :key="cat.id" class="hover:bg-slate-50/50 transition">
                  <td class="px-8 py-5 font-black text-slate-800">{{ cat.nombre }}</td>
                  <td class="px-8 py-5 text-slate-500 font-medium">{{ cat.descripcion || 'Sin descripción' }}</td>
                  <td class="px-8 py-5 text-right space-x-2">
                    <button @click="editarModalCategoria(cat)" class="text-slate-400 hover:text-amber-500 hover:bg-amber-50 p-2.5 rounded-xl transition">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
                    </button>
                    <button @click="confirmarEliminarCategoria(cat.id, cat.nombre)" class="text-slate-400 hover:text-rose-600 hover:bg-rose-50 p-2.5 rounded-xl transition">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <div v-if="mostrarModalUsuario" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4 animate-fade-in">
      <div class="bg-white rounded-[2rem] shadow-2xl w-full max-w-lg overflow-hidden transform transition-all border border-slate-100">
        <div class="p-8">
          <div class="flex justify-between items-center mb-6 border-b border-slate-100 pb-4">
            <h2 class="text-2xl font-black text-slate-800">{{ modoEdicionUsuario ? 'Editar Usuario' : 'Nuevo Usuario' }}</h2>
            <button @click="mostrarModalUsuario = false" class="text-slate-400 hover:text-rose-500 text-3xl font-bold transition leading-none">&times;</button>
          </div>
          <form @submit.prevent="guardarUsuario" class="space-y-5">
            <div>
              <label class="block text-[11px] font-black text-slate-400 uppercase tracking-widest mb-1.5 ml-1">Nombre Completo</label>
              <input v-model="formUsuario.nombre" type="text" required class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 outline-none transition font-medium text-slate-700">
            </div>
            <div>
              <label class="block text-[11px] font-black text-slate-400 uppercase tracking-widest mb-1.5 ml-1">Correo Electrónico</label>
              <input v-model="formUsuario.correo" type="email" required :disabled="modoEdicionUsuario" :class="{'opacity-60 cursor-not-allowed': modoEdicionUsuario}" class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl outline-none transition font-medium text-slate-700">
            </div>
            <div v-if="!modoEdicionUsuario">
              <label class="block text-[11px] font-black text-slate-400 uppercase tracking-widest mb-1.5 ml-1">Contraseña</label>
              <input v-model="formUsuario.contrasena" type="text" required class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl outline-none transition font-medium text-slate-700">
            </div>
            <div>
              <label class="block text-[11px] font-black text-slate-400 uppercase tracking-widest mb-1.5 ml-1">Rol</label>
              <select v-model="formUsuario.rol" class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl outline-none transition font-bold text-slate-700">
                <option value="AUTOR">AUTOR</option>
                <option value="MODERADOR">MODERADOR</option>
                <option value="ADMINISTRADOR">ADMINISTRADOR</option>
              </select>
            </div>
            <div class="pt-6 mt-6 border-t border-slate-100 flex justify-end gap-3">
              <button type="button" @click="mostrarModalUsuario = false" class="px-5 py-2.5 text-slate-500 font-bold hover:bg-slate-100 rounded-xl transition">Cancelar</button>
              <button type="submit" :disabled="procesando" class="bg-blue-600 text-white font-bold px-6 py-2.5 rounded-xl hover:bg-blue-700 shadow-md transition disabled:opacity-50">
                {{ procesando ? 'Guardando...' : 'Guardar' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div v-if="mostrarModalCategoria" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4 animate-fade-in">
      <div class="bg-white rounded-[2rem] shadow-2xl w-full max-w-lg overflow-hidden transform transition-all border border-slate-100">
        <div class="p-8">
          <div class="flex justify-between items-center mb-6 border-b border-slate-100 pb-4">
            <h2 class="text-2xl font-black text-slate-800">{{ modoEdicionCategoria ? 'Editar Categoría' : 'Nueva Categoría' }}</h2>
            <button @click="mostrarModalCategoria = false" class="text-slate-400 hover:text-rose-500 text-3xl font-bold transition leading-none">&times;</button>
          </div>
          <form @submit.prevent="guardarCategoria" class="space-y-5">
            <div>
              <label class="block text-[11px] font-black text-slate-400 uppercase tracking-widest mb-1.5 ml-1">Nombre de la Categoría</label>
              <input v-model="formCategoria.nombre" type="text" required placeholder="Ej. Políticas Públicas" class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:border-[#7a1b2e] focus:ring-4 focus:ring-[#7a1b2e]/10 outline-none transition font-medium text-slate-700">
            </div>
            <div>
              <label class="block text-[11px] font-black text-slate-400 uppercase tracking-widest mb-1.5 ml-1">Descripción (Opcional)</label>
              <textarea v-model="formCategoria.descripcion" rows="3" placeholder="Detalla de qué trata esta categoría..." class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:border-[#7a1b2e] focus:ring-4 focus:ring-[#7a1b2e]/10 outline-none transition font-medium text-slate-700 resize-none"></textarea>
            </div>
            <div class="pt-6 mt-6 border-t border-slate-100 flex justify-end gap-3">
              <button type="button" @click="mostrarModalCategoria = false" class="px-5 py-2.5 text-slate-500 font-bold hover:bg-slate-100 rounded-xl transition">Cancelar</button>
              <button type="submit" :disabled="procesando" class="bg-[#7a1b2e] text-white font-bold px-6 py-2.5 rounded-xl hover:bg-[#5a1422] shadow-md transition disabled:opacity-50">
                {{ procesando ? 'Guardando...' : 'Guardar' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import api from '../services/api';
import Swal from 'sweetalert2';
import { notificarExito, notificarError } from '../services/alertas';

const pestana = ref('usuarios'); // Controla qué tabla ver
const nombreAdmin = ref('Cargando...'); 
const procesando = ref(false);

// --- ESTADOS: USUARIOS ---
const usuarios = ref([]);
const cargandoUsuarios = ref(false);
const busquedaUsuario = ref('');
const mostrarModalUsuario = ref(false);
const modoEdicionUsuario = ref(false);
const idUsuarioActual = ref(null);
const formUsuario = ref({ nombre: '', correo: '', contrasena: '', rol: 'AUTOR' });

// --- ESTADOS: CATEGORÍAS ---
const categorias = ref([]);
const cargandoCategorias = ref(false);
const busquedaCategoria = ref('');
const mostrarModalCategoria = ref(false);
const modoEdicionCategoria = ref(false);
const idCategoriaActual = ref(null);
const formCategoria = ref({ nombre: '', descripcion: '' });

// --- FILTROS ---
const usuariosFiltrados = computed(() => {
  if (!busquedaUsuario.value) return usuarios.value;
  const t = busquedaUsuario.value.toLowerCase();
  return usuarios.value.filter(u => u.nombre.toLowerCase().includes(t) || u.correo.toLowerCase().includes(t));
});

const categoriasFiltradas = computed(() => {
  if (!busquedaCategoria.value) return categorias.value;
  const t = busquedaCategoria.value.toLowerCase();
  return categorias.value.filter(c => c.nombre.toLowerCase().includes(t));
});

// --- INICIALIZACIÓN ---
const cargarPerfilReal = async () => {
  try {
    const res = await api.get('/auth/me');
    nombreAdmin.value = res.data.nombre; 
  } catch (error) {
    nombreAdmin.value = 'Administrador';
  }
};

const cargarUsuarios = async () => {
  cargandoUsuarios.value = true;
  try {
    const res = await api.get('/usuarios/');
    usuarios.value = res.data.map(u => ({ ...u, activo: u.activo !== undefined ? u.activo : true }));
  } catch (error) {
    notificarError('No se pudieron cargar los usuarios.');
  } finally { cargandoUsuarios.value = false; }
};

const cargarCategorias = async () => {
  cargandoCategorias.value = true;
  try {
    const res = await api.get('/categorias/');
    categorias.value = res.data;
  } catch (error) {
    notificarError('No se pudieron cargar las categorías.');
  } finally { cargandoCategorias.value = false; }
};

onMounted(() => {
  cargarPerfilReal();
  cargarUsuarios();
  cargarCategorias();
});

// --- LÓGICA DE USUARIOS ---
const abrirModalUsuario = () => {
  modoEdicionUsuario.value = false;
  formUsuario.value = { nombre: '', correo: '', contrasena: '', rol: 'AUTOR' };
  mostrarModalUsuario.value = true;
};
const abrirModalEditar = (u) => {
  modoEdicionUsuario.value = true;
  idUsuarioActual.value = u.id;
  formUsuario.value = { nombre: u.nombre, correo: u.correo, rol: u.rol };
  mostrarModalUsuario.value = true;
};
const guardarUsuario = async () => {
  procesando.value = true;
  try {
    if (modoEdicionUsuario.value) await api.put(`/usuarios/${idUsuarioActual.value}`, formUsuario.value);
    else await api.post('/usuarios/', formUsuario.value);
    notificarExito('Usuario guardado exitosamente.');
    mostrarModalUsuario.value = false;
    cargarUsuarios();
  } catch (error) { notificarError('Ocurrió un error al guardar.'); } 
  finally { procesando.value = false; }
};
const confirmarEliminarUsuario = async (id, nombre) => {
  const result = await Swal.fire({ title: '¿Eliminar?', text: `Borrarás a ${nombre}`, icon: 'warning', showCancelButton: true });
  if (result.isConfirmed) {
    try {
      await api.delete(`/usuarios/${id}`);
      notificarExito('Usuario eliminado.');
      cargarUsuarios();
    } catch (e) { notificarError('Error al eliminar.'); }
  }
};
const cambiarEstadoUsuario = async (u) => { /* Lógica de tu toggle aquí */ };

// --- LÓGICA DE CATEGORÍAS ---
const abrirModalCategoria = () => {
  modoEdicionCategoria.value = false;
  formCategoria.value = { nombre: '', descripcion: '' };
  mostrarModalCategoria.value = true;
};
const editarModalCategoria = (cat) => {
  modoEdicionCategoria.value = true;
  idCategoriaActual.value = cat.id;
  formCategoria.value = { nombre: cat.nombre, descripcion: cat.descripcion };
  mostrarModalCategoria.value = true;
};
const guardarCategoria = async () => {
  procesando.value = true;
  try {
    if (modoEdicionCategoria.value) await api.put(`/categorias/${idCategoriaActual.value}`, formCategoria.value);
    else await api.post('/categorias/', formCategoria.value);
    notificarExito('Categoría guardada exitosamente.');
    mostrarModalCategoria.value = false;
    cargarCategorias();
  } catch (error) { 
    notificarError(error.response?.data?.detail || 'Ocurrió un error al guardar la categoría.'); 
  } finally { procesando.value = false; }
};
const confirmarEliminarCategoria = async (id, nombre) => {
  const result = await Swal.fire({ 
    title: '<span style="color:#1e293b; font-weight:900;">¿Borrar Categoría?</span>', 
    html: `<p style="color:#64748b;">Eliminarás la categoría <b>"${nombre}"</b>.</p>`, 
    icon: 'warning', 
    showCancelButton: true,
    confirmButtonColor: '#f43f5e',
    cancelButtonColor: '#94a3b8',
    confirmButtonText: 'Sí, Borrar',
    customClass: { popup: 'rounded-3xl shadow-2xl font-sans', confirmButton: 'font-bold rounded-xl px-6 py-3', cancelButton: 'font-bold rounded-xl px-6 py-3'}
  });
  if (result.isConfirmed) {
    try {
      await api.delete(`/categorias/${id}`);
      notificarExito('Categoría eliminada.');
      cargarCategorias();
    } catch (e) { notificarError('Error al eliminar. Posiblemente esté en uso por una revista.'); }
  }
};

// --- LÓGICA PARA CAMBIAR MI PROPIA CONTRASEÑA ---
const cambiarMiContrasena = async () => {
  const { value: formValues } = await Swal.fire({
    title: '<span style="color:#1e293b; font-weight:900;">Actualizar Seguridad</span>',
    html: `
      <div class="text-left mt-2 space-y-4 font-sans">
        <div>
          <label class="block text-xs font-bold text-slate-400 uppercase tracking-widest mb-1.5 ml-1">Contraseña Actual</label>
          <input id="swal-actual" type="password" class="w-full border border-slate-200 bg-slate-50 rounded-xl px-4 py-3 focus:border-[#7a1b2e] focus:ring-4 focus:ring-[#7a1b2e]/10 outline-none transition font-medium text-slate-700" placeholder="••••••••">
        </div>
        <div>
          <label class="block text-xs font-bold text-slate-400 uppercase tracking-widest mb-1.5 ml-1">Nueva Contraseña</label>
          <input id="swal-nueva" type="password" class="w-full border border-slate-200 bg-slate-50 rounded-xl px-4 py-3 focus:border-[#7a1b2e] focus:ring-4 focus:ring-[#7a1b2e]/10 outline-none transition font-medium text-slate-700" placeholder="Mínimo 6 caracteres">
        </div>
        <div>
          <label class="block text-xs font-bold text-slate-400 uppercase tracking-widest mb-1.5 ml-1">Confirmar Nueva Contraseña</label>
          <input id="swal-confirmar" type="password" class="w-full border border-slate-200 bg-slate-50 rounded-xl px-4 py-3 focus:border-[#7a1b2e] focus:ring-4 focus:ring-[#7a1b2e]/10 outline-none transition font-medium text-slate-700" placeholder="Repite la nueva contraseña">
        </div>
      </div>
    `,
    showCancelButton: true,
    confirmButtonText: 'Actualizar Contraseña',
    cancelButtonText: 'Cancelar',
    confirmButtonColor: '#7a1b2e',
    cancelButtonColor: '#94a3b8',
    customClass: {
      popup: 'rounded-[2rem] shadow-2xl font-sans border border-slate-100',
      confirmButton: 'font-bold rounded-xl px-6 py-3',
      cancelButton: 'font-bold rounded-xl px-6 py-3'
    },
    preConfirm: () => {
      const actual = document.getElementById('swal-actual').value;
      const nueva = document.getElementById('swal-nueva').value;
      const confirmar = document.getElementById('swal-confirmar').value;

      if (!actual || !nueva || !confirmar) {
        Swal.showValidationMessage('Por favor, completa todos los campos.');
        return false;
      }
      if (nueva.length < 6) {
        Swal.showValidationMessage('La nueva contraseña debe tener al menos 6 caracteres.');
        return false;
      }
      if (nueva !== confirmar) {
        Swal.showValidationMessage('Las contraseñas nuevas no coinciden.');
        return false;
      }
      
      return { contrasena_actual: actual, nueva_contrasena: nueva };
    }
  });

  if (formValues) {
    try {
      Swal.fire({ title: 'Guardando...', allowOutsideClick: false, didOpen: () => Swal.showLoading() });
      
      const respuesta = await api.put('/auth/me/cambiar-contrasena', formValues);
      
      Swal.fire({
        title: '¡Actualizada!',
        text: respuesta.data.mensaje,
        icon: 'success',
        confirmButtonColor: '#7a1b2e',
        customClass: { popup: 'rounded-3xl font-sans', confirmButton: 'font-bold rounded-xl px-6 py-3' }
      });

    } catch (error) {
      Swal.fire({
        title: 'Error',
        text: error.response?.data?.detail || 'No se pudo actualizar la contraseña.',
        icon: 'error',
        confirmButtonColor: '#7a1b2e',
        customClass: { popup: 'rounded-3xl font-sans', confirmButton: 'font-bold rounded-xl px-6 py-3' }
      });
    }
  }
};
</script>

<style scoped>
.animate-fade-in { animation: fadeIn 0.4s ease-out forwards; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
</style>