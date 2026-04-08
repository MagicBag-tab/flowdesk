import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../components/login/LoginView.vue'
import Inventory from '../components/inventory/Inventory.vue'

const routes = [
  { path: '/',          component: LoginView },
  { path: '/inventory', component: Inventory },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})