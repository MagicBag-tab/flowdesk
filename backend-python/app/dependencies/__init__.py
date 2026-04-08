from fastapi import Depends

from app.dependencies.auth import get_current_user
from app.schemas.auth import UsuarioAutenticado


def get_current_user_id(
    current_user: UsuarioAutenticado = Depends(get_current_user),
) -> int:
    return current_user.id_usuario
