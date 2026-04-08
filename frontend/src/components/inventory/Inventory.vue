<template>
  <div class="inventario-page">
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">Inventario</h1>
        <span class="product-count">{{ productosFiltrados.length }} productos</span>
      </div>
      <button class="btn-add" @click="abrirModal()">
        <span class="btn-icon">+</span>
        Agregar producto
      </button>
    </div>

    <div class="content-wrapper">

      <div class="table-container">
        <table class="inventory-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Nombre</th>
              <th>Cantidad</th>
              <th>Descripción</th>
              <th>Categoría</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="producto in productosFiltrados"
              :key="producto.id"
              :class="{ 'low-stock': producto.cantidad <= producto.stockMinimo }"
            >
              <td class="td-id">{{ producto.id }}</td>
              <td class="td-nombre">
                <span class="nombre-text">{{ producto.nombre }}</span>
                <span v-if="producto.cantidad <= producto.stockMinimo" class="badge-alerta">
                  Stock bajo
                </span>
              </td>
              <td class="td-cantidad">
                <span
                  class="cantidad-pill"
                  :class="{
                    'cantidad-ok':  producto.cantidad > producto.stockMinimo,
                    'cantidad-low': producto.cantidad <= producto.stockMinimo
                  }"
                >
                  {{ producto.cantidad }}
                </span>
              </td>
              <td class="td-desc">{{ producto.descripcion }}</td>
              <td class="td-cat">
                <span class="cat-tag">{{ producto.categoria }}</span>
              </td>
              <td class="td-acciones">
                <button class="btn-action edit" @click="abrirModal(producto)" title="Editar">✏️</button>
                <button class="btn-action delete" @click="confirmarEliminar(producto)" title="Eliminar">🗑️</button>
              </td>
            </tr>
            <tr v-if="productosFiltrados.length === 0">
              <td colspan="6" class="empty-state">
                No hay productos para los filtros seleccionados.
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="filtros-panel">
        <p class="filtros-titulo">Filtros</p>

        <p class="filtros-label">Categoría</p>
        <ul class="filtros-list">
          <li
            v-for="cat in categorias"
            :key="cat"
            :class="{ active: categoriasSeleccionadas.includes(cat) }"
            @click="toggleCategoria(cat)"
          >
            <span class="checkbox" :class="{ checked: categoriasSeleccionadas.includes(cat) }">
              <span v-if="categoriasSeleccionadas.includes(cat)">✓</span>
            </span>
            {{ cat }}
          </li>
        </ul>

        <hr class="filtros-divider" />

        <p class="filtros-label">Stock</p>
        <ul class="filtros-list">
          <li :class="{ active: filtroStock === 'todos' }" @click="filtroStock = 'todos'">
            <span class="checkbox" :class="{ checked: filtroStock === 'todos' }">
              <span v-if="filtroStock === 'todos'">✓</span>
            </span>
            Todos
          </li>
          <li :class="{ active: filtroStock === 'bajo' }" @click="filtroStock = 'bajo'">
            <span class="checkbox" :class="{ checked: filtroStock === 'bajo' }">
              <span v-if="filtroStock === 'bajo'">✓</span>
            </span>
            Stock bajo
          </li>
          <li :class="{ active: filtroStock === 'normal' }" @click="filtroStock = 'normal'">
            <span class="checkbox" :class="{ checked: filtroStock === 'normal' }">
              <span v-if="filtroStock === 'normal'">✓</span>
            </span>
            Normal
          </li>
        </ul>

        <button class="btn-limpiar" @click="limpiarFiltros">Limpiar filtros</button>
      </div>
    </div>

    <div v-if="modalVisible" class="modal-overlay" @click.self="cerrarModal">
      <div class="modal">
        <div class="modal-header">
          <h2 class="modal-title">{{ editando ? 'Editar producto' : 'Nuevo producto' }}</h2>
          <button class="modal-close" @click="cerrarModal">✕</button>
        </div>

        <form class="modal-form" @submit.prevent="guardarProducto">
          <div class="form-row">
            <div class="form-group">
              <label>Nombre <span class="required">*</span></label>
              <input v-model="form.nombre" type="text" placeholder="Ej. Arroz Diana 500g" required />
            </div>
            <div class="form-group">
              <label>Categoría <span class="required">*</span></label>
              <select v-model="form.categoria" required>
                <option value="" disabled>Seleccionar...</option>
                <option v-for="cat in categorias" :key="cat" :value="cat">{{ cat }}</option>
                <option value="__nueva__">+ Nueva categoría</option>
              </select>
            </div>
          </div>

          <div v-if="form.categoria === '__nueva__'" class="form-group">
            <label>Nueva categoría <span class="required">*</span></label>
            <input v-model="nuevaCategoria" type="text" placeholder="Nombre de la categoría" />
          </div>

          <div class="form-group">
            <label>Descripción</label>
            <input v-model="form.descripcion" type="text" placeholder="Descripción breve del producto" />
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Precio (Q) <span class="required">*</span></label>
              <input v-model.number="form.precio" type="number" min="0" step="0.01" placeholder="0.00" required />
            </div>
            <div class="form-group">
              <label>Cantidad en stock <span class="required">*</span></label>
              <input v-model.number="form.cantidad" type="number" min="0" placeholder="0" required />
            </div>
            <div class="form-group">
              <label>Stock mínimo</label>
              <input v-model.number="form.stockMinimo" type="number" min="0" placeholder="5" />
            </div>
          </div>

          <div v-if="errorForm" class="form-error">{{ errorForm }}</div>

          <div class="modal-actions">
            <button type="button" class="btn-cancel" @click="cerrarModal">Cancelar</button>
            <button type="submit" class="btn-save">
              {{ editando ? 'Guardar cambios' : 'Crear producto' }}
            </button>
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

<script setup src="./Inventory.js"></script>

<style src="./Inventory.css" scoped></style>