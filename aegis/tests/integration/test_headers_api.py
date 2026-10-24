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

@pytest.mark.asyncio
async def test_execution_etag_returns_304_when_unchanged(client):
    create_response = await client.post("/api/v1/executions/",
                                        json={
                                            "tenant_id": "tenant-etag",
                                            "task": "Analyze etag"
                                        })

    assert create_response.status_code == 201

    execution_id = create_response.json()["execution_id"]

    first_get = await client.get(f"/api/v1/executions/{execution_id}")

    assert first_get.status_code == 200
    assert "Etag" in first_get.headers

    etag = first_get.headers["Etag"]

    second_get = await client.get(f"/api/v1/executions/{execution_id}",
                                  headers={
                                      "If-None-Match": etag,
                                  })

    assert second_get.status_code == 304
    assert second_get.text == ""