<template>
  <div class="login-bg">
    <div class="login-card register-card">
      <div class="login-brand">
        <h2 class="brand-name">FlowDesk</h2>
      </div>

      <h1 class="login-title">Crear Cuenta</h1>
      <p class="login-subtitle">Registra tu empresa para comenzar</p>

      <div v-if="errorGeneral" class="alert alert-error">
        <span>{{ errorGeneral }}</span>
        <button class="alert-close" @click="errorGeneral = ''">✕</button>
      </div>

      <div v-if="successMsg" class="alert alert-success">
        <span>{{ successMsg }}</span>
      </div>

      <form @submit.prevent="registrar">

        <p class="seccion-titulo">Datos de la empresa</p>

        <div class="form-group">
          <label class="form-label">Nombre de la empresa <span class="required">*</span></label>
          <input
            v-model="nombreEmpresa"
            type="text"
            class="form-input"
            :class="{ 'input-error': errores.nombreEmpresa }"
            placeholder="Ej. Mi Tienda S.A."
            @input="limpiarError('nombreEmpresa')"
          />
          <span v-if="errores.nombreEmpresa" class="error-msg">{{ errores.nombreEmpresa }}</span>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label class="form-label">Tipo de negocio <span class="required">*</span></label>
            <select
              v-model="tipoNegocio"
              class="form-input"
              :class="{ 'input-error': errores.tipoNegocio }"
              @change="limpiarError('tipoNegocio')"
            >
              <option value="" disabled>Selecciona...</option>
              <option value="tienda">Tienda / Retail</option>
              <option value="restaurante">Restaurante / Alimentos</option>
              <option value="manufactura">Manufactura</option>
              <option value="emprendimiento">Emprendimiento</option>
              <option value="otro">Otro</option>
            </select>
            <span v-if="errores.tipoNegocio" class="error-msg">{{ errores.tipoNegocio }}</span>
          </div>

          <div class="form-group">
            <label class="form-label">Teléfono</label>
            <input
              v-model="telefono"
              type="text"
              class="form-input"
              placeholder="Ej. 5555-1234"
              @input="limpiarError('telefono')"
            />
          </div>
        </div>

        <p class="seccion-titulo">Datos del administrador</p>

        <div class="form-group">
          <label class="form-label">Nombre completo <span class="required">*</span></label>
          <input
            v-model="nombreAdmin"
            type="text"
            class="form-input"
            :class="{ 'input-error': errores.nombreAdmin }"
            placeholder="Ej. Juan García"
            @input="limpiarError('nombreAdmin')"
          />
          <span v-if="errores.nombreAdmin" class="error-msg">{{ errores.nombreAdmin }}</span>
        </div>

        <div class="form-group">
          <label class="form-label">Usuario <span class="required">*</span></label>
          <input
            v-model="username"
            type="text"
            class="form-input"
            :class="{ 'input-error': errores.username }"
            placeholder="Nombre de usuario para iniciar sesión"
            @input="limpiarError('username')"
          />
          <span v-if="errores.username" class="error-msg">{{ errores.username }}</span>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label class="form-label">Contraseña <span class="required">*</span></label>
            <input
              v-model="password"
              type="password"
              class="form-input"
              :class="{ 'input-error': errores.password }"
              placeholder="Mínimo 6 caracteres"
              maxlength="20"
              @input="limpiarError('password')"
            />
            <span v-if="errores.password" class="error-msg">{{ errores.password }}</span>
          </div>

          <div class="form-group">
            <label class="form-label">Confirmar contraseña <span class="required">*</span></label>
            <input
              v-model="confirmarPassword"
              type="password"
              class="form-input"
              :class="{ 'input-error': errores.confirmarPassword }"
              placeholder="Repite tu contraseña"
              maxlength="20"
              @input="limpiarError('confirmarPassword')"
            />
            <span v-if="errores.confirmarPassword" class="error-msg">{{ errores.confirmarPassword }}</span>
          </div>
        </div>

        <button type="submit" class="btn-login" :disabled="cargando">
          <span v-if="cargando" class="spinner"></span>
          <span>{{ cargando ? 'Registrando...' : 'Crear cuenta' }}</span>
        </button>

        <p class="link-login">
          ¿Ya tienes cuenta?
          <span class="link-texto" @click="irALogin">Iniciar sesión</span>
        </p>

      </form>
    </div>
  </div>
</template>

<script>
import registerLogic from './registro.js'
export default registerLogic
</script>

<style src="./registro.css" scoped></style>
