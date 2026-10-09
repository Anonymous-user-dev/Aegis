from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

from app.domain.execution import ExecutionStatus

class CreateExecutionRequest(BaseModel):
    tenant_id: str
    task: str

class ExecutionResponse(BaseModel):
    execution_id: UUID
    tenant_id: str
    task: str
    status: ExecutionStatus
    result: str | None
    error: str | None   
    created_at: datetime
    updated_at: datetime