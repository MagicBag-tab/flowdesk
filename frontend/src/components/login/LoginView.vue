<template>
  <div class="login-bg">
    <div class="login-card">
      <div class="login-brand">
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
          <label class="form-label">Usuario</label>
          <input
            v-model="username"
            class="form-input"
            :class="{ 'input-error': errores.username }"
            placeholder="Nombre de usuario"
            @input="limpiarError('username')"
          />
          <span v-if="errores.username" class="error-msg">{{ errores.username }}</span>
        </div>

        <div class="form-group">
          <label class="form-label">Contraseña</label>
          <input
            v-model="password"
            type="password"
            class="form-input"
            :class="{ 'input-error': errores.password }"
            placeholder="Ingresa tu contraseña"
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
      <p class="link-registro">
        <span class="link-texto" @click="$router.push('/registro')">Registra tu negocio</span>
      </p>
    </div>
  </div>
</template>

<script>
import loginLogic from './login.js'
export default loginLogic
</script>


<style src="./login.css" scoped></style>