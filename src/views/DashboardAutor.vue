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
            {{ nombreAutor.charAt(0).toUpperCase() }}
          </div>
          <div>
            <div class="flex items-center gap-3 mb-1">
              <h1 class="text-3xl font-black text-white tracking-tight drop-shadow-md">
                {{ nombreAutor }}
              </h1>
              <span class="bg-white/10 backdrop-blur-md text-white text-[10px] font-black px-3 py-1.5 rounded-lg uppercase tracking-widest border border-white/20 shadow-sm">
                Autor
              </span>
            </div>
            <p class="text-sm text-slate-300 font-medium">
              Facultad de Ciencias Sociales • Panel de Gestión
            </p>
          </div>
        </div>
        
        <div class="flex bg-slate-800/50 p-1.5 rounded-2xl backdrop-blur-md border border-white/10 shadow-lg">
          <button 
            @click="pestanaActual = 'resumen'" 
            :class="pestanaActual === 'resumen' ? 'bg-white text-slate-900 shadow-md' : 'text-slate-300 hover:text-white hover:bg-white/10'"
            class="px-6 py-2.5 rounded-xl transition-all duration-300 text-sm font-bold flex items-center gap-2"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" /></svg>
            Resumen
          </button>
          <button 
            @click="pestanaActual = 'publicar'" 
            :class="pestanaActual === 'publicar' ? 'bg-[#7a1b2e] text-white shadow-md border border-[#7a1b2e]/50' : 'text-slate-300 hover:text-white hover:bg-white/10'"
            class="px-6 py-2.5 rounded-xl transition-all duration-300 text-sm font-bold flex items-center gap-2"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" /></svg>
            Nueva Publicación
          </button>
        </div>
      </div>
    </div>

    <div class="max-w-[1400px] mx-auto px-4 md:px-8 -mt-8 relative z-20 space-y-8">
      
      <div v-if="pestanaActual === 'resumen'" class="space-y-8 animate-fade-in">
        
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <div class="bg-white p-6 rounded-[1.5rem] shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-100 flex justify-between items-start hover:-translate-y-1 transition duration-300">
            <div>
              <p class="text-sm text-slate-500 font-medium mb-1">Publicaciones</p>
              <h3 class="text-3xl font-black text-slate-800">{{ misRevistas.length }}</h3>
              <p class="text-xs text-slate-400 font-bold mt-2">Documentos subidos</p>
            </div>
            <div class="w-14 h-14 rounded-2xl bg-slate-900 flex items-center justify-center text-white shadow-lg shadow-slate-900/20">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
            </div>
          </div>
          
          <div class="bg-white p-6 rounded-[1.5rem] shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-100 flex justify-between items-start hover:-translate-y-1 transition duration-300">
            <div>
              <p class="text-sm text-slate-500 font-medium mb-1">Vistas Activas</p>
              <h3 class="text-3xl font-black text-slate-800">{{ estadisticasGlobales.vistas }}</h3>
              <p class="text-xs text-[#7a1b2e] font-bold mt-2">Lectores únicos</p>
            </div>
            <div class="w-14 h-14 rounded-2xl bg-[#7a1b2e] flex items-center justify-center text-white shadow-lg shadow-[#7a1b2e]/30">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
            </div>
          </div>

          <div class="bg-white p-6 rounded-[1.5rem] shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-100 flex justify-between items-start hover:-translate-y-1 transition duration-300">
            <div>
              <p class="text-sm text-slate-500 font-medium mb-1">Tiempo Retenido</p>
              <h3 class="text-3xl font-black text-slate-800">{{ formatearTiempo(estadisticasGlobales.tiempo) }}</h3>
              <p class="text-xs text-slate-400 font-bold mt-2">Impacto generado</p>
            </div>
            <div class="w-14 h-14 rounded-2xl bg-slate-700 flex items-center justify-center text-white shadow-lg shadow-slate-700/20">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            </div>
          </div>

          <div class="bg-white p-6 rounded-[1.5rem] shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-100 flex justify-between items-start hover:-translate-y-1 transition duration-300">
            <div>
              <p class="text-sm text-slate-500 font-medium mb-1">Puntuación</p>
              <h3 class="text-3xl font-black text-slate-800">{{ estadisticasGlobales.estrellas }}</h3>
              <p class="text-xs text-amber-500 font-bold mt-2">Promedio general</p>
            </div>
            <div class="w-14 h-14 rounded-2xl bg-amber-500 flex items-center justify-center text-white shadow-lg shadow-amber-500/30">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" /></svg>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-[2rem] shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-100 overflow-hidden">
          <div class="px-8 py-6 flex justify-between items-center bg-slate-50/50">
            <div>
              <h3 class="text-xl font-black text-slate-800">Monitoreo de Revistas</h3>
              <p class="text-sm text-slate-500 mt-1">Revisa el estado y rendimiento de tus publicaciones.</p>
            </div>
            <button @click="cargarMisRevistas" class="text-slate-600 bg-white hover:bg-slate-50 px-4 py-2.5 rounded-xl text-sm font-bold transition flex items-center gap-2 border border-slate-200 shadow-sm">
              <span :class="{'animate-spin': cargando}">🔄</span> Actualizar
            </button>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full text-left border-t border-slate-100">
              <thead class="text-slate-400 text-xs font-bold bg-white">
                <tr>
                  <th class="px-8 py-4 font-bold uppercase tracking-wider">Documento y Categoría</th>
                  <th class="px-8 py-4 font-bold uppercase tracking-wider">Estado Actual</th>
                  <th class="px-8 py-4 font-bold uppercase tracking-wider">Eficiencia (Vistas / Tiempo)</th>
                  <th class="px-8 py-4 font-bold uppercase tracking-wider">Acción</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100 text-sm bg-white">
                
                <tr v-if="misRevistas.length === 0">
                  <td colspan="4" class="px-8 py-20 text-center">
                    <div class="w-20 h-20 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-4 border border-slate-100">
                      <span class="text-3xl text-slate-300">📂</span>
                    </div>
                    <h4 class="text-lg font-black text-slate-800">No hay datos para mostrar</h4>
                    <p class="text-slate-500 mt-1">Sube tu primera investigación para ver estadísticas.</p>
                  </td>
                </tr>

                <tr v-for="revista in misRevistas" :key="revista.id" class="hover:bg-slate-50/50 transition duration-200 group">
                  <td class="px-8 py-5">
                    <div class="font-black text-slate-800 text-base mb-1">{{ revista.titulo }}</div>
                    <div class="flex items-center gap-2 text-xs text-slate-500 font-medium">
                      <span class="bg-slate-100 px-2 py-0.5 rounded text-slate-600">{{ revista.categoria }}</span>
                      <span>•</span>
                      <span>{{ new Date(revista.fecha_creacion).toLocaleDateString() }}</span>
                    </div>
                  </td>
                  
                  <td class="px-8 py-5">
                    <span :class="{
                      'bg-amber-50 text-amber-700 border-amber-200': revista.estado === 'PENDIENTE',
                      'bg-emerald-50 text-emerald-700 border-emerald-200': revista.estado === 'APROBADA',
                      'bg-rose-50 text-rose-700 border-rose-200': revista.estado === 'RECHAZADA'
                    }" class="px-3 py-1.5 rounded-lg text-xs font-bold tracking-wide flex inline-flex items-center gap-1.5 border">
                      <span :class="{
                        'bg-amber-500': revista.estado === 'PENDIENTE',
                        'bg-emerald-500': revista.estado === 'APROBADA',
                        'bg-rose-500': revista.estado === 'RECHAZADA'
                      }" class="w-1.5 h-1.5 rounded-full animate-pulse"></span>
                      {{ revista.estado === 'PENDIENTE' ? 'En Revisión' : revista.estado }}
                    </span>
                  </td>

                  <td class="px-8 py-5">
                    <div v-if="revista.estado === 'APROBADA'" class="flex gap-4 text-sm font-bold text-slate-700">
                      <div class="flex flex-col gap-1" title="Vistas Totales">
                        <span class="text-[10px] uppercase tracking-wide text-slate-400">Vistas</span>
                        <span class="text-slate-700 font-semibold">{{ revista.vistas || 0 }}</span>
                      </div>
                      <div class="flex flex-col gap-1" title="Tiempo Leído">
                        <span class="text-[10px] uppercase tracking-wide text-slate-400">Tiempo</span>
                        <span class="text-slate-700 font-semibold">{{ formatearTiempo(revista.tiempo_lectura_total_segundos) }}</span>
                      </div>
                      <div class="flex flex-col gap-1" title="Promedio de Reseñas">
                        <span class="text-[10px] uppercase tracking-wide text-slate-400">Promedio</span>
                        <span class="text-slate-700 font-semibold">{{ calcularEstrellasCorto(revista.resenas) }}</span>
                      </div>
                    </div>
                    <div v-else class="text-xs text-slate-400 font-medium bg-slate-50 px-3 py-1.5 rounded-md inline-block">
                      Esperando aprobación...
                    </div>
                  </td>

                  <td class="px-8 py-5">
                    
                    <div v-if="revista.estado === 'APROBADA'" class="flex flex-wrap gap-2">
                      <router-link :to="'/revista/' + revista.id" class="text-white bg-slate-900 hover:bg-[#7a1b2e] px-4 py-2.5 rounded-xl text-xs font-bold transition flex items-center gap-2 shadow-sm">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                        Leer
                      </router-link>

                      <button @click="verComentarios(revista)" class="text-amber-700 bg-amber-50 hover:bg-amber-500 hover:text-white border border-amber-200 hover:border-amber-500 px-4 py-2.5 rounded-xl text-xs font-bold transition flex items-center gap-2 shadow-sm">
                        💬 Comentarios
                      </button>
                    </div>

                    <div v-else-if="revista.revisiones && revista.revisiones.length > 0" class="text-xs text-slate-600 bg-rose-50 p-2.5 rounded-lg max-w-[200px] border border-rose-100 line-clamp-2" :title="revista.revisiones[0].observaciones">
                      <span class="font-bold text-rose-600">Nota:</span> {{ revista.revisiones[0].observaciones }}
                    </div>
                    
                    <span v-else class="text-slate-300 text-xs">-</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div v-if="pestanaActual === 'publicar'" class="animate-fade-in max-w-4xl mx-auto">
        <div class="bg-white p-8 md:p-12 rounded-[2rem] shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-100">
          
          <div class="mb-8 border-b border-slate-100 pb-6">
            <h2 class="text-2xl font-black text-slate-800">Publicar Nueva Edición</h2>
            <p class="text-slate-500 text-sm mt-1">Completa los datos de tu investigación y sube el documento PDF para revisión.</p>
          </div>

          <form @submit.prevent="publicarRevista" class="space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              
              <div class="col-span-2">
                <label class="block text-[11px] font-black text-slate-400 uppercase tracking-widest mb-2 ml-1">Título de la Revista</label>
                <input v-model="titulo" type="text" required class="w-full px-5 py-3.5 bg-slate-50 border border-slate-200 rounded-2xl focus:bg-white focus:border-[#7a1b2e] focus:ring-4 focus:ring-[#7a1b2e]/10 outline-none transition-all font-bold text-slate-800 placeholder-slate-300" placeholder="Ej. El impacto de las políticas públicas en Bolivia">
              </div>

              <div class="col-span-2">
                <label class="block text-[11px] font-black text-slate-400 uppercase tracking-widest mb-2 ml-1">Resumen Corto</label>
                <textarea v-model="descripcion" required rows="3" class="w-full px-5 py-3.5 bg-slate-50 border border-slate-200 rounded-2xl focus:bg-white focus:border-[#7a1b2e] focus:ring-4 focus:ring-[#7a1b2e]/10 outline-none transition-all font-medium text-slate-800 resize-none placeholder-slate-300" placeholder="Describe brevemente de qué trata..."></textarea>
              </div>

              <div class="col-span-2 md:col-span-1">
                <label class="block text-[11px] font-black text-slate-400 uppercase tracking-widest mb-2 ml-1">Categoría</label>
                <select v-model="categoria" required class="w-full px-5 py-3.5 bg-slate-50 border border-slate-200 rounded-2xl focus:bg-white focus:border-[#7a1b2e] focus:ring-4 focus:ring-[#7a1b2e]/10 outline-none transition-all font-bold text-slate-700 cursor-pointer appearance-none">
                  <option v-for="cat in categorias" :key="cat.id" :value="cat.nombre">{{ cat.nombre }}</option>
                </select>
              </div>
            </div>

            <div class="mt-8">
              <label class="block text-[11px] font-black text-slate-400 uppercase tracking-widest mb-2 ml-1">Documento Original</label>
              <div class="bg-slate-50 hover:bg-slate-100 p-8 rounded-3xl border-2 border-dashed border-slate-200 hover:border-[#7a1b2e]/50 text-center transition-colors duration-300 relative cursor-pointer group">
                <input @change="cargarPDF" type="file" accept=".pdf" required class="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10">
                <div class="w-16 h-16 bg-white rounded-2xl shadow-sm flex items-center justify-center mx-auto mb-4 group-hover:-translate-y-2 transition-transform duration-300 border border-slate-100">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" /></svg>
                </div>
                <h4 class="text-sm font-bold text-slate-700 mb-1">Arrastra tu PDF aquí o haz clic para buscar</h4>
                <p class="text-xs text-slate-400 font-medium">Solo archivos .pdf</p>
                
                <div v-if="archivoPdf" class="mt-4 inline-flex items-center gap-2 bg-[#7a1b2e]/10 text-[#7a1b2e] px-4 py-2 rounded-xl text-xs font-bold border border-[#7a1b2e]/20">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 3H7a2 2 0 01-2-2V5a2 2 0 012-2h7l5 5v11a2 2 0 01-2 2z"/></svg>
                  {{ archivoPdf.name }}
                </div>
              </div>
            </div>

            <div v-show="pdfCargado" class="bg-white border border-slate-200 p-6 rounded-[2rem] flex flex-col md:flex-row items-center gap-8 mt-6">
              <div class="flex-1 text-center md:text-left">
                <h3 class="text-sm font-bold text-slate-800 mb-2">Selecciona la Portada</h3>
                <p class="text-xs text-slate-500 font-medium mb-4">Usa las flechas para navegar por el documento y elegir la página que servirá de imagen miniatura.</p>
                
                <div class="flex items-center justify-center md:justify-start gap-4 mb-4">
                  <button type="button" @click="cambiarPagina(-1)" :disabled="paginaActual <= 1" class="p-2 bg-slate-50 text-slate-600 disabled:text-slate-300 hover:bg-slate-200 rounded-lg transition font-bold border border-slate-200">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" /></svg>
                  </button>
                  <span class="text-sm font-black text-slate-700">{{ paginaActual }} / {{ totalPaginas }}</span>
                  <button type="button" @click="cambiarPagina(1)" :disabled="paginaActual >= totalPaginas" class="p-2 bg-slate-50 text-slate-600 disabled:text-slate-300 hover:bg-slate-200 rounded-lg transition font-bold border border-slate-200">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" /></svg>
                  </button>
                </div>
              </div>

              <div class="w-32 md:w-40 p-2 bg-slate-50 rounded-2xl shadow-inner border border-slate-100 flex-shrink-0">
                <canvas ref="canvasPortada" class="w-full h-auto rounded-xl shadow-md border border-slate-200"></canvas>
              </div>
            </div>

            <div class="pt-6">
              <div v-if="mensaje" :class="exito ? 'bg-emerald-50 text-emerald-700 border-emerald-200' : 'bg-[#7a1b2e]/10 text-[#7a1b2e] border-[#7a1b2e]/20'" class="p-4 rounded-xl border text-sm font-bold text-center mb-6">
                {{ mensaje }}
              </div>

              <button type="submit" :disabled="cargando || !pdfCargado" class="w-full bg-slate-900 text-white font-bold text-sm py-4 rounded-2xl hover:bg-[#7a1b2e] hover:shadow-lg hover:shadow-[#7a1b2e]/30 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2">
                <span v-if="cargando" class="flex items-center gap-2">
                  <div class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  Procesando documento...
                </span>
                <span v-else>Publicar Documento</span>
              </button>
            </div>
          </form>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, shallowRef, onMounted, computed } from 'vue';
import api from '../services/api';
import Swal from 'sweetalert2';
import * as pdfjsLib from 'pdfjs-dist';
import pdfWorker from 'pdfjs-dist/build/pdf.worker.mjs?url';

pdfjsLib.GlobalWorkerOptions.workerSrc = pdfWorker;

// ESTADO DE LA INTERFAZ
const pestanaActual = ref('resumen');
const misRevistas = ref([]);
const nombreAutor = ref('Cargando...'); 

// NUEVO: Arreglo de Categorías de la Base de Datos
const categorias = ref([]);

// Variables del Formulario
const titulo = ref('');
const descripcion = ref('');
const categoria = ref(''); // Ahora comienza vacío
const archivoPdf = ref(null);
const cargando = ref(false);
const mensaje = ref('');
const exito = ref(false);

// Variables del PDF
const pdfCargado = shallowRef(null);
const paginaActual = ref(1);
const totalPaginas = ref(0);
const canvasPortada = ref(null);

// ESTADÍSTICAS GLOBALES
const estadisticasGlobales = computed(() => {
  let vistas = 0;
  let tiempo = 0;
  let sumaEstrellas = 0;
  let totalResenas = 0;

  misRevistas.value.forEach(revista => {
    vistas += (revista.vistas || 0);
    tiempo += (revista.tiempo_lectura_total_segundos || 0);
    if (revista.resenas && revista.resenas.length > 0) {
      revista.resenas.forEach(r => {
        sumaEstrellas += r.calificacion;
        totalResenas++;
      });
    }
  });

  const promedio = totalResenas > 0 ? (sumaEstrellas / totalResenas).toFixed(1) : '0.0';
  return { vistas, tiempo, estrellas: promedio };
});

const formatearTiempo = (segundos) => {
  if (!segundos) return '0m';
  const minutos = Math.floor(segundos / 60);
  if (minutos < 60) return `${minutos}m`;
  const horas = Math.floor(minutos / 60);
  const minsRestantes = minutos % 60;
  return `${horas}h ${minsRestantes}m`;
};

const calcularEstrellasCorto = (resenas) => {
  if (!resenas || resenas.length === 0) return '-';
  const suma = resenas.reduce((acc, r) => acc + r.calificacion, 0);
  return (suma / resenas.length).toFixed(1);
};

const cargarPDF = async (evento) => {
  const archivo = evento.target.files[0];
  if (!archivo) return;
  archivoPdf.value = archivo;
  mensaje.value = '';
  exito.value = false;

  try {
    const arrayBuffer = await archivo.arrayBuffer();
    const loadingTask = pdfjsLib.getDocument({ data: arrayBuffer });
    pdfCargado.value = await loadingTask.promise;
    totalPaginas.value = pdfCargado.value.numPages;
    paginaActual.value = 1; 
    renderizarPagina(paginaActual.value);
  } catch (error) {
    console.error(error);
    mensaje.value = "El archivo PDF no se puede leer.";
  }
};

const cambiarPagina = (delta) => {
  const nuevaPagina = paginaActual.value + delta;
  if (nuevaPagina >= 1 && nuevaPagina <= totalPaginas.value) {
    paginaActual.value = nuevaPagina;
    renderizarPagina(nuevaPagina);
  }
};

const renderizarPagina = async (numPagina) => {
  if (!pdfCargado.value) return;
  const pagina = await pdfCargado.value.getPage(numPagina);
  const viewport = pagina.getViewport({ scale: 1.0 }); 
  const canvas = canvasPortada.value;
  const contexto = canvas.getContext('2d');
  canvas.height = viewport.height;
  canvas.width = viewport.width;
  await pagina.render({ canvasContext: contexto, viewport: viewport }).promise;
};

const obtenerImagenDelCanvas = () => {
  return new Promise((resolve) => {
    canvasPortada.value.toBlob((blob) => resolve(new File([blob], "portada.jpg", { type: "image/jpeg" })), 'image/jpeg', 0.85); 
  });
};

const cargarPerfilReal = async () => {
  try {
    const res = await api.get('/auth/me');
    nombreAutor.value = res.data.nombre; 
  } catch (error) {
    nombreAutor.value = localStorage.getItem('usuario_correo')?.split('@')[0] || 'Autor Institucional';
  }
};

const cargarMisRevistas = async () => {
  cargando.value = true;
  try {
    const respuesta = await api.get('/revistas/mis-revistas');
    misRevistas.value = respuesta.data;
  } catch (error) {
    console.error("Error al cargar historial:", error);
  } finally {
    cargando.value = false;
  }
};

const cargarCategorias = async () => {
  try {
    const res = await api.get('/categorias/');
    categorias.value = res.data;
    if (categorias.value.length > 0) {
      categoria.value = categorias.value[0].nombre; // Auto-selecciona la primera
    }
  } catch (error) {
    console.error("Error al cargar categorías", error);
  }
};

const verComentarios = async (revista) => {
  try {
    Swal.fire({
      title: 'Buscando comentarios...',
      allowOutsideClick: false,
      didOpen: () => Swal.showLoading()
    });

    const res = await api.get(`/revistas/${revista.id}/resenas`);
    const resenas = res.data;

    if (resenas.length === 0) {
      Swal.fire({
        title: 'Sin reseñas aún',
        text: 'Esta publicación todavía no ha recibido comentarios.',
        icon: 'info',
        confirmButtonColor: '#7a1b2e',
        customClass: { popup: 'rounded-3xl font-sans', confirmButton: 'rounded-xl px-6 py-2' }
      });
      return;
    }

    let htmlContent = '<div class="space-y-4 max-h-[400px] overflow-y-auto text-left font-sans mt-4 pr-2">';
    
    resenas.forEach(r => {
      const calificacionTexto = `${r.calificacion}/5`;
      const nombreUsuario = r.usuario_correo.split('@')[0];
      const mensajeComentario = r.comentario ? `"${r.comentario}"` : '<span class="text-slate-400">Solo dejó calificación.</span>';
      
      htmlContent += `
        <div class="p-4 bg-slate-50 border border-slate-100 rounded-2xl shadow-sm">
          <div class="flex justify-between items-start mb-2 border-b border-slate-200 pb-2">
            <span class="font-black text-slate-800 text-sm">@${nombreUsuario}</span>
            <span class="text-slate-600 text-xs tracking-widest">${calificacionTexto}</span>
          </div>
          <p class="text-slate-600 text-sm font-medium italic">${mensajeComentario}</p>
          <p class="text-[10px] text-slate-400 mt-3 text-right font-bold uppercase tracking-wider">${new Date(r.fecha).toLocaleDateString()}</p>
        </div>
      `;
    });
    
    htmlContent += '</div>';

    Swal.fire({
      title: `<span style="color:#1e293b; font-weight:900;">Comentarios de la comunidad</span>`,
      html: htmlContent,
      showConfirmButton: true,
      confirmButtonText: 'Cerrar',
      confirmButtonColor: '#7a1b2e',
      customClass: {
        popup: 'rounded-[2rem] shadow-2xl font-sans',
        confirmButton: 'font-bold rounded-xl px-8 py-3 w-full',
      }
    });

  } catch (error) {
    Swal.fire({
      title: 'Error',
      text: 'No se pudieron cargar los comentarios.',
      icon: 'error',
      confirmButtonColor: '#7a1b2e'
    });
  }
};

onMounted(() => {
  cargarCategorias(); // Agregado aquí
  cargarMisRevistas();
  cargarPerfilReal();
});

const publicarRevista = async () => {
  cargando.value = true;
  exito.value = false;
  try {
    mensaje.value = 'Procesando imágenes y archivos...';
    const archivoPortada = await obtenerImagenDelCanvas();
    const formData = new FormData();
    formData.append('archivo_pdf', archivoPdf.value);
    formData.append('archivo_portada', archivoPortada);

    const resArchivos = await api.post('/subir/revista/', formData, { headers: { 'Content-Type': 'multipart/form-data' } });

    mensaje.value = 'Enviando publicación al decanato...';
    await api.post('/revistas/', {
      titulo: titulo.value,
      descripcion: descripcion.value,
      categoria: categoria.value,
      ruta_portada: resArchivos.data.ruta_portada,
      ruta_pdf: resArchivos.data.ruta_pdf
    });

    exito.value = true;
    mensaje.value = '¡Publicación enviada a revisión con éxito!';
    titulo.value = ''; descripcion.value = '';
    
    setTimeout(() => {
      cargarMisRevistas();
      pestanaActual.value = 'resumen';
      mensaje.value = '';
    }, 2500);

  } catch (error) {
    exito.value = false;
    mensaje.value = 'Error al subir. Intenta de nuevo.';
  } finally {
    cargando.value = false;
  }
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

::-webkit-scrollbar {
  width: 6px;
}
::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 10px;
}
::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>