import pytest


@pytest.mark.asyncio
async def test_location_header(client):
    response = await client.post("/api/v1/executions/",
                                 json={
                                     "tenant_id": "tenant-2020",
                                     "task": "Analyze smth"
                                 })
    execution_id = response.json()["execution_id"]

    assert response.status_code == 201
    assert response.headers["Location"] == f"/api/v1/executions/{execution_id}"