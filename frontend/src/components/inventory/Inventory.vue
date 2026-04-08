<template>
  <div class="inventario-page">
    <div class="page-header-bar">
      <h1 class="page-title">Inventario</h1>
    </div>

    <div class="content-container">
      <div class="table-container">
        <table class="inventory-table">
          <thead>
            <tr>
              <th v-if="columnasVisibles.id">ID</th>
              <th v-if="columnasVisibles.nombre">Nombre</th>
              <th v-if="columnasVisibles.cantidad">Cantidad</th>
              <th v-if="columnasVisibles.descripcion">Descripción</th>
              <th v-if="columnasVisibles.precio">Precio c/u</th>
              <th v-if="columnasVisibles.proveedor">Proveedor</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="producto in productosFiltrados" :key="producto.id">
              <td v-if="columnasVisibles.id">{{ producto.id }}</td>
              <td v-if="columnasVisibles.nombre">{{ producto.nombre }}</td>
              <td v-if="columnasVisibles.cantidad">{{ producto.cantidad }}</td>
              <td v-if="columnasVisibles.descripcion">{{ producto.descripcion }}</td>
              <td v-if="columnasVisibles.precio">Q{{ producto.precio.toFixed(2) }}</td>
              <td v-if="columnasVisibles.proveedor">{{ producto.proveedor ?? '—' }}</td>
              <td class="td-acciones">
                <button class="btn-action" @click="abrirModal(producto)" title="Editar">✏️</button>
                <button class="btn-action" @click="confirmarEliminar(producto)" title="Eliminar">🗑️</button>
              </td>
            </tr>
            <tr v-if="productosFiltrados.length === 0">
              <td :colspan="columnaCount + 1" class="empty-state">
                No hay productos para mostrar.
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="filtros-panel">
        <p class="filtros-titulo">Filtros</p>
        <p class="filtros-sub">mostrar</p>
        <ul class="filtros-list">
          <li v-for="col in todasColumnas" :key="col.key" @click="toggleColumna(col.key)">
            <span class="checkbox" :class="{ checked: columnasVisibles[col.key] }">
              <span v-if="columnasVisibles[col.key]">✓</span>
            </span>
            {{ col.label }}
          </li>
        </ul>
      </div>
    </div>

    <button class="btn-fab" @click="abrirModal()" title="Agregar producto">+</button>

    <div v-if="modalVisible" class="modal-overlay" @click.self="cerrarModal">
      <div class="modal">
        <div class="modal-header">
          <h2 class="modal-title">{{ editando ? 'Editar producto' : 'Nuevo producto' }}</h2>
          <button class="modal-close" @click="cerrarModal">✕</button>
        </div>
        <form class="modal-form" @submit.prevent="guardarProducto">
          <div class="form-group">
            <label>Nombre <span class="required">*</span></label>
            <input v-model="form.nombre" type="text" placeholder="Ej. Arroz Diana 500g" required />
          </div>
          <div class="form-group">
            <label>Descripción</label>
            <input v-model="form.descripcion" type="text" placeholder="Descripción breve" />
          </div>
          <div class="form-row form-row-3">
            <div class="form-group form-group-sm">
              <label>Precio (Q) <span class="required">*</span></label>
              <input v-model.number="form.precio" type="number" min="0" step="0.01" placeholder="0.00" required />
            </div>
            <div class="form-group form-group-sm">
              <label>Cantidad <span class="required">*</span></label>
              <input v-model.number="form.cantidad" type="number" min="0" placeholder="0" required />
            </div>
            <div class="form-group form-group-sm">
              <label>Stock mínimo</label>
              <input v-model.number="form.stockMinimo" type="number" min="0" placeholder="5" />
            </div>
          </div>
          <div v-if="errorForm" class="form-error">{{ errorForm }}</div>
          <div class="modal-actions">
            <button type="button" class="btn-cancel" @click="cerrarModal">Cancelar</button>
            <button type="submit" class="btn-save">{{ editando ? 'Guardar cambios' : 'Crear producto' }}</button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="modalEliminar" class="modal-overlay" @click.self="modalEliminar = false">
      <div class="modal modal-sm">
        <div class="modal-header">
          <h2 class="modal-title">Eliminar producto</h2>
          <button class="modal-close" @click="modalEliminar = false">✕</button>
        </div>
        <p class="modal-body-text">
          ¿Estás seguro que deseas eliminar
          <strong>{{ productoAEliminar?.nombre }}</strong>?
          Esta acción no se puede deshacer.
        </p>
        <div class="modal-actions">
          <button class="btn-cancel" @click="modalEliminar = false">Cancelar</button>
          <button class="btn-delete-confirm" @click="eliminarProducto">Eliminar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import {
  productosFiltrados,
  modalVisible, editando, errorForm, form,
  abrirModal, cerrarModal, guardarProducto,
  modalEliminar, productoAEliminar,
  confirmarEliminar, eliminarProducto
} from './Inventory.js'

const todasColumnas = [
  { key: 'id',          label: 'ID' },
  { key: 'nombre',      label: 'Nombre' },
  { key: 'cantidad',    label: 'Cantidad' },
  { key: 'descripcion', label: 'Descripción' },
  { key: 'precio',      label: 'Precio c/u' },
  { key: 'proveedor',   label: 'Proveedor' },
]

const columnasVisibles = ref({
  id: true, nombre: true, cantidad: true,
  descripcion: true, precio: false, proveedor: false,
})

function toggleColumna(key) {
  columnasVisibles.value[key] = !columnasVisibles.value[key]
}

const columnaCount = computed(() =>
  Object.values(columnasVisibles.value).filter(Boolean).length
)
</script>

<style src="./Inventory.css" scoped></style>