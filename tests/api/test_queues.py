from fastapi.testclient import TestClient


def test_queues(client: TestClient):
    res = client.get("/api/queues/")
    assert res.status_code == 200

    data = res.json()
    assert isinstance(data, list)
