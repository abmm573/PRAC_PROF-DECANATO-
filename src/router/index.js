import { createRouter, createWebHistory } from 'vue-router'
import PortalPublico from '../views/PortalPublico.vue'
import Login from '../views/Login.vue'
import DashboardAutor from '../views/DashboardAutor.vue'
import PanelModerador from '../views/PanelModerador.vue'
import VisorRevista from '../views/VisorRevista.vue'
import PanelAdmin from '../views/PanelAdmin.vue' // <-- 1. Importamos la nueva vista
import RestaurarContrasena from '../views/RestaurarContrasena.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'inicio',
      component: PortalPublico
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    { 
      path: '/dashboard', 
      name: 'dashboard', 
      component: DashboardAutor 
    },
    { 
      path: '/moderacion', 
      name: 'moderacion', 
      component: PanelModerador 
    },
    { 
      path: '/admin', // <-- 2. Agregamos la ruta web
      name: 'admin', 
      component: PanelAdmin 
    },
    {
    path: '/restaurar',
    name: 'RestaurarContrasena',
    component: RestaurarContrasena
    },
    { 
      path: '/revista/:id', 
      name: 'visor', 
      component: VisorRevista 
    }
  ]
})

export default router