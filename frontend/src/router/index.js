import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../components/login/LoginView.vue'
import Inventory from '../components/inventory/Inventory.vue'
import Registro from '../components/registro/registro.vue'

const routes = [
  { path: '/',          component: LoginView },
  { path: '/registro', component: Registro },
  { path: '/inventory', component: Inventory },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})