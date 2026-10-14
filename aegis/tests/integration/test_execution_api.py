import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
import uuid


@pytest.mark.asyncio
async def test_create_execution_api(client):
    response = await client.post(
        "/api/v1/executions/",
        json={
            "tenant_id": "tenant-1",
            "task": "Analyze something",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["tenant_id"] == "tenant-1"
    assert body["task"] == "Analyze something"
    assert body["status"] == "pending"
    assert body["result"] is None
    assert body["error"] is None

@pytest.mark.asyncio
async def test_get_existing_execution(client):
    create_response = await client.post(
        "/api/v1/executions/",
        json={
            "tenant_id": "tenant-0",
            "task": "Make a summary",
        },
    )

    created_body = create_response.json()

    execution_id = created_body["execution_id"]

    response = await client.get(
        f"/api/v1/executions/{execution_id}"
    )

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_nonexisting_execution(client):
    execution_id = uuid.uuid4()

    response = await client.get(
        f"/api/v1/executions/{execution_id}"
    )

    assert response.status_code == 404
