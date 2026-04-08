import psycopg2

from app.db import get_db_cursor

DEFAULT_ROLE_NAME = "empleado"
BASE_ROLES = (
    ("administrador", "Dueno o administrador principal del negocio."),
    ("supervisor", "Gerente o supervisor con permisos de coordinacion."),
    ("encargado_inventario", "Usuario operativo enfocado en inventario."),
    ("empleado", "Rol operativo base con privilegios limitados."),
)


def ensure_roles_schema() -> None:
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS rol (
                id_rol SERIAL PRIMARY KEY,
                nombre VARCHAR(50) UNIQUE NOT NULL,
                descripcion TEXT
            )
            """
        )
        cursor.execute(
            """
            DO $$
            BEGIN
                IF EXISTS (
                    SELECT 1
                    FROM information_schema.columns
                    WHERE table_schema = 'public'
                    AND table_name = 'rol'
                    AND column_name = 'nombre_rol'
                ) AND NOT EXISTS (
                    SELECT 1
                    FROM information_schema.columns
                    WHERE table_schema = 'public'
                    AND table_name = 'rol'
                    AND column_name = 'nombre'
                ) THEN
                    ALTER TABLE rol RENAME COLUMN nombre_rol TO nombre;
                ELSIF EXISTS (
                    SELECT 1
                    FROM information_schema.columns
                    WHERE table_schema = 'public'
                    AND table_name = 'rol'
                    AND column_name = 'nombre_rol'
                ) THEN
                    UPDATE rol
                    SET nombre = nombre_rol
                    WHERE nombre IS NULL;
                END IF;
            END $$;
            """
        )
        cursor.execute("ALTER TABLE rol ADD COLUMN IF NOT EXISTS nombre VARCHAR(50)")
        cursor.execute("ALTER TABLE rol ADD COLUMN IF NOT EXISTS descripcion TEXT")
        cursor.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS rol_nombre_unique_idx
            ON rol (nombre)
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS usuario (
                id_usuario SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                email VARCHAR(120) UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                id_rol INTEGER NOT NULL REFERENCES rol (id_rol)
            )
            """
        )
        cursor.execute("ALTER TABLE usuario ADD COLUMN IF NOT EXISTS nombre VARCHAR(100)")
        cursor.execute(
            """
            DO $$
            BEGIN
                IF EXISTS (
                    SELECT 1
                    FROM information_schema.columns
                    WHERE table_schema = 'public'
                    AND table_name = 'usuario'
                    AND column_name = 'correo'
                ) AND NOT EXISTS (
                    SELECT 1
                    FROM information_schema.columns
                    WHERE table_schema = 'public'
                    AND table_name = 'usuario'
                    AND column_name = 'email'
                ) THEN
                    ALTER TABLE usuario RENAME COLUMN correo TO email;
                ELSIF EXISTS (
                    SELECT 1
                    FROM information_schema.columns
                    WHERE table_schema = 'public'
                    AND table_name = 'usuario'
                    AND column_name = 'correo'
                ) THEN
                    UPDATE usuario
                    SET email = correo
                    WHERE email IS NULL;
                END IF;

                IF EXISTS (
                    SELECT 1
                    FROM information_schema.columns
                    WHERE table_schema = 'public'
                    AND table_name = 'usuario'
                    AND column_name = 'contrasena'
                ) AND NOT EXISTS (
                    SELECT 1
                    FROM information_schema.columns
                    WHERE table_schema = 'public'
                    AND table_name = 'usuario'
                    AND column_name = 'password_hash'
                ) THEN
                    ALTER TABLE usuario RENAME COLUMN contrasena TO password_hash;
                ELSIF EXISTS (
                    SELECT 1
                    FROM information_schema.columns
                    WHERE table_schema = 'public'
                    AND table_name = 'usuario'
                    AND column_name = 'contrasena'
                ) THEN
                    UPDATE usuario
                    SET password_hash = contrasena
                    WHERE password_hash IS NULL;
                END IF;

                IF EXISTS (
                    SELECT 1
                    FROM information_schema.columns
                    WHERE table_schema = 'public'
                    AND table_name = 'usuario'
                    AND column_name = 'estado'
                ) THEN
                    ALTER TABLE usuario
                    ALTER COLUMN estado SET DEFAULT 'activo';

                    UPDATE usuario
                    SET estado = 'activo'
                    WHERE estado IS NULL;
                END IF;
            END $$;
            """
        )
        cursor.execute("ALTER TABLE usuario ADD COLUMN IF NOT EXISTS email VARCHAR(120)")
        cursor.execute("ALTER TABLE usuario ADD COLUMN IF NOT EXISTS password_hash TEXT")
        cursor.execute("ALTER TABLE usuario ADD COLUMN IF NOT EXISTS id_rol INTEGER")
        cursor.execute("ALTER TABLE usuario ADD COLUMN IF NOT EXISTS estado VARCHAR(30) DEFAULT 'activo'")
        cursor.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS usuario_email_unique_idx
            ON usuario (email)
            """
        )
        cursor.execute(
            """
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1
                    FROM pg_constraint
                    WHERE conname = 'usuario_id_rol_fkey'
                ) THEN
                    ALTER TABLE usuario
                    ADD CONSTRAINT usuario_id_rol_fkey
                    FOREIGN KEY (id_rol) REFERENCES rol (id_rol);
                END IF;
            END $$;
            """
        )


def seed_base_roles_with_cursor(cursor) -> None:
    for nombre, descripcion in BASE_ROLES:
        cursor.execute("SELECT id_rol FROM rol WHERE nombre = %s", (nombre,))
        if cursor.fetchone() is None:
            cursor.execute(
                """
                INSERT INTO rol (nombre, descripcion)
                VALUES (%s, %s)
                """,
                (nombre, descripcion),
            )

    cursor.execute("SELECT id_rol FROM rol WHERE nombre = %s", (DEFAULT_ROLE_NAME,))
    default_role = cursor.fetchone()
    if default_role is not None:
        cursor.execute(
            """
            UPDATE usuario
            SET id_rol = %s
            WHERE id_rol IS NULL
            """,
            (default_role["id_rol"],),
        )


def seed_base_roles() -> None:
    with get_db_cursor(commit=True) as cursor:
        seed_base_roles_with_cursor(cursor)


def initialize_roles_module() -> None:
    try:
        ensure_roles_schema()
        seed_base_roles()
    except psycopg2.OperationalError:
        return


if __name__ == "__main__":
    initialize_roles_module()
