<template>
  <div class="login-bg">
    <div class="login-card">
      <div class="login-brand">
        <span class="brand-icon">📋</span>
        <h2 class="brand-name">FlowDesk</h2>
      </div>

      <h1 class="login-title">Iniciar Sesión</h1>

      <div v-if="errorGeneral" class="alert alert-error">
        <span>{{ errorGeneral }}</span>
        <button class="alert-close" @click="errorGeneral = ''">✕</button>
      </div>

      <div v-if="successMsg" class="alert alert-success">
        <span>{{ successMsg }}</span>
      </div>

      <form @submit.prevent="login">
        <div class="form-group">
          <label class="form-label">Correo Electrónico</label>
          <input
            v-model="email"
            type="email"
            class="form-input"
            :class="{ 'input-error': errores.email }"
            placeholder="correo@ejemplo.com"
            @input="limpiarError('email')"
          />
          <span v-if="errores.email" class="error-msg">{{ errores.email }}</span>
        </div>

        <div class="form-group">
          <label class="form-label">Contraseña</label>
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

        <button type="submit" class="btn-login" :disabled="cargando">
          <span v-if="cargando" class="spinner"></span>
          <span>{{ cargando ? 'Ingresando...' : 'Iniciar Sesión' }}</span>
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import loginLogic from './login.js'
export default loginLogic
</script>


<style src="./login.css" scoped></style>