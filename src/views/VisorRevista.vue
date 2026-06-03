<template>
  <div class="min-h-screen bg-slate-900 flex flex-col font-sans overflow-hidden relative">
    
    <div class="absolute inset-0 z-0 pointer-events-none">
      <img v-if="revista?.ruta_portada" :src="`http://localhost:8000${revista.ruta_portada}`" class="w-full h-full object-cover opacity-20 blur-3xl transition-opacity duration-1000">
      <div class="absolute inset-0 bg-slate-900/70"></div>
    </div>

    <header v-if="revista" class="relative z-20 bg-slate-900/50 backdrop-blur-xl border-b border-white/10 px-6 py-4 flex justify-between items-center shrink-0 shadow-lg">
      <div class="flex items-center gap-4">
        <button @click="volverAtras" class="p-2.5 bg-white/5 hover:bg-white/10 rounded-xl transition text-white border border-white/10 shadow-sm" title="Volver al repositorio">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
        </button>
        
        <div>
          <h2 class="text-white font-black text-lg leading-tight tracking-tight">{{ revista.titulo }}</h2>
          <div class="flex items-center gap-2 mt-0.5">
            <span class="text-[10px] font-black uppercase tracking-widest text-[#7a1b2e] bg-white px-2 py-0.5 rounded-md">
              {{ revista.categoria }}
            </span>
            <span class="text-xs text-slate-400 font-medium hidden md:inline">Facultad de Ciencias Sociales</span>
          </div>
        </div>
      </div>

      <div class="flex gap-3 items-center">
        <button @click="abrirModalResena" class="bg-[#7a1b2e] hover:bg-[#5a1422] text-white transition-colors duration-300 px-5 py-2.5 rounded-xl text-sm font-bold flex items-center gap-2 shadow-lg shadow-[#7a1b2e]/20 border border-[#7a1b2e]/50">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.518 4.674a1 1 0 00.95.69h4.908c.969 0 1.371 1.24.588 1.81l-3.974 2.888a1 1 0 00-.364 1.118l1.518 4.674c.3.921-.755 1.688-1.539 1.118l-3.974-2.888a1 1 0 00-1.176 0l-3.974 2.888c-.784.57-1.838-.197-1.539-1.118l1.518-4.674a1 1 0 00-.364-1.118L2.132 9.101c-.783-.57-.38-1.81.588-1.81h4.908a1 1 0 00.95-.69l1.518-4.674z"/></svg>
          Calificar
        </button>
      </div>
    </header>

    <div v-if="cargando" class="flex-grow flex flex-col items-center justify-center relative z-20">
      <div class="w-14 h-14 border-4 border-slate-700 border-t-[#7a1b2e] rounded-full animate-spin mb-6 shadow-lg"></div>
      <p class="text-slate-200 font-bold text-lg animate-pulse tracking-wide">{{ mensajeCarga }}</p>
    </div>

    <main 
      :class="cargando ? 'opacity-0 absolute inset-0 pointer-events-none' : 'opacity-100 relative z-10'" 
      class="flex-grow flex items-center justify-center p-4 transition-opacity duration-700 overflow-hidden"
    >
      <button 
        @click="pasarPaginaAnterior" 
        class="absolute left-2 md:left-8 z-30 bg-slate-900/60 backdrop-blur-sm border border-white/10 hover:bg-[#7a1b2e] text-white p-4 rounded-2xl transition-all duration-300 hidden md:block shadow-2xl hover:scale-110 group"
        :class="{'opacity-0 cursor-not-allowed pointer-events-none': !puedeRetroceder}"
        :disabled="!puedeRetroceder"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-slate-300 group-hover:text-white transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7" /></svg>
      </button>
      
      <div class="relative group">
        <div 
          id="flipbook-container" 
          class="shadow-[0_20px_50px_rgba(0,0,0,0.5)] mx-auto rounded-r-sm"
          :style="{ width: anchoContenedor, height: alturaContenedor }"
        ></div>
        
        <div class="absolute -bottom-8 left-0 w-full text-center hidden md:block">
           <span class="bg-slate-900/80 backdrop-blur-md border border-white/10 text-slate-300 text-xs font-bold px-4 py-1.5 rounded-full shadow-lg">
             Página {{ paginaActual }} de {{ totalPaginas }}
           </span>
        </div>
      </div>

      <button 
        @click="pasarPaginaSiguiente" 
        class="absolute right-2 md:right-8 z-30 bg-slate-900/60 backdrop-blur-sm border border-white/10 hover:bg-[#7a1b2e] text-white p-4 rounded-2xl transition-all duration-300 hidden md:block shadow-2xl hover:scale-110 group"
        :class="{'opacity-0 cursor-not-allowed pointer-events-none': !puedeAvanzar}"
        :disabled="!puedeAvanzar"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-slate-300 group-hover:text-white transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7" /></svg>
      </button>
    </main>

    <div v-if="!cargando" class="md:hidden bg-slate-900/90 backdrop-blur-lg border-t border-white/10 text-white py-3 px-4 flex justify-between items-center relative z-20 shrink-0 pb-safe">
      <button @click="pasarPaginaAnterior" :disabled="!puedeRetroceder" :class="!puedeRetroceder ? 'opacity-30' : ''" class="p-3 bg-white/10 rounded-xl active:bg-white/20 transition">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg>
      </button>
      <span class="text-xs font-black tracking-widest text-slate-400 bg-black/30 px-4 py-2 rounded-lg border border-white/5 uppercase">
        {{ paginaActual }} / {{ totalPaginas }}
      </span>
      <button @click="pasarPaginaSiguiente" :disabled="!puedeAvanzar" :class="!puedeAvanzar ? 'opacity-30' : ''" class="p-3 bg-white/10 rounded-xl active:bg-white/20 transition">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
      </button>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../services/api';

import { PageFlip } from 'page-flip';
import * as pdfjsLib from 'pdfjs-dist';
import pdfWorker from 'pdfjs-dist/build/pdf.worker.mjs?url';

import Swal from 'sweetalert2';
import { notificarExito, notificarError } from '../services/alertas';

pdfjsLib.GlobalWorkerOptions.workerSrc = pdfWorker;

const ruta = useRoute();
const enrutador = useRouter();

const revista = ref(null);
const cargando = ref(true);
const mensajeCarga = ref('Conectando con el repositorio...');

const alturaContenedor = ref('600px');
const anchoContenedor = ref('800px');
const paginaActual = ref(1);
const totalPaginas = ref(0);
const puedeRetroceder = ref(false);
const puedeAvanzar = ref(true);
let libro = null;

let tiempoInicioLectura = null;

// --- LÓGICA CORREGIDA: REGISTRO DE TIEMPO DE LECTURA SEGURO ---
const registrarTiempoLectura = () => {
  if (!tiempoInicioLectura) return;
  
  const segundosLeidos = Math.floor((Date.now() - tiempoInicioLectura) / 1000);
  
  // Guardamos únicamente lecturas significativas (mayores a 5 segundos)
  if (segundosLeidos > 5) {
    const blob = new Blob([JSON.stringify({ segundos: segundosLeidos })], { type: 'application/json' });
    // sendBeacon garantiza que los datos viajen incluso si se cierra la pestaña bruscamente
    navigator.sendBeacon(`http://localhost:8000/api/revistas/${ruta.params.id}/tiempo`, blob);
  }
  tiempoInicioLectura = null; 
};

const volverAtras = () => {
  registrarTiempoLectura();
  enrutador.push('/');
};

// Escuchar si el usuario cierra el navegador o la pestaña directamente
window.addEventListener('beforeunload', registrarTiempoLectura);

onBeforeUnmount(() => {
  registrarTiempoLectura();
  window.removeEventListener('beforeunload', registrarTiempoLectura);
});

// --- SISTEMA DE CALIFICACIONES INTERACTIVAS ---
const abrirModalResena = async () => {
  const { value: formValues } = await Swal.fire({
    title: '<span style="color:#1e293b; font-weight:900;">Califica esta edición</span>',
    html: `
      <div class="flex flex-col gap-4 text-left font-sans mt-2">
        <div>
          <label class="font-bold text-slate-500 text-xs uppercase tracking-wider block text-center mb-2">Puntuación:</label>
          <div class="star-rating-swal">
            <input type="radio" id="star5" name="swal-rating" value="5" checked />
            <label for="star5" title="Excelente">★</label>
            <input type="radio" id="star4" name="swal-rating" value="4" />
            <label for="star4" title="Muy buena">★</label>
            <input type="radio" id="star3" name="swal-rating" value="3" />
            <label for="star3" title="Buena">★</label>
            <input type="radio" id="star2" name="swal-rating" value="2" />
            <label for="star2" title="Regular">★</label>
            <input type="radio" id="star1" name="swal-rating" value="1" />
            <label for="star1" title="Mala">★</label>
          </div>
          <div id="star-text-value" class="text-[#7a1b2e] font-bold text-sm text-center mt-2">Excelente</div>
        </div>
        <div>
          <label class="font-bold text-slate-500 text-xs uppercase tracking-wider block mb-2">Comentario (Opcional):</label>
          <textarea id="swal-comentario" rows="3" placeholder="¿Qué te pareció el contenido de la revista?" class="w-full border border-slate-200 bg-slate-50 rounded-xl px-4 py-3 focus:border-[#7a1b2e] focus:ring-4 focus:ring-[#7a1b2e]/10 focus:outline-none transition font-medium text-slate-700 resize-none"></textarea>
        </div>
      </div>
    `,
    focusConfirm: false,
    showCancelButton: true,
    confirmButtonText: 'Enviar calificación',
    confirmButtonColor: '#7a1b2e', 
    cancelButtonColor: '#94a3b8',
    cancelButtonText: 'Cancelar',
    customClass: {
      popup: 'rounded-3xl shadow-2xl',
      confirmButton: 'font-bold rounded-xl px-6 py-3',
      cancelButton: 'font-bold rounded-xl px-6 py-3'
    },
    didOpen: () => {
      const radios = document.querySelectorAll('input[name="swal-rating"]');
      const textLabel = document.getElementById('star-text-value');
      const labels = ['Mala', 'Regular', 'Buena', 'Muy buena', 'Excelente'];

      radios.forEach(radio => {
        radio.addEventListener('change', (e) => {
          textLabel.textContent = labels[e.target.value - 1];
        });
      });
    },
    preConfirm: () => {
      const estrellaSeleccionada = document.querySelector('input[name="swal-rating"]:checked').value;
      const comentario = document.getElementById('swal-comentario').value;
      return { calificacion: parseInt(estrellaSeleccionada), comentario: comentario };
    }
  });

  if (formValues) {
    try {
      await api.post(`/revistas/${ruta.params.id}/resenas`, formValues);
      notificarExito('¡Gracias por tu reseña!');
    } catch (error) {
      console.error(error);
      notificarError('Hubo un error al guardar tu reseña. Verifica tu sesión.');
    }
  }
};

const pasarPaginaAnterior = () => { if (libro) libro.flipPrev(); };
const pasarPaginaSiguiente = () => { if (libro) libro.flipNext(); };

// --- RENDERIZADO Y CONSTRUCCIÓN EN 3D ---
onMounted(async () => {
  const idRevista = ruta.params.id;
  tiempoInicioLectura = Date.now();

  try {
    // CORRECCIÓN: Registro de visitas silencioso en segundo plano
    setTimeout(() => {
      api.post(`/revistas/${idRevista}/vista`).catch(e => console.error("Error al registrar vista", e));
    }, 1000);

    const respuesta = await api.get(`/revistas/${idRevista}`);
    revista.value = respuesta.data;
    mensajeCarga.value = 'Descargando documento PDF...';

    const loadingTask = pdfjsLib.getDocument('http://localhost:8000' + revista.value.ruta_pdf);
    const pdf = await loadingTask.promise;

    const primeraPagina = await pdf.getPage(1);
    const viewportBase = primeraPagina.getViewport({ scale: 1.5 });

    const anchoDisponible = window.innerWidth - 140; 
    const altoDisponible = window.innerHeight - 120; 
    const proporcionLibroAbierto = (viewportBase.width * 2) / viewportBase.height;
    
    let altoCalculado = anchoDisponible / proporcionLibroAbierto;
    let anchoCalculado = anchoDisponible;
    
    if (altoCalculado > altoDisponible) {
      altoCalculado = altoDisponible;
      anchoCalculado = altoCalculado * proporcionLibroAbierto;
    }
    
    alturaContenedor.value = Math.round(altoCalculado) + 'px';
    anchoContenedor.value = Math.round(anchoCalculado) + 'px';

    const flipbookContainer = document.getElementById('flipbook-container');
    flipbookContainer.innerHTML = ''; 

    for (let i = 1; i <= pdf.numPages; i++) {
      mensajeCarga.value = `Renderizando página ${i} de ${pdf.numPages}...`;
      
      const pageDiv = document.createElement('div');
      pageDiv.className = 'page bg-white overflow-hidden shadow-[inset_0_0_20px_rgba(0,0,0,0.05)]'; 
      
      const canvas = document.createElement('canvas');
      pageDiv.appendChild(canvas);
      flipbookContainer.appendChild(pageDiv);

      const pagina = await pdf.getPage(i);
      const viewport = pagina.getViewport({ scale: 1.5 });
      
      canvas.width = viewport.width;
      canvas.height = viewport.height;
      canvas.style.width = '100%';
      canvas.style.height = '100%';
      
      await pagina.render({ canvasContext: canvas.getContext('2d'), viewport: viewport }).promise;
    }

    if (pdf.numPages === 1) {
      const blankPage = document.createElement('div');
      blankPage.className = 'page bg-slate-50 overflow-hidden flex items-center justify-center border-l border-slate-200 shadow-[inset_0_0_20px_rgba(0,0,0,0.02)]';
      blankPage.innerHTML = '<span class="text-slate-300 font-black tracking-widest uppercase text-xl">Fin de Edición</span>';
      flipbookContainer.appendChild(blankPage);
    }

    mensajeCarga.value = 'Ensamblando revista...';

    libro = new PageFlip(flipbookContainer, {
      width: viewportBase.width,
      height: viewportBase.height,
      size: "stretch",      
      minWidth: 300,        
      maxWidth: 2000,
      minHeight: 400,
      maxHeight: 2000,
      showCover: true,
      autoCenter: true,
      maxShadowOpacity: 0.5,
      drawShadow: true,
      flippingTime: 800,
      usePortrait: true
    });

    libro.loadFromHTML(flipbookContainer.querySelectorAll('.page'));

    totalPaginas.value = pdf.numPages;
    actualizarEstadoBotones();

    libro.on('flip', (e) => {
      paginaActual.value = e.data + 1;
      actualizarEstadoBotones();
    });

    await new Promise(resolve => setTimeout(resolve, 300));
    cargando.value = false;

  } catch (error) {
    console.error("Error detallado:", error);
    mensajeCarga.value = 'Error técnico: ' + error.message;
  }
});

const actualizarEstadoBotones = () => {
  if (libro) {
    puedeRetroceder.value = paginaActual.value > 1;
    puedeAvanzar.value = paginaActual.value < totalPaginas.value;
  }
};
</script>

<style scoped>
.page {
  background-color: white;
  border-right: solid 1px rgba(0, 0, 0, 0.1);
  border-left: solid 1px rgba(0, 0, 0, 0.05);
}

.pb-safe {
  padding-bottom: env(safe-area-inset-bottom, 12px);
}

:global(.star-rating-swal) {
  display: flex;
  flex-direction: row-reverse; 
  justify-content: center;
  gap: 0.25rem;
}
:global(.star-rating-swal input) {
  display: none; 
}
:global(.star-rating-swal label) {
  font-size: 2.5rem; 
  color: #cbd5e1; 
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  line-height: 1;
}
:global(.star-rating-swal label:hover),
:global(.star-rating-swal label:hover ~ label),
:global(.star-rating-swal input:checked ~ label) {
  color: #facc15; 
  text-shadow: 0 0 15px rgba(250, 204, 21, 0.4); 
  transform: scale(1.1); 
}
</style>