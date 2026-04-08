from fastapi import APIRouter, status

from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UsuarioResponse
from app.services.auth import login_user, register_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def register_user_endpoint(payload: RegisterRequest):
    return register_user(payload)


@router.post("/login", response_model=TokenResponse)
def login_user_endpoint(payload: LoginRequest):
    return login_user(payload)
