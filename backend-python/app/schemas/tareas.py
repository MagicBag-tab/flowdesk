from datetime import date
from typing import Optional

from pydantic import BaseModel, field_validator


class TareaCreate(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    fecha_limite: date

    @field_validator("titulo")
    @classmethod
    def validate_titulo(cls, value: str) -> str:
        cleaned_value = value.strip()
        if not cleaned_value:
            raise ValueError("El titulo es obligatorio.")
        return cleaned_value

    @field_validator("descripcion")
    @classmethod
    def normalize_descripcion(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None

        cleaned_value = value.strip()
        return cleaned_value or None


class TareaResponse(BaseModel):
    id_tarea: int
    titulo: str
    descripcion: Optional[str] = None
    fecha_limite: date
    estado: str
    prioridad: str
    id_usuario: int
