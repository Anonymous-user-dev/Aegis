import pytest
import uuid

from app.domain.execution import Execution, ExecutionStatus
from tests.integration.conftest import TestSessionFactory
from app.infra.repository.execution_repository import ExecutionRepository


@pytest.mark.asyncio
async def test_add_and_get_execution(session):
    execution = Execution.create(tenant_id="random", task="random2")

    repository = ExecutionRepository(session)

    repository.add(execution)
    await session.flush()

    loaded = await repository.get_by_id(execution.execution_id)

    assert loaded is not None
    assert loaded.execution_id == execution.execution_id
    assert loaded.status == ExecutionStatus.PENDING
    assert loaded.result is None
    assert loaded.error is None

@pytest.mark.asyncio
async def test_get_missing_execution_returns_none(session):
    random_id = uuid.uuid4()

    repository = ExecutionRepository(session)

    loaded = await repository.get_by_id(random_id)

    assert loaded is None
