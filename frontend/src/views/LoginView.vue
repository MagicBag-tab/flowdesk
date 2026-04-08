<template>
    <v-container fluid class="fill-height login-bg">
        <v-row justify="center" alaign="center">
            <v-col xs="12" sm="4" md ="4" lg="4" xl="4">
                <div class="text-center mb-6">
                    <h2 class="text-indigo-darken-3 mt-2" style="font-weight:700; font-size:22px;">Flowdesk</h2>
                </div>
                <v-card rounded="lg" elevation="6">
                    <v-card-text class="pa-6">
                        <h1 class="text-indigo-darken-3 mb-1" style="font-size:24px; font-weight:700;">Iniciar Sesión</h1>
                        <v-alert v-if="errorGeneral" type="error" variant="tonal" closable class="mb-5" @click:close="errorGeneral = ''">
                            {{ errorGeneral }}
                        </v-alert>
                        <v-alert v-if="successMsg" type="success" variant="tonal" class="mb-5" @click:close="successMsg = ''">
                            {{ successMsg }}
                        </v-alert>
                        <v-form ref="form" @submit.prevent="login">
                            <v-text-field v-model="email" label="Correo Electrónico" type="email" color="indigo" clearable prepend-inner-icon="mdi-email-outline" variant="outlined" class="mb-2" :rules="reglasEmail" :error-messages="errores.email" @input="limpiarError('email')"/>
                            <v-text-field label="Contraseña" :type="mostrarPassword ? 'text' : 'password'" maxlength="20" color="indigo" clearable prepend-inner-icon="mdi-lock-outline" :append-inner-icon="mostrarPassword ? 'mdi-eye-off' : 'mdi-eye'" variant="outlined" density="comfortable" class="mb-1" v-model="password" @click:append-inner="mostrarPassword = !mostrarPassword" :rules="reglasPassword" :error-messages="errores.password" @input="limpiarError('password')"/>
                            <v-btn color="indigo" size="large" block rounded="md" :loading="cargando" :disabled="cargando" type="submit">
                                Iniciar Sesión
                            </v-btn>
                        </v-form>
                    </v-card-text> 
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import loginLogic from './login.js'
export default loginLogic
</script>


<style scoped>
.login-bg {
  min-height: 100vh;
  background: linear-gradient(135deg, #dce8fd 0%, #eef4ff 50%, #f3e8ff 100%);
}
</style>