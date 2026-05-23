from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .routers import admin, tasks, users, ws
from .storage import get_storage

app = FastAPI(title="KR5 Task Manager")

app.include_router(tasks.router)
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(ws.router)

@app.on_event("startup")
def startup_event() -> None:
    get_storage().reset()

@app.get("/health", response_class=JSONResponse)
def health() -> dict:
    return {"status": "ok", "env": "docker"}
