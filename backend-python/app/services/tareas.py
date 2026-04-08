from datetime import date

from app.db import get_db_cursor

DEFAULT_ESTADO = "pendiente"
DEFAULT_PRIORIDAD = "media"


def create_tarea(user_id: int, titulo: str, descripcion: str | None, fecha_limite: date) -> dict:
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            """
            INSERT INTO tarea (id_usuario, titulo, descripcion, fecha_limite, estado, prioridad)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_tarea, titulo, descripcion, fecha_limite, estado, prioridad, id_usuario
            """,
            (user_id, titulo, descripcion, fecha_limite, DEFAULT_ESTADO, DEFAULT_PRIORIDAD),
        )
        tarea = cursor.fetchone()

    return dict(tarea)


def list_tareas(user_id: int, fecha: date | None = None, solo_pendientes: bool = False) -> list[dict]:
    query = """
        SELECT id_tarea, titulo, descripcion, fecha_limite, estado, prioridad, id_usuario
        FROM tarea
        WHERE id_usuario = %s
    """
    params: list[object] = [user_id]

    if fecha is not None:
        query += " AND fecha_limite = %s"
        params.append(fecha)

    if solo_pendientes:
        query += " AND LOWER(estado) = %s"
        params.append(DEFAULT_ESTADO)

    query += " ORDER BY fecha_limite ASC, id_tarea ASC"

    with get_db_cursor() as cursor:
        cursor.execute(query, tuple(params))
        tareas = cursor.fetchall()

    return [dict(tarea) for tarea in tareas]
