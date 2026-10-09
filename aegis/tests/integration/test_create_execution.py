import pytest

from app.application.create_execution import CreateExecutionCommand, CreateExecution
from app.domain.execution import ExecutionStatus
from app.infra.repository.execution_repository import ExecutionRepository

@pytest.mark.asyncio
async def test_create_execution(session):
    repository = ExecutionRepository(session)
    use_case = CreateExecution(repository)

    command = CreateExecutionCommand(
        tenant_id="tenant-1",
        task="Analyze this paper etc"
    )

    execution = await use_case.create(command)

    await session.flush()

    loaded = await repository.get_by_id(execution.execution_id)

    assert loaded is not None
    assert loaded.tenant_id == "tenant-1"
    assert loaded.task == "Analyze this paper etc"
    assert loaded.status == ExecutionStatus.PENDING
