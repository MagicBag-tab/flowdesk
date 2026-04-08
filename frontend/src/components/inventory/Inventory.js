import { ref, computed } from 'vue'

const productos = ref([
  { id: 'P001', nombre: 'Terra Lab',     cantidad: 112, descripcion: 'Desinfectante',   categoria: 'All',        precio: 45.00,  stockMinimo: 10 },
  { id: 'P002', nombre: 'Topo Gigio',   cantidad: 47,  descripcion: 'Uso doméstico',   categoria: 'Doméstico',  precio: 28.50,  stockMinimo: 15 },
  { id: 'P003', nombre: 'Versa 24',     cantidad: 12,  descripcion: 'Transit 14',      categoria: 'Doméstico',  precio: 62.00,  stockMinimo: 20 },
  { id: 'P004', nombre: 'Purple Lexus', cantidad: 600, descripcion: 'Escalas AOS',     categoria: 'Electrónico',precio: 120.00, stockMinimo: 50 },
  { id: 'P005', nombre: 'Tallo 278',    cantidad: 30,  descripcion: 'Logi',            categoria: 'Ropa',       precio: 89.00,  stockMinimo: 10 },
  { id: 'P006', nombre: 'Nuevo Blanco', cantidad: 25,  descripcion: 'Residuos #12',    categoria: 'All',        precio: 15.00,  stockMinimo: 30 },
])

const categorias = computed(() => {
  const cats = [...new Set(productos.value.map(p => p.categoria))]
  return cats.sort()
})

const categoriasSeleccionadas = ref([])
const filtroStock = ref('todos')

function toggleCategoria(cat) {
  const idx = categoriasSeleccionadas.value.indexOf(cat)
  if (idx === -1) categoriasSeleccionadas.value.push(cat)
  else categoriasSeleccionadas.value.splice(idx, 1)
}

function limpiarFiltros() {
  categoriasSeleccionadas.value = []
  filtroStock.value = 'todos'
}

const productosFiltrados = computed(() => {
  return productos.value.filter(p => {
    const pasaCat =
      categoriasSeleccionadas.value.length === 0 ||
      categoriasSeleccionadas.value.includes(p.categoria)

    const pasaStock =
      filtroStock.value === 'todos' ||
      (filtroStock.value === 'bajo'   && p.cantidad <= p.stockMinimo) ||
      (filtroStock.value === 'normal' && p.cantidad >  p.stockMinimo)

    return pasaCat && pasaStock
  })
})

const modalVisible   = ref(false)
const editando       = ref(false)
const errorForm      = ref('')
const nuevaCategoria = ref('')

const formVacio = () => ({
  id: '', nombre: '', descripcion: '', categoria: '',
  precio: null, cantidad: null, stockMinimo: 5,
})
const form = ref(formVacio())

function abrirModal(producto = null) {
  errorForm.value = ''
  nuevaCategoria.value = ''
  if (producto) {
    editando.value = true
    form.value = { ...producto }
  } else {
    editando.value = false
    form.value = formVacio()
  }
  modalVisible.value = true
}

function cerrarModal() {
  modalVisible.value = false
}

function guardarProducto() {
  errorForm.value = ''

  if (form.value.categoria === '__nueva__') {
    if (!nuevaCategoria.value.trim()) {
      errorForm.value = 'Ingresa el nombre de la nueva categoría.'
      return
    }
    form.value.categoria = nuevaCategoria.value.trim()
  }

  if (editando.value) {
    const idx = productos.value.findIndex(p => p.id === form.value.id)
    if (idx !== -1) productos.value[idx] = { ...form.value }
  } else {
    const nuevoId = 'P' + String(productos.value.length + 1).padStart(3, '0')
    productos.value.push({ ...form.value, id: nuevoId })
  }

  cerrarModal()
}

const modalEliminar     = ref(false)
const productoAEliminar = ref(null)

function confirmarEliminar(producto) {
  productoAEliminar.value = producto
  modalEliminar.value = true
}

function eliminarProducto() {
  productos.value = productos.value.filter(p => p.id !== productoAEliminar.value.id)
  modalEliminar.value = false
  productoAEliminar.value = null
}