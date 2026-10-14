from fastapi import APIRouter,status, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas.execution import ExecutionResponse, CreateExecutionRequest
from app.api.dependencies import get_session
from uuid import UUID
from app.domain.execution import ExecutionStatus, Execution
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

@router.get("/", response_model=list[ExecutionResponse], status_code=status.HTTP_200_OK)
async def get_all_executions(session: AsyncSession = Depends(get_session), execution_status: ExecutionStatus | None = Query(default=None, alias="status"), limit: int = Query(default=10, ge=1, le=100), offset: int = Query(default=0, ge=0)) -> list[ExecutionResponse]:
    repository = ExecutionRepository(session=session)

    executions = await repository.list(limit=limit, offset=offset, status=execution_status)

    responses = [
        ExecutionResponse(
        execution_id=execution.execution_id,
        tenant_id=execution.tenant_id,
        task=execution.task,
        status=execution.status,
        result=execution.result,
        error=execution.error,
        created_at=execution.created_at,
        updated_at=execution.updated_at,
        )
        for execution in executions
    ]

    return responses