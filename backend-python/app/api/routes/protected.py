from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user, require_roles
from app.schemas.auth import ProtectedRouteResponse, UsuarioAutenticado

router = APIRouter(prefix="/demo-roles", tags=["roles"])


@router.get("/admin", response_model=ProtectedRouteResponse)
def admin_only_route(
    current_user: UsuarioAutenticado = Depends(require_roles("administrador")),
):
    return {
        "message": "Acceso permitido solo para administradores.",
        "current_user": current_user,
    }


@router.get("/supervision", response_model=ProtectedRouteResponse)
def supervisor_route(
    current_user: UsuarioAutenticado = Depends(
        require_roles("administrador", "supervisor")
    ),
):
    return {
        "message": "Acceso permitido para administradores y supervisores.",
        "current_user": current_user,
    }


@router.get("/authenticated", response_model=ProtectedRouteResponse)
def authenticated_route(
    current_user: UsuarioAutenticado = Depends(get_current_user),
):
    return {
        "message": "Acceso permitido para cualquier usuario autenticado.",
        "current_user": current_user,
    }
