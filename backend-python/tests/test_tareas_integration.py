from datetime import date

from fastapi.testclient import TestClient

from app.main import app
from app.schemas.auth import UsuarioAutenticado
from app.services import tareas as tareas_service


class CursorContextManager:
    def __init__(self, cursor):
        self.cursor = cursor

    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc, tb):
        return False


class ListCursor:
    def __init__(self, rows):
        self.rows = rows
        self.executed_query = None
        self.executed_params = None

    def execute(self, query, params=None):
        self.executed_query = " ".join(query.split())
        self.executed_params = params

    def fetchall(self):
        return self.rows


def build_current_user(user_id: int = 1) -> UsuarioAutenticado:
    return UsuarioAutenticado(
        id_usuario=user_id,
        nombre="Ana",
        email="ana@example.com",
        id_rol=4,
        rol="empleado",
    )


def test_create_tarea_route_uses_authenticated_user(monkeypatch):
    from app.dependencies.auth import get_current_user
    from app.api.routes import tareas as tareas_route

    captured = {}

    def fake_create_tarea(user_id: int, titulo: str, descripcion: str | None, fecha_limite: date):
        captured["user_id"] = user_id
        captured["titulo"] = titulo
        captured["descripcion"] = descripcion
        captured["fecha_limite"] = fecha_limite
        return {
            "id_tarea": 10,
            "titulo": titulo,
            "descripcion": descripcion,
            "fecha_limite": fecha_limite,
            "estado": "pendiente",
            "prioridad": "media",
            "id_usuario": user_id,
        }

    monkeypatch.setattr(tareas_route, "create_tarea", fake_create_tarea)
    app.dependency_overrides[get_current_user] = lambda: build_current_user(user_id=7)
    client = TestClient(app)

    try:
        response = client.post(
            "/tareas",
            json={
                "titulo": "Llamar clientes",
                "descripcion": "Confirmar pedidos",
                "fecha_limite": "2026-04-08",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 201
    assert captured["user_id"] == 7
    assert response.json()["id_usuario"] == 7


def test_list_tareas_route_uses_daily_pending_defaults(monkeypatch):
    from app.dependencies.auth import get_current_user
    from app.api.routes import tareas as tareas_route

    captured = {}

    def fake_list_tareas(user_id: int, fecha: date | None = None, solo_pendientes: bool = False):
        captured["user_id"] = user_id
        captured["fecha"] = fecha
        captured["solo_pendientes"] = solo_pendientes
        return []

    monkeypatch.setattr(tareas_route, "list_tareas", fake_list_tareas)
    app.dependency_overrides[get_current_user] = lambda: build_current_user(user_id=3)
    client = TestClient(app)

    try:
        response = client.get("/tareas", params={"fecha": "2026-04-08"})
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert captured == {
        "user_id": 3,
        "fecha": date(2026, 4, 8),
        "solo_pendientes": True,
    }


def test_list_tareas_service_filters_by_user_date_and_pending(monkeypatch):
    rows = [
        {
            "id_tarea": 1,
            "titulo": "Comprar insumos",
            "descripcion": None,
            "fecha_limite": date(2026, 4, 8),
            "estado": "pendiente",
            "prioridad": "media",
            "id_usuario": 5,
        }
    ]
    cursor = ListCursor(rows)

    monkeypatch.setattr(
        tareas_service,
        "get_db_cursor",
        lambda commit=False: CursorContextManager(cursor),
    )

    tareas = tareas_service.list_tareas(
        user_id=5,
        fecha=date(2026, 4, 8),
        solo_pendientes=True,
    )

    assert tareas == rows
    assert "WHERE id_usuario = %s" in cursor.executed_query
    assert "AND fecha_limite = %s" in cursor.executed_query
    assert "AND LOWER(estado) = %s" in cursor.executed_query
    assert cursor.executed_params == (5, date(2026, 4, 8), "pendiente")
