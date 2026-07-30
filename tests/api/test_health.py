from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_healthz():
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_readyz_shape():
    resp = client.get("/readyz")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] in ("ok", "degraded")
    assert set(data["checks"].keys()) == {"env", "ticket_data"}
    assert isinstance(data["missing_env"], list)
