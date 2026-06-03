<template>
  <div class="relative flex-1 w-full flex items-center justify-center p-4 overflow-hidden font-sans">
    
    <div class="absolute inset-0 z-0">
      <img src="https://images.unsplash.com/photo-1541339907198-e08759df9a04?q=80&w=2000&auto=format&fit=crop" 
           class="w-full h-full object-cover opacity-50" alt="Fondo Universidad">
      <div class="absolute inset-0 bg-gradient-to-br from-slate-900/100 via-[#7a1b2e]/85 to-slate-900/100 backdrop-blur-md"></div>
    </div>

    <div class="relative z-10 w-full max-w-md bg-white rounded-3xl shadow-[0_20px_60px_-15px_rgba(0,0,0,0.5)] p-8 md:p-10 animate-fade-in border border-white/20">
      
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-blue-50 mb-5 shadow-inner">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-blue-700" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2C9.243 2 7 4.243 7 7s2.243 5 5 5 5-2.243 5-5-2.243-5-5-5zm0 8c-1.654 0-3-1.346-3-3s1.346-3 3-3 3 1.346 3 3-1.346 3-3 3zm9 11v-1c0-3.859-3.141-7-7-7H10c-3.859 0-7 3.141-7 7v1h2v-1c0-2.757 2.243-5 5-5h4c2.757 0 5 2.243 5 5v1h2z"/>
          </svg>
        </div>
        <h2 class="text-3xl font-black text-slate-800 tracking-tight">Revista Digital</h2>
        <p class="text-sm text-slate-500 mt-2 font-medium">Ingresa tus credenciales o usa tu cuenta UMSA.</p>
      </div>

      <form @submit.prevent="iniciarSesion" class="space-y-5">
        <div>
          <input v-model="formLogin.correo" type="email" placeholder="Correo electrónico" required 
            class="w-full px-4 py-3.5 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:border-[#7a1b2e] focus:ring-4 focus:ring-[#7a1b2e]/10 outline-none transition text-slate-700 font-medium">
        </div>
        <div class="relative">
          <input v-model="formLogin.contrasena" :type="verClave ? 'text' : 'password'" placeholder="Contraseña" required
            class="w-full px-4 py-3.5 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:border-[#7a1b2e] focus:ring-4 focus:ring-[#7a1b2e]/10 outline-none transition text-slate-700 font-medium">
          <button type="button" @click="verClave = !verClave" class="absolute right-4 top-3.5 text-slate-400 hover:text-[#7a1b2e] transition text-xs font-bold uppercase tracking-wide">
            <span v-if="!verClave">Mostrar</span><span v-else>Ocultar</span>
          </button>
        </div>

        <button type="submit" :disabled="cargando" class="w-full bg-[#7a1b2e] text-white font-bold py-3.5 rounded-xl hover:bg-[#5a1422] transition-all duration-300 shadow-lg hover:shadow-[#7a1b2e]/40 disabled:opacity-50">
          {{ cargando ? 'Verificando...' : 'Ingresar al sistema' }}
        </button>

        <div class="text-center mt-4">
          <button type="button" @click="recuperarContrasena" class="text-sm font-bold text-slate-500 hover:text-[#7a1b2e] transition-colors duration-300">
            ¿Olvidaste tu contraseña?
          </button>
        </div>

      </form>

      <div class="mt-8 mb-6 relative">
        <div class="absolute inset-0 flex items-center">
          <div class="w-full border-t border-slate-200"></div>
        </div>
        <div class="relative flex justify-center text-sm">
          <span class="px-4 bg-white text-slate-400 font-bold uppercase tracking-widest text-[10px]">Opciones de Acceso</span>
        </div>
      </div>

      <button @click="loginConGoogle" type="button" class="w-full border-2 border-slate-100 flex items-center justify-center gap-3 py-3.5 rounded-xl bg-white hover:bg-slate-50 transition-all duration-300 font-bold text-slate-700 text-sm hover:border-slate-300 shadow-sm">
        <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/google/google-original.svg" class="w-5">
        Continuar con cuenta UMSA
      </button>
      
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../services/api';
import { notificarExito, notificarError } from '../services/alertas';
import Swal from 'sweetalert2';

const route = useRoute();
const router = useRouter();
const formLogin = ref({ correo: '', contrasena: '' });
const verClave = ref(false);
const cargando = ref(false);

const iniciarSesion = async () => {
  cargando.value = true;
  try {
    const formData = new FormData();
    formData.append('username', formLogin.value.correo);
    formData.append('password', formLogin.value.contrasena);

    const respuesta = await api.post('/auth/login', formData);
    localStorage.setItem('token_acceso', respuesta.data.access_token);
    
    const resUsuario = await api.get('/auth/me');
    localStorage.setItem('rol_usuario', resUsuario.data.rol);
    localStorage.setItem('usuario_correo', resUsuario.data.correo);

    notificarExito('¡Bienvenido de vuelta!');
    
    if (resUsuario.data.rol === 'ADMINISTRADOR') router.push('/admin');
    else if (resUsuario.data.rol === 'MODERADOR') router.push('/moderacion');
    else router.push('/dashboard');

  } catch (error) {
    notificarError('Correo o contraseña incorrectos.');
  } finally {
    cargando.value = false;
  }
};

const recuperarContrasena = async () => {
  const { value: email } = await Swal.fire({
    title: '<span style="color:#1e293b; font-weight:900;">Recuperar Contraseña</span>',
    html: '<p style="color:#64748b; font-size:14px; margin-bottom:10px;">Ingresa el correo de tu cuenta y te enviaremos las instrucciones para restaurarla.</p>',
    input: 'email',
    inputPlaceholder: 'ejemplo@umsa.bo',
    showCancelButton: true,
    confirmButtonText: 'Enviar enlace',
    cancelButtonText: 'Cancelar',
    confirmButtonColor: '#7a1b2e',
    cancelButtonColor: '#94a3b8',
    customClass: {
      popup: 'rounded-[2rem] shadow-2xl font-sans border border-slate-100',
      confirmButton: 'font-bold rounded-xl px-6 py-3',
      cancelButton: 'font-bold rounded-xl px-6 py-3',
      input: 'border-slate-200 rounded-xl focus:border-[#7a1b2e] focus:ring-4 focus:ring-[#7a1b2e]/10 px-4 py-3 font-medium text-slate-700 outline-none transition'
    }
  });

  if (email) {
    try {
      Swal.fire({ title: 'Enviando...', allowOutsideClick: false, didOpen: () => Swal.showLoading() });
      
      // Llamada a nuestro nuevo backend
      await api.post('/auth/solicitar-recuperacion', { correo: email });
      
      Swal.fire({
        title: '<span style="color:#1e293b; font-weight:900;">¡Correo enviado!</span>',
        html: '<p style="color:#64748b;">Revisa tu bandeja de entrada o la carpeta de Spam.</p>',
        icon: 'success',
        confirmButtonColor: '#7a1b2e',
        customClass: { popup: 'rounded-[2rem] font-sans', confirmButton: 'font-bold rounded-xl px-6 py-3' }
      });
    } catch (error) {
      notificarError('No se encontró una cuenta con ese correo o hubo un error.');
    }
  }
};

const loginConGoogle = async () => {
  try {
    const res = await api.get('/auth/google/login');
    window.location.href = res.data.url;
  } catch (error) {
    notificarError('Error al conectar con Google.');
  }
};

onMounted(async () => {
  const token = route.query.token;
  const error = route.query.error;

  if (error === 'dominio') notificarError('Usa solo correos @umsa.bo');

  if (token) {
    localStorage.setItem('token_acceso', token);
    const res = await api.get('/auth/me');
    localStorage.setItem('rol_usuario', res.data.rol);
    notificarExito(`Bienvenido ${res.data.nombre}`);
    router.push('/dashboard');
  }
});
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.5s ease-out forwards;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); scale: 0.95; }
  to { opacity: 1; transform: translateY(0); scale: 1; }
}
</style>