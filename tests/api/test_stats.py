from fastapi.testclient import TestClient


def test_stats(client: TestClient):
    res = client.get("/api/stats/")
    assert res.status_code == 200

    data = res.json()
    assert isinstance(data, dict)
