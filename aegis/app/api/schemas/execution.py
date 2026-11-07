from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from app.domain.execution import ExecutionStatus
from app.api.schemas.common import NonEmptyText

class SucceedExecutionRequest(BaseModel):
    result: NonEmptyText

class FailedExecutionRequest(BaseModel):
    error: NonEmptyText

class CreateExecutionRequest(BaseModel):
    tenant_id: NonEmptyText
    task: NonEmptyText
    
class ExecutionResponse(BaseModel):
    execution_id: UUID
    tenant_id: str
    task: str
    status: ExecutionStatus
    result: str | None
    error: str | None   
    created_at: datetime
    updated_at: datetime
