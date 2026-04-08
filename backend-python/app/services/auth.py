from app.core.security import create_access_token, hash_password, verify_password
from app.db import get_db_cursor
from app.db.bootstrap import DEFAULT_ROLE_NAME
from app.schemas.auth import LoginRequest, RegisterRequest
from app.utils.exceptions import AuthenticationError, ConflictError, NotFoundError


def register_user(payload: RegisterRequest) -> dict:
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            """
            SELECT id_usuario
            FROM usuario
            WHERE email = %s
            """,
            (payload.email,),
        )
        if cursor.fetchone() is not None:
            raise ConflictError("El correo ya esta registrado.")

        cursor.execute(
            """
            SELECT id_rol, nombre, descripcion
            FROM rol
            WHERE nombre = %s
            """,
            (DEFAULT_ROLE_NAME,),
        )
        default_role = cursor.fetchone()
        if default_role is None:
            raise NotFoundError("No existe el rol por defecto configurado.")

        cursor.execute(
            """
            INSERT INTO usuario (nombre, email, password_hash, id_rol)
            VALUES (%s, %s, %s, %s)
            RETURNING id_usuario, nombre, email, id_rol
            """,
            (
                payload.nombre,
                payload.email,
                hash_password(payload.password),
                default_role["id_rol"],
            ),
        )
        created_user = cursor.fetchone()

    return {
        "id_usuario": created_user["id_usuario"],
        "nombre": created_user["nombre"],
        "email": created_user["email"],
        "rol": default_role,
    }


def login_user(payload: LoginRequest) -> dict:
    with get_db_cursor() as cursor:
        cursor.execute(
            """
            SELECT
                u.id_usuario,
                u.nombre,
                u.email,
                u.password_hash,
                u.id_rol,
                r.nombre AS rol
            FROM usuario u
            INNER JOIN rol r ON r.id_rol = u.id_rol
            WHERE u.email = %s
            """,
            (payload.email,),
        )
        user = cursor.fetchone()

    if user is None or not verify_password(payload.password, user["password_hash"]):
        raise AuthenticationError("Credenciales invalidas.")

    return {
        "access_token": create_access_token(
            user_id=user["id_usuario"],
            role_name=user["rol"],
            email=user["email"],
        ),
        "token_type": "bearer",
    }
