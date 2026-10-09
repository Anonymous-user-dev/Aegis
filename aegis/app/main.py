from fastapi import FastAPI
from app.api.routes.executions import router as executions_router

app = FastAPI(
    title="Aegis!!!"
)

app.include_router(executions_router)