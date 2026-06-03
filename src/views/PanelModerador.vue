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
          <div class="w-16 h-16 bg-white rounded-2xl flex items-center justify-center text-[#7a1b2e] text-2xl font-black shadow-[0_0_20px_rgba(122,27,46,0.4)] border border-white/20">
            {{ nombreModerador.charAt(0).toUpperCase() }}
          </div>
          <div>
            <div class="flex items-center gap-3 mb-1">
              <h1 class="text-3xl font-black text-white tracking-tight drop-shadow-md">
                {{ nombreModerador }}
              </h1>
              <span class="bg-blue-500/20 backdrop-blur-md text-blue-300 text-[10px] font-black px-3 py-1.5 rounded-lg uppercase tracking-widest border border-blue-400/30 shadow-sm flex items-center gap-1.5">
                <span class="w-1.5 h-1.5 rounded-full bg-blue-400 animate-pulse"></span> {{ rolActual }}
              </span>
            </div>
            
            <p class="text-sm text-slate-300 font-medium flex items-center gap-4">
              Facultad de Ciencias Sociales • Panel de Control
              
              <button @click="cambiarMiContrasena" class="text-xs text-blue-300 hover:text-white font-bold flex items-center gap-1 bg-white/5 hover:bg-white/20 px-2 py-1 rounded-md transition border border-white/10">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4v-3.21l5.586-5.586A6 6 0 0115 9z" /></svg>
                Cambiar clave
              </button>
            </p>
          </div>
        </div>
        
        <div class="flex bg-slate-800/50 p-1.5 rounded-2xl backdrop-blur-md border border-white/10 shadow-lg">
          <button 
            @click="pestana = 'pendientes'" 
            :class="pestana === 'pendientes' ? 'bg-white text-slate-900 shadow-md' : 'text-slate-300 hover:text-white hover:bg-white/10'"
            class="px-5 py-2.5 rounded-xl transition-all duration-300 text-sm font-bold flex items-center gap-2"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            Pendientes
            <span v-if="revistasPendientes.length > 0" class="bg-rose-500 text-white text-[10px] px-2 py-0.5 rounded-md ml-1">
              {{ revistasPendientes.length }}
            </span>
          </button>
          <button 
            @click="pestana = 'historial'" 
            :class="pestana === 'historial' ? 'bg-[#7a1b2e] text-white shadow-md border border-[#7a1b2e]/50' : 'text-slate-300 hover:text-white hover:bg-white/10'"
            class="px-5 py-2.5 rounded-xl transition-all duration-300 text-sm font-bold flex items-center gap-2"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002 2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>
            Historial de Moderación
          </button>
        </div>
      </div>
    </div>

    <div class="max-w-[1400px] mx-auto px-4 md:px-8 -mt-8 relative z-20 space-y-8">

      <div v-if="cargando" class="flex flex-col items-center justify-center py-20 bg-white rounded-[2rem] shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-100">
        <div class="w-12 h-12 border-4 border-slate-200 border-t-blue-500 rounded-full animate-spin mb-4"></div>
        <p class="text-slate-500 font-bold tracking-widest uppercase text-xs animate-pulse">Sincronizando registros...</p>
      </div>

      <div v-else-if="pestana === 'pendientes'" class="animate-fade-in">
        <div v-if="revistasPendientes.length === 0" class="text-center py-24 bg-white rounded-[2rem] shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-100">
          <div class="w-24 h-24 bg-emerald-50 rounded-full flex items-center justify-center mx-auto mb-6 border border-emerald-100 shadow-sm">
            <span class="text-4xl">🎉</span>
          </div>
          <h3 class="text-2xl font-black text-slate-800">¡Bandeja al día!</h3>
          <p class="text-slate-500 font-medium mt-2 max-w-sm mx-auto">No tienes ninguna revista pendiente de revisión en este momento. Buen trabajo.</p>
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <div v-for="revista in revistasPendientes" :key="revista.id" class="bg-white rounded-[1.5rem] shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-100 overflow-hidden flex flex-col transition-all duration-300 hover:shadow-xl hover:-translate-y-1 group">
            
            <div class="h-52 bg-slate-100 relative overflow-hidden">
              <img :src="'http://localhost:8000' + revista.ruta_portada" @error="manejarErrorImagen" class="w-full h-full object-cover object-top transition-transform duration-700 group-hover:scale-105" />
              <div class="absolute inset-0 bg-slate-900/60 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center backdrop-blur-[2px]">
                <a :href="'http://localhost:8000' + revista.ruta_pdf" target="_blank" class="bg-white text-slate-900 font-bold px-5 py-2.5 rounded-xl flex items-center gap-2 transform translate-y-4 group-hover:translate-y-0 transition-all duration-300 shadow-lg hover:bg-blue-50">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                  Revisar PDF
                </a>
              </div>
            </div>
            
            <div class="p-6 flex-grow flex flex-col">
              <div class="flex items-start justify-between mb-3">
                <span class="text-[10px] font-black text-slate-500 bg-slate-100 uppercase tracking-widest px-2.5 py-1 rounded-md">{{ revista.categoria }}</span>
                <span class="text-[10px] font-bold text-slate-400">{{ new Date(revista.fecha_creacion).toLocaleDateString() }}</span>
              </div>
              
              <h3 class="text-lg font-black text-slate-800 leading-tight mb-1 line-clamp-2" :title="revista.titulo">{{ revista.titulo }}</h3>
              
              <p class="text-[11px] text-slate-500 font-bold mb-3 uppercase tracking-wide flex items-center gap-1">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
                Autor: <span class="text-blue-600">{{ revista.autor ? revista.autor.nombre : 'Desconocido' }}</span>
              </p>

              <p class="text-sm text-slate-500 line-clamp-2 mb-4 font-medium">{{ revista.descripcion }}</p>
              
              <div class="mt-auto grid grid-cols-2 gap-3 pt-5 border-t border-slate-100">
                <button @click="confirmarAprobacion(revista)" class="bg-emerald-50 text-emerald-700 hover:bg-emerald-500 hover:text-white border border-emerald-200 hover:border-emerald-500 font-bold py-2.5 rounded-xl transition-all duration-300 flex items-center justify-center gap-1.5 text-sm shadow-sm">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>
                  Aprobar
                </button>
                <button @click="solicitarCorreccion(revista)" class="bg-rose-50 text-rose-700 hover:bg-rose-500 hover:text-white border border-rose-200 hover:border-rose-500 font-bold py-2.5 rounded-xl transition-all duration-300 flex items-center justify-center gap-1.5 text-sm shadow-sm">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
                  Rechazar
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else-if="pestana === 'historial'" class="animate-fade-in bg-white rounded-[2rem] shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-100 overflow-hidden">
        
        <div class="px-8 py-6 flex justify-between items-center bg-slate-50/50 border-b border-slate-100">
          <div>
            <h3 class="text-xl font-black text-slate-800">
              {{ rolActual === 'ADMINISTRADOR' ? 'Historial Global de Moderación' : 'Mi Historial de Moderación' }}
            </h3>
            <p class="text-sm text-slate-500 mt-1">
              {{ rolActual === 'ADMINISTRADOR' ? 'Auditoría completa de todas las evaluaciones del sistema.' : 'Registro de las ediciones que has evaluado.' }}
            </p>
          </div>
          <button @click="cargarRevistas" class="text-slate-600 bg-white hover:bg-slate-50 px-4 py-2.5 rounded-xl text-sm font-bold transition flex items-center gap-2 border border-slate-200 shadow-sm">
            <span :class="{'animate-spin': cargando}">🔄</span> Refrescar
          </button>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left text-sm">
            <thead class="text-slate-400 uppercase tracking-wider text-xs font-bold bg-white">
              <tr>
                <th class="px-8 py-5">Revista y Autor</th>
                <th class="px-8 py-5">Fecha de Subida</th>
                <th class="px-8 py-5">Estado Final</th>
                <th v-if="rolActual === 'ADMINISTRADOR'" class="px-8 py-5">Moderador Responsable</th>
                <th class="px-8 py-5">Acciones</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              
              <tr v-if="historialRevistas.length === 0">
                <td :colspan="rolActual === 'ADMINISTRADOR' ? 5 : 4" class="px-8 py-20 text-center">
                  <div class="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-4 border border-slate-100">
                    <span class="text-2xl text-slate-400">📂</span>
                  </div>
                  <h4 class="text-lg font-black text-slate-800">No hay registros históricos</h4>
                  <p class="text-slate-500 mt-1">Las revistas que apruebes o rechaces aparecerán aquí.</p>
                </td>
              </tr>

              <tr v-for="revista in historialRevistas" :key="revista.id" class="hover:bg-slate-50/50 transition duration-200">
                <td class="px-8 py-5">
                  <p class="font-black text-slate-800 text-base mb-1">{{ revista.titulo }}</p>
                  
                  <p class="text-[11px] text-slate-500 font-bold mb-2 uppercase tracking-wide">
                    Autor: <span class="text-blue-600">{{ revista.autor ? revista.autor.nombre : 'Desconocido' }}</span>
                  </p>
                  
                  <p class="text-xs text-slate-500 font-medium">
                    <span class="bg-slate-100 px-2 py-0.5 rounded text-slate-600">{{ revista.categoria }}</span>
                  </p>
                </td>
                
                <td class="px-8 py-5 text-slate-500 font-medium">
                  {{ new Date(revista.fecha_creacion).toLocaleDateString() }}
                </td>
                
                <td class="px-8 py-5">
                  <span :class="{
                      'bg-emerald-50 text-emerald-700 border-emerald-200': revista.estado === 'APROBADA',
                      'bg-rose-50 text-rose-700 border-rose-200': revista.estado === 'RECHAZADA'
                    }" class="px-3 py-1.5 rounded-lg text-xs font-bold tracking-wide flex inline-flex items-center gap-1.5 border">
                    <span :class="{
                        'bg-emerald-500': revista.estado === 'APROBADA',
                        'bg-rose-500': revista.estado === 'RECHAZADA'
                      }" class="w-1.5 h-1.5 rounded-full"></span>
                    {{ revista.estado }}
                  </span>
                </td>

                <td v-if="rolActual === 'ADMINISTRADOR'" class="px-8 py-5">
                  <div v-if="revista.revisiones && revista.revisiones.length > 0" class="flex items-center gap-2">
                    <div class="w-6 h-6 rounded-full bg-blue-100 text-blue-700 font-bold flex items-center justify-center text-[10px]">
                      {{ obtenerInicialModerador(revista.revisiones) }}
                    </div>
                    <span class="text-xs font-bold text-slate-700">{{ obtenerNombreModerador(revista.revisiones) }}</span>
                  </div>
                  <span v-else class="text-xs font-medium text-slate-400 italic">No registrado</span>
                </td>

                <td class="px-8 py-5">
                  <a v-if="revista.estado === 'APROBADA'" :href="'http://localhost:8000' + revista.ruta_pdf" target="_blank" class="text-blue-600 bg-blue-50 hover:bg-blue-600 hover:text-white px-4 py-2 rounded-xl text-xs font-bold transition inline-flex items-center gap-2">
                    Ver PDF
                  </a>
                  <div v-else-if="revista.revisiones && revista.revisiones.length > 0" class="text-xs text-slate-600 bg-slate-100 p-2.5 rounded-lg max-w-[200px] border border-slate-200 line-clamp-2" :title="obtenerUltimaRevision(revista.revisiones).observaciones">
                    <span class="font-bold text-rose-500">Motivo:</span> {{ obtenerUltimaRevision(revista.revisiones).observaciones }}
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
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

const revistas = ref([]);
const cargando = ref(true);
const pestana = ref('pendientes');

// VARIABLES DE SESIÓN 
const nombreModerador = ref('Cargando...'); 
const rolActual = ref('');
const idActual = ref(null);

// --- FILTROS COMPUTADOS AVANZADOS ---
const revistasPendientes = computed(() => revistas.value.filter(r => r.estado === 'PENDIENTE'));

const historialRevistas = computed(() => {
  const completadas = revistas.value.filter(r => r.estado !== 'PENDIENTE');

  if (rolActual.value === 'ADMINISTRADOR') {
    return completadas; 
  } else {
    return completadas.filter(r => {
      if (!r.revisiones || r.revisiones.length === 0) return false;
      return r.revisiones.some(rev => {
        const modId = rev.moderador_id || (rev.moderador && rev.moderador.id);
        return modId === idActual.value;
      });
    });
  }
});

const obtenerUltimaRevision = (revisiones) => {
  if (!revisiones || revisiones.length === 0) return null;
  const ordenadas = [...revisiones].sort((a, b) => new Date(a.fecha_revision) - new Date(b.fecha_revision));
  return ordenadas[ordenadas.length - 1];
};

const obtenerNombreModerador = (revisiones) => {
  const rev = obtenerUltimaRevision(revisiones);
  if (!rev) return 'Desconocido';
  if (rev.moderador && rev.moderador.nombre) return rev.moderador.nombre;
  return `ID: ${rev.moderador_id}`; 
};

const obtenerInicialModerador = (revisiones) => {
  const rev = obtenerUltimaRevision(revisiones);
  if (!rev) return '?';
  if (rev.moderador && rev.moderador.nombre) return rev.moderador.nombre.charAt(0).toUpperCase();
  return 'M';
};

const cargarPerfilReal = async () => {
  try {
    const res = await api.get('/auth/me');
    nombreModerador.value = res.data.nombre; 
    rolActual.value = res.data.rol;
    idActual.value = res.data.id;
  } catch (error) {
    nombreModerador.value = localStorage.getItem('usuario_correo')?.split('@')[0] || 'Gestor';
    rolActual.value = localStorage.getItem('rol_usuario') || 'MODERADOR';
  }
};

const cargarRevistas = async () => {
  cargando.value = true;
  try {
    const respuesta = await api.get('/revistas/admin/todas');
    revistas.value = respuesta.data;
  } catch (error) {
    console.error(error);
  } finally {
    cargando.value = false;
  }
};

onMounted(() => {
  cargarPerfilReal();
  cargarRevistas();
});

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

const confirmarAprobacion = async (revista) => {
  const result = await Swal.fire({
    title: '<span style="color:#1e293b; font-weight:900;">¿Aprobar publicación?</span>',
    html: `<p style="color:#64748b;">La revista <b>"${revista.titulo}"</b> pasará a ser visible para todo el público en la plataforma digital.</p>`,
    icon: 'question',
    showCancelButton: true,
    confirmButtonColor: '#10b981', 
    cancelButtonColor: '#94a3b8',
    confirmButtonText: 'Sí, Aprobar edición',
    cancelButtonText: 'Cancelar',
    customClass: {
      popup: 'rounded-3xl shadow-2xl font-sans',
      confirmButton: 'font-bold rounded-xl px-6 py-3',
      cancelButton: 'font-bold rounded-xl px-6 py-3'
    }
  });

  if (result.isConfirmed) {
    try {
      await api.put(`/revistas/${revista.id}/estado`, { estado: 'APROBADA' });
      notificarExito('Revista aprobada y publicada oficialmente.');
      cargarRevistas();
    } catch (error) {
      notificarError('Hubo un error al intentar aprobar la revista.');
    }
  }
};

const solicitarCorreccion = async (revista) => {
  const { value: motivo } = await Swal.fire({
    title: '<span style="color:#1e293b; font-weight:900;">Solicitar Corrección</span>',
    html: `
      <div class="text-left mt-2">
        <label class="block text-xs font-bold text-slate-400 uppercase tracking-widest mb-2">Motivo del rechazo / Feedback</label>
        <textarea id="swal-motivo" class="w-full border border-slate-200 bg-slate-50 rounded-xl p-4 focus:border-rose-500 focus:ring-4 focus:ring-rose-500/10 outline-none transition font-medium text-slate-700 resize-none" rows="3" placeholder="Ej. La calidad de la portada no es óptima o existen errores de formato en las páginas 3 y 4..."></textarea>
      </div>
    `,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#f43f5e', 
    cancelButtonColor: '#94a3b8',
    confirmButtonText: 'Rechazar Documento',
    cancelButtonText: 'Cancelar',
    customClass: {
      popup: 'rounded-3xl shadow-2xl font-sans',
      confirmButton: 'font-bold rounded-xl px-6 py-3',
      cancelButton: 'font-bold rounded-xl px-6 py-3'
    },
    preConfirm: () => {
      const texto = document.getElementById('swal-motivo').value;
      if (!texto) {
        Swal.showValidationMessage('Debes ingresar un motivo para que el autor pueda corregirlo.');
      }
      return texto;
    }
  });

  if (motivo) {
    try {
      await api.put(`/revistas/${revista.id}/estado`, { 
        estado: 'RECHAZADA',
        observaciones: motivo 
      });
      notificarExito('Revista rechazada. Se ha notificado al autor.');
      cargarRevistas();
    } catch (error) {
      notificarError('Hubo un error al procesar el rechazo.');
    }
  }
};

const manejarErrorImagen = (evento) => {
  evento.target.src = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="400" height="600"><rect width="400" height="600" fill="%23f8fafc"/><text x="50%" y="50%" font-family="sans-serif" font-size="20" font-weight="bold" text-anchor="middle" fill="%2394a3b8">Portada no disponible</text></svg>';
};
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.4s ease-out forwards;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>