import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_create_execution_api(client):
    response = await client.post(
        "/api/v1/execution/",
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