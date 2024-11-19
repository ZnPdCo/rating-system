import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'problems',
      component: () => import('../views/ProblemsView.vue'),
    },
    {
      path: '/legal/',
      name: 'legal',
      component: () => import('../views/LegalView.vue'),
    },
    {
      path: '/admin/',
      name: 'admin',
      component: () => import('../views/AdminView.vue'),
    },
    {
      path: '/login/',
      name: 'Login',
      component: () => import('../views/LoginView.vue'),
    },
    {
      path: '/update_password/',
      name: 'Update Password',
      component: () => import('../views/UpdatePasswordView.vue'),
    },
    {
      path: '/verify/',
      name: 'Verify',
      component: () => import('../views/VerifyView.vue'),
    },
  ],
})

export default router
