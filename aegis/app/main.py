from fastapi import FastAPI
from app.api.routes.executions import router as executions_router

version = "v1"

version_prefix = f"/api/{version}"

description = ""

app = FastAPI(
    title="Aegis!!!",
    description=description,
    version=version,
)



app.include_router(executions_router, prefix=f"{version_prefix}/execution", tags=["executions"])