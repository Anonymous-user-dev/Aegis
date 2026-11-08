from fastapi import FastAPI
from app.api.routes.executions import router as executions_router
from app.api.routes.auth import router as auth_router

version = "v1"

version_prefix = f"/api/{version}"

description = ""

app = FastAPI(
    title="Aegis!!!",
    description=description,
    version=version,
)



app.include_router(executions_router, prefix=f"{version_prefix}/executions", tags=["executions"])
app.include_router(auth_router, prefix=f"{version_prefix}/auth", tags=["auth"])