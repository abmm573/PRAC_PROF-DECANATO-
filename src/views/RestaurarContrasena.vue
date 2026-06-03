<template>
  <div class="min-h-screen bg-slate-50 flex flex-col font-sans">
    
    <header class="bg-slate-900 border-b border-white/10 px-6 py-4 flex justify-between items-center relative overflow-hidden">
      <div class="absolute inset-0 z-0">
        <div class="absolute -top-24 -left-24 w-96 h-96 bg-[#7a1b2e]/20 rounded-full blur-3xl"></div>
      </div>
      <div class="relative z-10 flex items-center gap-3">
        <div class="w-10 h-10 bg-white rounded-xl flex items-center justify-center font-black text-[#7a1b2e] text-xl shadow-lg">
          R
        </div>
        <div>
          <h1 class="text-white font-black text-xl tracking-tight leading-none">Revista Digital</h1>
          <span class="text-slate-400 text-xs font-bold uppercase tracking-widest">UMSA</span>
        </div>
      </div>
      <router-link to="/login" class="relative z-10 text-white text-sm font-bold hover:text-[#7a1b2e] transition">
        Volver al Login
      </router-link>
    </header>

    <main class="flex-grow flex items-center justify-center p-4 relative">
      <div class="w-full max-w-md bg-white rounded-[2rem] shadow-[0_20px_50px_-12px_rgba(0,0,0,0.1)] border border-slate-100 p-8 md:p-10 relative z-10 overflow-hidden">
        
        <div class="text-center mb-8">
          <div class="w-16 h-16 bg-[#7a1b2e]/10 rounded-2xl flex items-center justify-center mx-auto mb-4 border border-[#7a1b2e]/20">
            <span class="text-3xl">🔐</span>
          </div>
          <h2 class="text-2xl font-black text-slate-800 tracking-tight">Crea tu nueva contraseña</h2>
          <p class="text-sm text-slate-500 font-medium mt-2">Ingresa una contraseña segura que puedas recordar fácilmente.</p>
        </div>

        <form @submit.prevent="restaurarContrasena" class="space-y-5">
          
          <div>
            <label class="block text-[11px] font-black text-slate-400 uppercase tracking-widest mb-1.5 ml-1">Nueva Contraseña</label>
            <input 
              v-model="nuevaContrasena" 
              type="password" 
              required 
              minlength="6"
              class="w-full px-5 py-3.5 bg-slate-50 border border-slate-200 rounded-2xl focus:bg-white focus:border-[#7a1b2e] focus:ring-4 focus:ring-[#7a1b2e]/10 outline-none transition-all font-medium text-slate-800" 
              placeholder="••••••••"
            >
          </div>

          <div>
            <label class="block text-[11px] font-black text-slate-400 uppercase tracking-widest mb-1.5 ml-1">Confirmar Contraseña</label>
            <input 
              v-model="confirmarContrasena" 
              type="password" 
              required 
              class="w-full px-5 py-3.5 bg-slate-50 border border-slate-200 rounded-2xl focus:bg-white focus:border-[#7a1b2e] focus:ring-4 focus:ring-[#7a1b2e]/10 outline-none transition-all font-medium text-slate-800" 
              placeholder="••••••••"
            >
          </div>

          <button 
            type="submit" 
            :disabled="cargando" 
            class="w-full bg-[#7a1b2e] text-white font-bold py-4 rounded-2xl hover:bg-[#5a1422] transition-all duration-300 shadow-lg hover:shadow-[#7a1b2e]/40 disabled:opacity-50 mt-4"
          >
            {{ cargando ? 'Guardando...' : 'Restablecer Contraseña' }}
          </button>
        </form>

      </div>
    </main>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../services/api';
import Swal from 'sweetalert2';
import { notificarError } from '../services/alertas';

const route = useRoute();
const router = useRouter();

const nuevaContrasena = ref('');
const confirmarContrasena = ref('');
const cargando = ref(false);
const token = ref('');

// Capturamos el token de la URL apenas carga la página
onMounted(() => {
  token.value = route.query.token;
  if (!token.value) {
    Swal.fire({
      title: 'Enlace inválido',
      text: 'No se encontró el código de seguridad en el enlace.',
      icon: 'error',
      confirmButtonColor: '#7a1b2e'
    }).then(() => {
      router.push('/login');
    });
  }
});

const restaurarContrasena = async () => {
  if (nuevaContrasena.value !== confirmarContrasena.value) {
    notificarError('Las contraseñas no coinciden. Intenta de nuevo.');
    return;
  }

  cargando.value = true;
  try {
    const respuesta = await api.post('/auth/restablecer-contrasena', {
      token: token.value,
      nueva_contrasena: nuevaContrasena.value
    });

    Swal.fire({
      title: '<span style="color:#1e293b; font-weight:900;">¡Éxito!</span>',
      html: `<p style="color:#64748b;">${respuesta.data.mensaje}</p>`,
      icon: 'success',
      confirmButtonColor: '#7a1b2e',
      customClass: { popup: 'rounded-3xl font-sans', confirmButton: 'font-bold rounded-xl px-6 py-3' }
    }).then(() => {
      router.push('/login');
    });

  } catch (error) {
    Swal.fire({
      title: 'Enlace caducado',
      text: error.response?.data?.detail || 'El enlace de recuperación es inválido o ha caducado.',
      icon: 'error',
      confirmButtonColor: '#7a1b2e',
      customClass: { popup: 'rounded-3xl font-sans', confirmButton: 'font-bold rounded-xl px-6 py-3' }
    });
  } finally {
    cargando.value = false;
  }
};
</script>
