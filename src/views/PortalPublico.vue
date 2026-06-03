<template>
  <div class="min-h-screen bg-slate-50 font-sans pb-16">
    
    <div class="relative bg-slate-900 text-white py-16 md:py-24 overflow-hidden border-b border-[#7a1b2e]/30">
      <div class="absolute inset-0 z-0">
        <img src="https://images.unsplash.com/photo-1541339907198-e08759df9a04?q=80&w=2000&auto=format&fit=crop" 
             class="w-full h-full object-cover opacity-20">
        <div class="absolute inset-0 bg-gradient-to-br from-slate-900/90 via-[#7a1b2e]/60 to-slate-900/90 backdrop-blur-sm"></div>
      </div>

      <div class="relative z-10 container mx-auto px-4 text-center">
        <h1 class="text-4xl md:text-6xl font-black mb-4 tracking-tight drop-shadow-xl">
          Revista Digital <span class="text-white/80 font-light">UMSA</span>
        </h1>
        <p class="text-lg md:text-xl text-blue-100/80 max-w-2xl mx-auto font-medium">
          Accede a la producción académica de la Facultad de Ciencias Sociales.
        </p>
      </div>
    </div>

    <div class="container mx-auto px-4 -mt-8 relative z-20">
      <div class="bg-white rounded-3xl shadow-[0_15px_50px_-12px_rgba(0,0,0,0.1)] p-6 md:p-8 border border-slate-100 flex flex-col md:flex-row gap-6 items-end">
        
        <div class="flex-[2] w-full">
          <label class="block text-[11px] font-black text-slate-400 uppercase tracking-widest mb-2 ml-1">¿Qué estás buscando?</label>
          <div class="relative">
            <span class="absolute left-4 top-3.5">🔍</span>
            <input v-model="busqueda" type="text" placeholder="Título o tema de investigación..." 
              class="w-full pl-11 pr-4 py-3.5 bg-slate-50 border border-slate-200 rounded-2xl focus:bg-white focus:border-[#7a1b2e] focus:ring-4 focus:ring-[#7a1b2e]/5 outline-none transition font-medium">
          </div>
        </div>

        <div class="flex-1 w-full">
          <label class="block text-[11px] font-black text-slate-400 uppercase tracking-widest mb-2 ml-1">Filtrar por Categoría</label>
          <select v-model="categoriaSeleccionada" 
            class="w-full px-4 py-3.5 bg-slate-50 border border-slate-200 rounded-2xl focus:bg-white focus:border-[#7a1b2e] outline-none transition font-bold text-slate-600 appearance-none cursor-pointer">
            <option value="Todas">Todas las áreas</option>
            <option v-for="cat in categorias" :key="cat.id" :value="cat.nombre">{{ cat.nombre }}</option>
          </select>
        </div>

        <button @click="limpiarFiltros" class="px-6 py-3.5 text-slate-400 font-bold hover:text-[#7a1b2e] transition text-sm">
          Limpiar
        </button>
      </div>
    </div>

    <div class="container mx-auto px-4 mt-12">
      <div v-if="cargando" class="flex flex-col items-center justify-center py-20">
        <div class="w-12 h-12 border-4 border-[#7a1b2e] border-t-transparent rounded-full animate-spin"></div>
        <p class="mt-4 text-slate-400 font-bold animate-pulse">Cargando repositorio...</p>
      </div>

      <div v-else-if="revistasFiltradas.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
        <div v-for="revista in revistasFiltradas" :key="revista.id" 
             class="bg-white rounded-3xl shadow-sm hover:shadow-2xl transition-all duration-500 border border-slate-100 flex flex-col group overflow-hidden">
          
          <div class="relative h-64 bg-slate-100 overflow-hidden cursor-pointer" @click="irARevista(revista.id)">
            <img v-if="revista.ruta_portada" :src="`http://localhost:8000${revista.ruta_portada}`" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700">
            <div v-else class="w-full h-full flex flex-col items-center justify-center text-slate-500">
              <span class="text-sm font-semibold uppercase tracking-widest">Portada no disponible</span>
            </div>
            <span class="absolute bottom-4 left-4 bg-white/90 backdrop-blur-md text-[#7a1b2e] text-[10px] font-black px-3 py-1.5 rounded-xl shadow-sm border border-slate-100 uppercase">
              {{ revista.categoria }}
            </span>
          </div>

          <div class="p-6 flex-grow flex flex-col">
            <h3 class="font-black text-slate-800 text-lg leading-snug mb-2 line-clamp-2">{{ revista.titulo }}</h3>
            <p class="text-xs text-slate-400 font-bold uppercase tracking-tight mb-4">Facultad de Ciencias Sociales</p>

            <div class="mt-auto flex items-center gap-2 pt-5 border-t border-slate-50">
              <button @click="irARevista(revista.id)" class="flex-grow bg-slate-900 text-white font-bold py-3 rounded-xl hover:bg-[#7a1b2e] transition shadow-md flex items-center justify-center gap-2 text-sm">
                Leer edición
              </button>
              
              <button @click="copiarURL(revista.id)" class="p-3 bg-slate-50 text-slate-400 hover:text-blue-600 hover:bg-blue-50 border border-slate-200 rounded-xl transition shadow-sm" title="Compartir enlace">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" /></svg>
              </button>

              <button v-if="rolUsuario === 'ADMINISTRADOR'" @click="eliminarRevista(revista.id, revista.titulo)" class="p-3 bg-rose-50 text-rose-500 hover:text-white hover:bg-rose-500 border border-rose-200 rounded-xl transition shadow-sm" title="Eliminar Revista (Solo Admin)">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="text-center py-24 bg-white rounded-[2rem] border-2 border-dashed border-slate-200">
        <h3 class="text-xl font-black text-slate-800 mb-4">No encontramos lo que buscas</h3>
        <p class="text-slate-400 mt-1 font-medium">Prueba con otros términos o cambia la categoría.</p>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '../services/api';
import { notificarExito, notificarError } from '../services/alertas';
import Swal from 'sweetalert2';

const router = useRouter();
const cargando = ref(true);
const revistas = ref([]);
const busqueda = ref('');
const categoriaSeleccionada = ref('Todas');

// NUEVO: Variable para las categorías que vienen de la Base de Datos
const categorias = ref([]);

const cargarCategorias = async () => {
  try {
    const res = await api.get('/categorias/');
    categorias.value = res.data;
  } catch (error) {
    console.error("Error al cargar categorías", error);
  }
};

const cargarRevistas = async () => {
  cargando.value = true;
  try {
    const res = await api.get('/revistas/publicas'); 
    revistas.value = res.data;
  } catch (error) {
    notificarError('No se pudo conectar con el repositorio.');
  } finally {
    cargando.value = false;
  }
};

onMounted(() => {
  cargarCategorias(); // Cargar categorías reales
  cargarRevistas();
});

const revistasFiltradas = computed(() => {
  return revistas.value.filter(r => {
    const cumpleTexto = r.titulo.toLowerCase().includes(busqueda.value.toLowerCase());
    const cumpleCat = categoriaSeleccionada.value === 'Todas' || r.categoria === categoriaSeleccionada.value;
    return cumpleTexto && cumpleCat;
  });
});

const limpiarFiltros = () => {
  busqueda.value = '';
  categoriaSeleccionada.value = 'Todas';
};

const irARevista = (id) => router.push(`/revista/${id}`);

const rolUsuario = ref(localStorage.getItem('rol_usuario') || '');

const eliminarRevista = async (id, titulo) => {
  const result = await Swal.fire({
    title: '<span style="color:#1e293b; font-weight:900;">¿Eliminar revista?</span>',
    html: `<p style="color:#64748b;">Borrarás permanentemente la edición <b>"${titulo}"</b> de la plataforma pública. Esta acción no se puede deshacer.</p>`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#f43f5e', 
    cancelButtonColor: '#94a3b8',
    confirmButtonText: 'Sí, Eliminar Definitivamente',
    cancelButtonText: 'Cancelar',
    customClass: {
      popup: 'rounded-3xl shadow-2xl font-sans',
      confirmButton: 'font-bold rounded-xl px-6 py-3',
      cancelButton: 'font-bold rounded-xl px-6 py-3'
    }
  });

  if (result.isConfirmed) {
    try {
      await api.delete(`/revistas/${id}`);
      notificarExito('Revista eliminada de la plataforma.');
      cargarRevistas(); 
    } catch (error) {
      notificarError(error.response?.data?.detail || 'No se pudo eliminar la revista.');
    }
  }
};

const copiarURL = (id) => {
  const url = `${window.location.origin}/revista/${id}`;
  navigator.clipboard.writeText(url).then(() => {
    notificarExito('Enlace de la revista copiado al portapapeles');
  });
};
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>