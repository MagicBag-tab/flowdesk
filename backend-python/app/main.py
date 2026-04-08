from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routes.auth import router as auth_router
from app.api.routes.protected import router as protected_router
from app.api.routes.tareas import router as tareas_router
from app.db.bootstrap import initialize_roles_module
from app.utils.exceptions import AppError

app = FastAPI()
initialize_roles_module()
app.include_router(auth_router)
app.include_router(protected_router)
app.include_router(tareas_router)


@app.exception_handler(AppError)
def handle_app_error(_: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )


@app.get("/")
def read_root():
    return {"message": "Backend con Python"}
