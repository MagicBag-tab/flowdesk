export default {
  name: 'RegisterView',

  data() {
    return {
      nombreEmpresa: '',
      tipoNegocio: '',
      telefono: '',

      nombreAdmin: '',
      username: '',
      password: '',
      confirmarPassword: '',

      cargando: false,
      errorGeneral: '',
      successMsg: '',

      errores: {
        nombreEmpresa: '',
        tipoNegocio: '',
        nombreAdmin: '',
        username: '',
        password: '',
        confirmarPassword: '',
      },
    }
  },

  methods: {
    limpiarError(campo) {
      this.errores[campo] = ''
      this.errorGeneral = ''
    },

    validarFormulario() {
      let valido = true

      if (!this.nombreEmpresa.trim()) {
        this.errores.nombreEmpresa = 'El nombre de la empresa es requerido.'
        valido = false
      }

      if (!this.tipoNegocio) {
        this.errores.tipoNegocio = 'Selecciona el tipo de negocio.'
        valido = false
      }

      if (!this.nombreAdmin.trim()) {
        this.errores.nombreAdmin = 'El nombre del administrador es requerido.'
        valido = false
      }

      if (!this.username.trim()) {
        this.errores.username = 'El usuario es requerido.'
        valido = false
      } else if (this.username.length < 3) {
        this.errores.username = 'Mínimo 3 caracteres.'
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

      if (!this.confirmarPassword) {
        this.errores.confirmarPassword = 'Confirma tu contraseña.'
        valido = false
      } else if (this.password !== this.confirmarPassword) {
        this.errores.confirmarPassword = 'Las contraseñas no coinciden.'
        valido = false
      }

      return valido
    },

    async registrar() {
      this.errorGeneral = ''
      this.successMsg = ''

      if (!this.validarFormulario()) return

      this.cargando = true

      try {
        this.successMsg = 'Cuenta creada. Redirigiendo...'
        setTimeout(() => {
          this.$router.push('/')
        }, 1500)

      } catch (error) {
        this.errorGeneral = 'Error de conexión. Intenta de nuevo.'
        console.error('Error en registro:', error)

      } finally {
        this.cargando = false
      }
    },

    irALogin() {
      this.$router.push('/')
    },
  },
}