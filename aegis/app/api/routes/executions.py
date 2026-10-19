from fastapi import APIRouter,status, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas.execution import ExecutionResponse, CreateExecutionRequest, SucceedExecutionRequest, FailedExecutionRequest
from app.api.dependencies import get_session
from uuid import UUID
from app.domain.execution import ExecutionStatus, Execution, InvalidExecutionTransition
from app.infra.repository.execution_repository import ExecutionRepository
from app.application.create_execution import CreateExecution, CreateExecutionCommand
from app.application.succeed_execution import ExecutionNotFound, SucceedExecution, SucceedExecutionCommand
from app.application.fail_execution import ExecutionFail, ExecutionFailCommand
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

@router.post("/{execution_id}/succeed", response_model=ExecutionResponse, status_code=status.HTTP_200_OK)
async def execution_succeeded(execution_id: UUID, request: SucceedExecutionRequest, session: AsyncSession = Depends(get_session)) -> ExecutionResponse:
    repository = ExecutionRepository(session)

    use_case = SucceedExecution(repository)

    command = SucceedExecutionCommand(
        execution_id=execution_id,
        result=request.result)

    try:
        execution = await use_case.execute(command)

    except ExecutionNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Execution not found")

    except InvalidExecutionTransition as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc))

    await session.commit()

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

@router.post("/{execution_id}/fail", response_model=ExecutionResponse, status_code=status.HTTP_200_OK)
async def execution_fail(execution_id: UUID, request: FailedExecutionRequest, session: AsyncSession = Depends(get_session)) -> ExecutionResponse:
    repository = ExecutionRepository(session)
    use_case = ExecutionFail(repository)
    command = ExecutionFailCommand(execution_id, request.error)

    try:
        execution = await use_case.execute(command)

    except ExecutionNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Execution not found")

    except InvalidExecutionTransition as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))

    await session.commit()

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
