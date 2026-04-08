from fastapi.testclient import TestClient

from app.db.bootstrap import BASE_ROLES, seed_base_roles_with_cursor
from app.main import app
from app.schemas.auth import RegisterRequest, UsuarioAutenticado
from app.services import auth as auth_service


class SeedCursor:
    def __init__(self):
        self.roles = {}
        self.last_result = None
        self.updated_role_id = None

    def execute(self, query, params=None):
        normalized = " ".join(query.split())

        if normalized.startswith("SELECT id_rol FROM rol WHERE nombre = %s"):
            role_name = params[0]
            self.last_result = self.roles.get(role_name)
            return

        if normalized.startswith("INSERT INTO rol"):
            role_name, description = params
            role = {
                "id_rol": len(self.roles) + 1,
                "nombre": role_name,
                "descripcion": description,
            }
            self.roles[role_name] = role
            self.last_result = None
            return

        if normalized.startswith("UPDATE usuario SET id_rol = %s"):
            self.updated_role_id = params[0]
            self.last_result = None
            return

        raise AssertionError(f"Consulta no esperada: {normalized}")

    def fetchone(self):
        return self.last_result


class RegisterCursor:
    def __init__(self, state):
        self.state = state
        self.last_result = None

    def execute(self, query, params=None):
        normalized = " ".join(query.split())

        if normalized.startswith("SELECT id_usuario FROM usuario WHERE email = %s"):
            self.last_result = self.state["users"].get(params[0])
            return

        if normalized.startswith("SELECT id_rol, nombre, descripcion FROM rol WHERE nombre = %s"):
            self.last_result = self.state["roles"].get(params[0])
            return

        if normalized.startswith("INSERT INTO usuario"):
            user_id = len(self.state["users"]) + 1
            user = {
                "id_usuario": user_id,
                "nombre": params[0],
                "email": params[1],
                "password_hash": params[2],
                "id_rol": params[3],
            }
            self.state["users"][params[1]] = user
            self.last_result = user
            return

        raise AssertionError(f"Consulta no esperada: {normalized}")

    def fetchone(self):
        return self.last_result


class CursorContextManager:
    def __init__(self, cursor):
        self.cursor = cursor

    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc, tb):
        return False


def build_current_user(role_name: str) -> UsuarioAutenticado:
    return UsuarioAutenticado(
        id_usuario=1,
        nombre="Yehosua",
        email="yehosua@example.com",
        id_rol=1,
        rol=role_name,
    )


def test_seed_base_roles_creates_expected_roles():
    cursor = SeedCursor()

    seed_base_roles_with_cursor(cursor)
    seed_base_roles_with_cursor(cursor)

    assert set(cursor.roles.keys()) == {role[0] for role in BASE_ROLES}
    assert cursor.updated_role_id == cursor.roles["empleado"]["id_rol"]


def test_register_assigns_default_role(monkeypatch):
    state = {
        "roles": {
            "empleado": {
                "id_rol": 4,
                "nombre": "empleado",
                "descripcion": "Rol operativo base con privilegios limitados.",
            }
        },
        "users": {},
    }

    monkeypatch.setattr(
        auth_service,
        "get_db_cursor",
        lambda commit=False: CursorContextManager(RegisterCursor(state)),
    )

    user = auth_service.register_user(
        RegisterRequest(
            nombre="Ana",
            email="ana@example.com",
            password="securepass",
        )
    )

    assert user["rol"]["nombre"] == "empleado"
    assert state["users"]["ana@example.com"]["id_rol"] == 4


def test_admin_route_allows_administrador():
    from app.dependencies.auth import get_current_user

    app.dependency_overrides[get_current_user] = lambda: build_current_user("administrador")
    client = TestClient(app)

    try:
        response = client.get("/demo-roles/admin")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["current_user"]["rol"] == "administrador"


def test_admin_route_denies_empleado():
    from app.dependencies.auth import get_current_user

    app.dependency_overrides[get_current_user] = lambda: build_current_user("empleado")
    client = TestClient(app)

    try:
        response = client.get("/demo-roles/admin")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 403
    assert "Roles permitidos" in response.json()["detail"]
