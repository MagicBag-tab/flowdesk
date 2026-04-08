from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import decode_access_token
from app.db import get_db_cursor
from app.schemas.auth import UsuarioAutenticado
from app.utils.exceptions import AuthenticationError, AuthorizationError

http_bearer = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(http_bearer),
) -> UsuarioAutenticado:
    if credentials is None:
        raise AuthenticationError("Debe autenticarse para acceder.")

    payload = decode_access_token(credentials.credentials)

    with get_db_cursor() as cursor:
        cursor.execute(
            """
            SELECT
                u.id_usuario,
                u.nombre,
                u.email,
                u.id_rol,
                r.nombre AS rol
            FROM usuario u
            INNER JOIN rol r ON r.id_rol = u.id_rol
            WHERE u.id_usuario = %s
            """,
            (int(payload["sub"]),),
        )
        user = cursor.fetchone()

    if user is None:
        raise AuthenticationError("El usuario autenticado no existe.")

    return UsuarioAutenticado(**dict(user))


def require_roles(*allowed_roles: str):
    def dependency(current_user: UsuarioAutenticado = Depends(get_current_user)) -> UsuarioAutenticado:
        if current_user.rol not in allowed_roles:
            allowed = ", ".join(allowed_roles)
            raise AuthorizationError(f"Acceso restringido. Roles permitidos: {allowed}.")
        return current_user

    return dependency
