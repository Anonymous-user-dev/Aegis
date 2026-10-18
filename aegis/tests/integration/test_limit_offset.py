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


@pytest.mark.asyncio
async def test_offset_execution(client):
    create_response1 = await client.post("/api/v1/executions/",
                                 json={
                                     "tenant_id": "tenant-1",
                                     "task": "analyze the smth",
                                 },
                            )

    response_1 = create_response1.json()

    create_response2 = await client.post("/api/v1/executions/",
                                     json={
                                         "tenant_id": "tenant-2",
                                         "task": "analyze the smth",
                                     },
                                )

    response_2 = create_response2.json()
    
    create_response3 = await client.post("/api/v1/executions/",
                                     json={
                                         "tenant_id": "tenant-3",
                                         "task": "analyze the smth",
                                     },
                                )

    response_3 = create_response3.json()

    response = await client.get("/api/v1/executions/?limit=10&offset=1")

    response_json = response.json()

    returned_ids = [
        execution["execution_id"]
        for execution in response_json
    ]

    assert response.status_code == 200
    assert len(response_json) == 2
    assert response_3["execution_id"] not in returned_ids
    assert response_2["execution_id"] in returned_ids
    assert response_1["execution_id"] in returned_ids