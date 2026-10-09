from fastapi import APIRouter,status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas.execution import ExecutionResponse, ExecutionCommandRequest
from app.api.dependencies import get_session
from app.infra.repository.execution_repository import ExecutionRepository
from app.application.create_execution import CreateExecution, CreateExecutionCommand
router = APIRouter(
    prefix="/v1/executions",
    tags=["executions"]
)

@router.post("", response_model=ExecutionResponse, status_code=status.HTTP_201_CREATED)
async def create_execution(request: ExecutionCommandRequest, session: AsyncSession = Depends(get_session)):
    repository = ExecutionRepository(session)

    use_case = CreateExecution(repository)

    command = CreateExecutionCommand(
        tenant_id=request.tenant_id,
        task=request.task
    )

    execution = await use_case.create(command)

    await session.commit()


