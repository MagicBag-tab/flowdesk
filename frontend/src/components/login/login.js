export default {
  name: 'LoginView',

  data() {
    return {
      email: '',
      password: '',

      cargando: false,

      errorGeneral: '',
      successMsg: '',

      errores: {
        email: '',
        password: '',
      },
    }
  },

  methods: {
    limpiarError(campo) {
      this.errores[campo] = ''
      this.errorGeneral   = ''
    },

    validarFormulario() {
      let valido = true

      if (!this.email.trim()) {
        this.errores.email = 'El correo es requerido.'
        valido = false
      } else if (!/.+@.+\..+/.test(this.email)) {
        this.errores.email = 'Ingresa un correo válido.'
        valido = false
      }

      if (!this.password) {
        this.errores.password = 'La contraseña es requerida.'
        valido = false
      } else if (this.password.length < 6) {
        this.errores.password = 'Mínimo 6 caracteres.'
        valido = false
      } else if (this.password.length > 20) {
        this.errores.password = 'Máximo 20 caracteres.'
        valido = false
      }

      return valido
    },

    async login() {
      this.errorGeneral = ''
      this.successMsg   = ''

      if (!this.validarFormulario()) return

      this.cargando = true

      try {
        this.successMsg = 'Ingreso exitoso. Redirigiendo...'
        setTimeout(() => {
          this.$router.push('/inventory')
        }, 1000)

      } catch (error) {
        this.errorGeneral = 'Error de conexión. Intenta de nuevo.'
        console.error('Error en login:', error)

      } finally {
        this.cargando = false
      }
    },
  },
}