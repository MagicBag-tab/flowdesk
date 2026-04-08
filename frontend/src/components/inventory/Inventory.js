import { ref, computed } from 'vue'

export const productos = ref([
  { id: 'P001', nombre: 'Terra Lab',     cantidad: 112, descripcion: 'Desinfectante',   precio: 45.00,  stockMinimo: 10 },
  { id: 'P002', nombre: 'Topo Gigio',   cantidad: 47,  descripcion: 'Uso doméstico',   precio: 28.50,  stockMinimo: 15 },
  { id: 'P003', nombre: 'Versa 24',     cantidad: 12,  descripcion: 'Transit 14',      precio: 62.00,  stockMinimo: 20 },
  { id: 'P004', nombre: 'Purple Lexus', cantidad: 600, descripcion: 'Escalas AOS',     precio: 120.00, stockMinimo: 50 },
  { id: 'P005', nombre: 'Tallo 278',    cantidad: 30,  descripcion: 'Logi',            precio: 89.00,  stockMinimo: 10 },
  { id: 'P006', nombre: 'Nuevo Blanco', cantidad: 25,  descripcion: 'Residuos #12',    precio: 15.00,  stockMinimo: 30 },
])

export const filtroStock = ref('todos')

export const productosFiltrados = computed(() => {
  return productos.value.filter(p =>
    filtroStock.value === 'todos' ||
    (filtroStock.value === 'bajo'   && p.cantidad <= p.stockMinimo) ||
    (filtroStock.value === 'normal' && p.cantidad >  p.stockMinimo)
  )
})

export const modalVisible   = ref(false)
export const editando       = ref(false)
export const errorForm      = ref('')

const formVacio = () => ({
  id: '', nombre: '', descripcion: '',
  precio: null, cantidad: null, stockMinimo: 5,
})
export const form = ref(formVacio())

export function abrirModal(producto = null) {
  errorForm.value = ''
  if (producto) {
    editando.value = true
    form.value = { ...producto }
  } else {
    editando.value = false
    form.value = formVacio()
  }
  modalVisible.value = true
}

export function cerrarModal() {
  modalVisible.value = false
}

export function guardarProducto() {
  errorForm.value = ''

  if (editando.value) {
    const idx = productos.value.findIndex(p => p.id === form.value.id)
    if (idx !== -1) productos.value[idx] = { ...form.value }
  } else {
    const nuevoId = 'P' + String(productos.value.length + 1).padStart(3, '0')
    productos.value.push({ ...form.value, id: nuevoId })
  }

  cerrarModal()
}

export const modalEliminar     = ref(false)
export const productoAEliminar = ref(null)

export function confirmarEliminar(producto) {
  productoAEliminar.value = producto
  modalEliminar.value = true
}

export function eliminarProducto() {
  productos.value = productos.value.filter(p => p.id !== productoAEliminar.value.id)
  modalEliminar.value = false
  productoAEliminar.value = null
}