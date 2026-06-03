<template>
  <div class="min-h-screen flex flex-col font-sans">
    
    <header class="bg-azul-marino text-white shadow-lg relative z-50">
      <div class="container mx-auto px-4 py-3 flex justify-between items-center">
        
        <div class="flex items-center space-x-3">
  <span class="text-xl font-black tracking-wide bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-300">
    Revista Digital UMSA
  </span>
</div>
        
        <nav class="flex items-center space-x-1 md:space-x-2">
          
          <router-link 
            to="/" 
            class="px-4 py-2 rounded-xl text-sm font-medium transition-all duration-300 text-slate-300 hover:text-white hover:bg-white/10"
            active-class="bg-red-900 text-white font-bold shadow-md"
          >
            Inicio
          </router-link>
          
          <router-link 
            v-if="!estaLogueado" 
            to="/login" 
            class="px-4 py-2 rounded-xl text-sm font-medium transition-all duration-300 text-slate-300 hover:text-white hover:bg-white/10"
            active-class="bg-blue-600 text-white font-bold shadow-md"
          >
            Iniciar Sesión
          </router-link>

          <template v-else>
            
            <router-link 
              to="/dashboard" 
              class="px-4 py-2 rounded-xl text-sm font-medium transition-all duration-300 text-slate-300 hover:text-white hover:bg-white/10"
              active-class="bg-red-900 text-white font-bold shadow-md"
            >
              Mi Panel
            </router-link>

            <router-link 
              v-if="rolUsuario === 'ADMINISTRADOR' || rolUsuario === 'MODERADOR'" 
              to="/moderacion" 
              class="px-4 py-2 rounded-xl text-sm font-medium transition-all duration-300 text-slate-300 hover:text-white hover:bg-white/10"
              active-class="bg-red-900 text-white font-bold shadow-md"
            >
              Moderación
            </router-link>

            <router-link 
              v-if="rolUsuario === 'ADMINISTRADOR'" 
              to="/admin" 
              class="px-4 py-2 rounded-xl text-sm font-medium transition-all duration-300 text-slate-300 hover:text-white hover:bg-white/10"
              active-class="bg-red-900 text-white font-bold shadow-md"
            >
              Administración
            </router-link>

            <div class="h-6 w-px bg-slate-600 mx-2 opacity-50"></div>
            
            <button 
              @click="cerrarSesion" 
              class="px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 transition-all duration-300"
              title="Cerrar Sesión"
            >
              Salir
            </button>
          </template>

        </nav>
      </div>
    </header>

    <main class="flex-grow flex flex-col">
      <router-view />
    </main>

    <footer class="bg-white border-t border-slate-200 text-slate-500 text-center py-3 mt-auto">
  <p class="text-xs font-medium">&copy; 2026 Facultad de Ciencias Sociales</p>
</footer>

  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';

const enrutador = useRouter();
const rutaActual = useRoute();

const estaLogueado = ref(false);
const rolUsuario = ref('');

// Verificar sesión reactivamente
watch(
  () => rutaActual.path,
  () => {
    estaLogueado.value = !!localStorage.getItem('token_acceso');
    rolUsuario.value = localStorage.getItem('rol_usuario');
  },
  { immediate: true }
);

const cerrarSesion = () => {
  localStorage.removeItem('token_acceso');
  localStorage.removeItem('rol_usuario');
  localStorage.removeItem('usuario_correo');
  estaLogueado.value = false;
  rolUsuario.value = '';
  enrutador.push('/login');
};
</script>

<style>
/* Opcional: Asegurarnos de que el fondo general sea el que definimos en los componentes */
body {
  background-color: #f8fafc; /* slate-50 */
}
</style>