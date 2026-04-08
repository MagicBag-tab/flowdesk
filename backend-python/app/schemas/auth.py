from pydantic import BaseModel, field_validator


class RolResponse(BaseModel):
    id_rol: int
    nombre: str
    descripcion: str | None = None


class RegisterRequest(BaseModel):
    nombre: str
    email: str
    password: str

    @field_validator("nombre")
    @classmethod
    def validate_nombre(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("El nombre es obligatorio.")
        return cleaned

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        cleaned = value.strip().lower()
        if "@" not in cleaned:
            raise ValueError("Debe enviar un correo valido.")
        return cleaned


class LoginRequest(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        cleaned = value.strip().lower()
        if "@" not in cleaned:
            raise ValueError("Debe enviar un correo valido.")
        return cleaned


class UsuarioAutenticado(BaseModel):
    id_usuario: int
    nombre: str
    email: str
    id_rol: int
    rol: str


class UsuarioResponse(BaseModel):
    id_usuario: int
    nombre: str
    email: str
    rol: RolResponse


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ProtectedRouteResponse(BaseModel):
    message: str
    current_user: UsuarioAutenticado
