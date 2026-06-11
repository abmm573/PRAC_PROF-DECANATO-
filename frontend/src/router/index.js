import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      // ✅ La pantalla pública de fichaje ES la página de inicio
      path: '/',
      name: 'fichaje',
      component: () => import('../views/FichajeView.vue'),
      // Accesible para todos, sin restricciones
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: '/reset-password',
      name: 'reset-password',
      component: () => import('../views/ResetPasswordView.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: '/perfil',
      name: 'perfil',
      component: () => import('../views/PerfilView.vue'),
      meta: { requiresAuth: true, allowedRoles: ['ADMINISTRADOR', 'ENCARGADO', 'PASANTE'] }
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/DashboardView.vue'),
      meta: { requiresAuth: true, allowedRoles: ['PASANTE'] }
    },
    {
      path: '/reporte-pdf',
      name: 'pasante-reporte-pdf',
      component: () => import('../views/PasanteReportePdf.vue'),
      meta: { requiresAuth: true, allowedRoles: ['PASANTE', 'ENCARGADO', 'ADMINISTRADOR'] }
    },
    {
      path: '/encargado',
      name: 'encargado-dashboard',
      component: () => import('../views/EncargadoDashboard.vue'),
      meta: { requiresAuth: true, allowedRoles: ['ENCARGADO'] }
    },
    {
      path: '/admin',
      name: 'admin-dashboard',
      component: () => import('../views/AdminDashboard.vue'),
      meta: { requiresAuth: true, allowedRoles: ['ADMINISTRADOR'] }
    },
    {
      path: '/carreras',
      name: 'admin-carreras',
      component: () => import('../views/AdminCarreras.vue'),
      meta: { requiresAuth: true, allowedRoles: ['ADMINISTRADOR'] }
    },
    {
      path: '/programas',
      name: 'admin-programas',
      component: () => import('../views/AdminProgramas.vue'),
      meta: { requiresAuth: true, allowedRoles: ['ADMINISTRADOR'] }
    },
    {
      path: '/usuarios',
      name: 'admin-usuarios',
      component: () => import('../views/AdminUsuarios.vue'),
      meta: { requiresAuth: true, allowedRoles: ['ADMINISTRADOR', 'ENCARGADO'] }
    },
  ]
})

router.beforeEach((to) => {
  const authStore = useAuthStore()
  const isAuthenticated = !!authStore.token
  const userRole = authStore.user?.rol

  const panelDelRol = (rol) => {
    if (rol === 'ADMINISTRADOR') return '/admin'
    if (rol === 'ENCARGADO')     return '/encargado'
    if (rol === 'PASANTE')       return '/dashboard'
    return null
  }

  // 1. Ya logueado intentando ir al login → a su panel
  if (to.meta.requiresGuest && isAuthenticated) {
    const destino = panelDelRol(userRole)
    if (destino && destino !== to.path) return destino
    return true
  }

  // 2. Ruta protegida sin sesión → al login
  if (to.meta.requiresAuth && !isAuthenticated) {
    if (to.path !== '/login') return '/login'
    return true
  }

  // 3. Ruta protegida con rol incorrecto → a su panel
  if (to.meta.requiresAuth && to.meta.allowedRoles && isAuthenticated) {
    if (!to.meta.allowedRoles.includes(userRole)) {
      const destino = panelDelRol(userRole)
      if (destino && destino !== to.path) return destino
      if (!destino) {
        authStore.logout()
        return '/login'
      }
    }
  }

  return true
})

export default router
