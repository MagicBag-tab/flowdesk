class AppError(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

class ValidationError(AppError):
    def __init__(self, message="Error de validación"):
        super().__init__(message, 400)

class NotFoundError(AppError):
    def __init__(self, message="Recurso no encontrado"):
        super().__init__(message, 404)


class ConflictError(AppError):
    def __init__(self, message="El recurso ya existe"):
        super().__init__(message, 409)


class AuthenticationError(AppError):
    def __init__(self, message="No autenticado"):
        super().__init__(message, 401)


class AuthorizationError(AppError):
    def __init__(self, message="No autorizado"):
        super().__init__(message, 403)
