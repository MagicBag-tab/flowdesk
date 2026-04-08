export default {
  name: 'LoginView',

  data() {
    return {
      email: '',
      password: '',
      recordarme: false,
 
      mostrarPassword: false,
      cargando: false,
 
      errorGeneral: '',
      successMsg: '',
 
      errores: {
        email: '',
        password: '',
      },
 
      reglasEmail: [
        v => !!v                        || 'El correo es requerido.',
        v => /.+@.+\..+/.test(v)        || 'Ingresa un correo válido.',
      ],
 
      reglasPassword: [
        v => !!v                        || 'La contraseña es requerida.',
        v => v.length >= 6              || 'Mínimo 6 caracteres.',
        v => v.length <= 20             || 'Máximo 20 caracteres.',
      ],
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
      }
 
      return valido
    },
 
    async login() {
      this.errorGeneral = ''
      this.successMsg   = ''
 
      if (!this.validarFormulario()) return
 
      this.cargando = true
 
      try {
        //llamada a backend
      } catch (error) {
        this.errorGeneral = 'Error de conexión. Intenta de nuevo.'
        console.error('Error en login:', error)
 
      } finally {
        this.cargando = false
      }
    },
  },
}