from fastapi import APIRouter,status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas.execution import ExecutionResponse, CreateExecutionRequest
from app.api.dependencies import get_session
from uuid import UUID
from app.infra.repository.execution_repository import ExecutionRepository
from app.application.create_execution import CreateExecution, CreateExecutionCommand
router = APIRouter()

@router.post("/", response_model=ExecutionResponse, status_code=status.HTTP_201_CREATED)
async def create_execution(request: CreateExecutionRequest, session: AsyncSession = Depends(get_session)):
    repository = ExecutionRepository(session)

    use_case = CreateExecution(repository)

    command = CreateExecutionCommand(
        tenant_id=request.tenant_id,
        task=request.task
    )

    execution = await use_case.create(command)

    await session.commit()

    return ExecutionResponse(
    execution_id=execution.execution_id,
    tenant_id=execution.tenant_id,
    task=execution.task,
    status=execution.status,
    result=execution.result,
    error=execution.error,
    created_at=execution.created_at,
    updated_at=execution.updated_at)


@router.get("/{execution_id}", response_model=ExecutionResponse)
async def get_execution_by_id(execution_id: UUID, session: AsyncSession = Depends(get_session)):
    repository = ExecutionRepository(session)

    execution = await repository.get_by_id(execution_id)

    if execution is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
        )

    return ExecutionResponse(
        execution_id=execution.execution_id,
        tenant_id=execution.tenant_id,
        task=execution.task,
        status=execution.status,
        result=execution.result,
        error=execution.error,
        created_at=execution.created_at,
        updated_at=execution.updated_at,
    )