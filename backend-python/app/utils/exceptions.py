class AppError(Exception):
    def _init_(self, message, status_code = 400):
        self.message = message
        self.status_code = status_code

class ValidationError(AppError):
    def _init_(self, message = "Error de validación"):
        super()._init_(message, 400)

class NotFoundError(AppError):
    def _init_(self, message = "Recurso no encontrado"):
        super()._init_(message, 404)