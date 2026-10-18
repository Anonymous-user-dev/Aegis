import pytest

from app.application.create_execution import CreateExecutionCommand, CreateExecution
from app.domain.execution import ExecutionStatus
from app.infra.repository.execution_repository import ExecutionRepository

@pytest.mark.asyncio
async def test_limit_execution(client):
    create_response1 = await client.post("/api/v1/executions/",
                                 json={
                                     "tenant_id": "tenant-1",
                                     "task": "analyze the smth",
                                 },
                            )
    create_response2 = await client.post("/api/v1/executions/",
                                     json={
                                         "tenant_id": "tenant-2",
                                         "task": "analyze the smth",
                                     },
                                )
    create_response3 = await client.post("/api/v1/executions/",
                                     json={
                                         "tenant_id": "tenant-3",
                                         "task": "analyze the smth",
                                     },
                                )

    response = await client.get("/api/v1/executions/?limit=2")

    response_json = response.json()

    assert response.status_code == 200
    assert len(response_json) == 2