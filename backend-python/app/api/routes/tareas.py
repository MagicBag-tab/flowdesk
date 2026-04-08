from datetime import date

from fastapi import APIRouter, Depends, Query, status

from app.dependencies import get_current_user_id
from app.schemas.tareas import TareaCreate, TareaResponse
from app.services.tareas import create_tarea, list_tareas

router = APIRouter(prefix="/tareas", tags=["tareas"])


@router.post("", response_model=TareaResponse, status_code=status.HTTP_201_CREATED)
def create_tarea_endpoint(
    payload: TareaCreate,
    current_user_id: int = Depends(get_current_user_id),
):
    return create_tarea(
        user_id=current_user_id,
        titulo=payload.titulo,
        descripcion=payload.descripcion,
        fecha_limite=payload.fecha_limite,
    )


@router.get("", response_model=list[TareaResponse])
def list_tareas_endpoint(
    fecha: date | None = Query(default=None),
    solo_pendientes: bool | None = Query(default=None),
    current_user_id: int = Depends(get_current_user_id),
):
    solo_pendientes_resuelto = solo_pendientes if solo_pendientes is not None else fecha is not None

    return list_tareas(
        user_id=current_user_id,
        fecha=fecha,
        solo_pendientes=solo_pendientes_resuelto,
    )
