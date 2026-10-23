import pytest
import uuid

from app.application.create_execution import CreateExecutionCommand, CreateExecution
from app.domain.execution import ExecutionStatus
from app.infra.repository.execution_repository import ExecutionRepository

@pytest.mark.asyncio
async def test_limit_zero_returns_validation_error(client):
    response = await client.get("/api/v1/executions/?limit=0")

    assert response.status_code == 422

@pytest.mark.asyncio
async def test_negative_offset_returns_validation_error(client):
    response = await client.get("/api/v1/executions/?offset=-1")

    assert response.status_code == 422

@pytest.mark.asyncio
async def test_unknown_status_returns_validation_error(client):
    response = await client.get("/api/v1/executions/?status=garbage")

    assert response.status_code == 422

@pytest.mark.asyncio
async def test_exceeded_limit_returns_validation_error(client):
    response = await client.get("/api/v1/executions/?limit=101")

    assert response.status_code == 422

@pytest.mark.asyncio
async def test_create_execution_rejects_whitespace_tenant_id(client):
    response = await client.post("/api/v1/executions/",
                                 json={
                                     "tenant_id": "      ",
                                     "task": "Random task"
                                 })

    assert response.status_code == 422

@pytest.mark.asyncio
async def test_create_execution_rejects_whitespace_task(client):
    response = await client.post("/api/v1/executions/",
                                 json={
                                     "tenant_id": "Tenant-022",
                                     "task": "    "
                                 })

    assert response.status_code == 422

@pytest.mark.asyncio 
async def test_missing_execution(client):
    execution_id = uuid.uuid4()

    response = await client.post(f"/api/v1/executions/{execution_id}/succeed",
                                 json={
                                     "result": "Completed"
                                 })

    assert response.status_code == 404

@pytest.mark.asyncio
async def test_invalid_execution_transition(client):
    response_1 = await client.post(f"/api/v1/executions/",
                                         json={
                                             "tenant_id": "tenant-023",
                                             "task": "Analyze smth"
                                         })

    response_1_json = response_1.json()
    execution_id = response_1_json["execution_id"]

    response_succeed = await client.post(f"/api/v1/executions/{execution_id}/succeed", json={
        "result": "Finished"
        })

    response_fail = await client.post(f"/api/v1/executions/{execution_id}/fail",
                                      json={
                                          "error": "Error"
                                      })

    assert response_fail.status_code == 409
    assert response_1.status_code == 201
    assert response_succeed.status_code == 200