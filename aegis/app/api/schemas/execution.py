from pydantic import BaseModel, Field, StringConstraints
from uuid import UUID
from typing import Annotated
from datetime import datetime

from app.domain.execution import ExecutionStatus

NonEmptyText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]

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
