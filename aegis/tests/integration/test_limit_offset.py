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

@pytest.mark.asyncio
async def test_status_execution(client):
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

    execution_id1 = response_1["execution_id"]
    execution_id2 = response_2["execution_id"]


    status_id1 = await client.post(f"/api/v1/executions/{execution_id1}/succeed",
                                         json={"result": "Analysis fompleted"})
    
    status_id2 = await client.post(f"/api/v1/executions/{execution_id2}/fail",
                                   json={
                                       "error": "Something failed"
                                   })

    assert status_id1.status_code == 200
    assert status_id2.status_code == 200

    response_3 = status_id1.json()
    response_4 = status_id2.json()

    assert response_3["result"] == "Analysis fompleted"
    assert response_3["error"] is None
    assert response_3["status"] == "succeeded"
    assert response_4["result"] is None
    assert response_4["error"] == "Something failed"
    assert response_4["status"] == "failed"

    succeeded_response = await client.get(f"/api/v1/executions/?status=succeeded")

    failed_response = await client.get(f"/api/v1/executions/?status=failed")

    assert succeeded_response.status_code == 200
    assert failed_response.status_code == 200

    succeeded_list = succeeded_response.json()
    failed_list = failed_response.json()

    succeeded_statuses = [execution["status"] for execution in succeeded_list]
    failed_statuses = [execution["status"] for execution in failed_list]

    assert all(status == "succeeded" for status in succeeded_statuses)
    assert all(status == "failed" for status in failed_statuses)

    assert succeeded_list[0]["execution_id"] == execution_id1
    assert failed_list[0]["execution_id"] == execution_id2
    

    
