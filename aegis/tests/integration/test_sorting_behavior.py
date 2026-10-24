import pytest

from app.application.create_execution import CreateExecutionCommand, CreateExecution
from app.domain.execution import ExecutionStatus
from app.infra.repository.execution_repository import ExecutionRepository

@pytest.mark.asyncio
async def test_sorting_executions(client):
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

    response_1 = create_response1.json()
    response_2 = create_response2.json()
    response_3 = create_response3.json()

    get_response = await client.get("/api/v1/executions/?sort=created_at&order=asc")
    
    assert get_response.status_code == 200

    executions_json = get_response.json()

    returned_ids = [
        execution["execution_id"] for execution in executions_json
    ]

    assert returned_ids[0] == response_1["execution_id"]
    assert returned_ids[1] == response_2["execution_id"]
    assert returned_ids[2] == response_3["execution_id"]
