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
    assert "ETag" in first_get.headers

    etag = first_get.headers["ETag"]

    second_get = await client.get(f"/api/v1/executions/{execution_id}",
                                  headers={
                                      "If-None-Match": etag,
                                  })

    assert second_get.status_code == 304
    assert second_get.text == ""

@pytest.mark.asyncio
async def test_execution_etag_changes_after_update(client):
    create_response = await client.post("/api/v1/executions/",
                                        json={
                                            "tenant_id": "tenant-etag2",
                                            "task": "test etag"
                                        })
    assert create_response.status_code == 201

    execution_id = create_response.json()["execution_id"]

    

    first_get = await client.get(f"/api/v1/executions/{execution_id}")

    assert first_get.status_code == 200
    assert "ETag" in first_get.headers

    etag = first_get.headers["ETag"]

    second_response = await client.post(f"/api/v1/executions/{execution_id}/succeed",
                                        json={
                                            "result": "Finished"
                                        })
    assert second_response.status_code == 200

    second_get = await client.get(f"/api/v1/executions/{execution_id}",
                                  headers={
                                      "If-None-Match": etag
                                  })

    assert second_get.status_code == 200
    assert second_get.headers["ETag"] != etag
    assert second_get.json()["status"] == "succeeded"

@pytest.mark.asyncio
async def test_cache_control_returns_no_store(client):
    create_response = await client.post("/api/v1/executions/",
                                        json={
                                            "tenant_id": "tenant-cache",
                                            "task": "test cache-control"
                                        })
    assert create_response.status_code == 201

    execution_id = create_response.json()["execution_id"]

    get = await client.get(f"/api/v1/executions/{execution_id}")

    assert get.status_code == 200
    assert get.headers["Cache-Control"] == "no-store"