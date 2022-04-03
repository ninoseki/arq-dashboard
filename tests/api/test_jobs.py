from fastapi.testclient import TestClient


def test_jobs(client: TestClient):
    res = client.get("/api/jobs/")
    assert res.status_code == 200

    data = res.json()
    assert isinstance(data, dict)
