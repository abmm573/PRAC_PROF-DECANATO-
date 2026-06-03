import Swal from 'sweetalert2';

// Configuración para los "Toasts" (Notificaciones pequeñas en la esquina)
const Toast = Swal.mixin({
  toast: true,
  position: 'top-end',
  showConfirmButton: false,
  timer: 3000,
  timerProgressBar: true,
  didOpen: (toast) => {
    toast.addEventListener('mouseenter', Swal.stopTimer)
    toast.addEventListener('mouseleave', Swal.resumeTimer)
  }
});

export const notificarExito = (mensaje) => {
  Toast.fire({ icon: 'success', title: mensaje });
};

export const notificarError = (mensaje) => {
  Toast.fire({ icon: 'error', title: mensaje });
};

export const notificarInfo = (mensaje) => {
  Toast.fire({ icon: 'info', title: mensaje });
};