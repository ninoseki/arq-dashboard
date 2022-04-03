from fastapi.testclient import TestClient


def test_functions(client: TestClient):
    res = client.get("/api/functions/")
    assert res.status_code == 200

    data = res.json()
    assert isinstance(data, list)
