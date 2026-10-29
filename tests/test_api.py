from fastapi.testclient import TestClient
from api import app


def test_api_triage_and_human_review(tmp_path, monkeypatch):
    monkeypatch.setenv("CRITICALOPS_DB_PATH", str(tmp_path / "test.sqlite"))
    with TestClient(app) as client:
        assert client.get("/health").status_code == 200
        response = client.post("/api/incidents/triage", json={
            "description": "Pump vibration is increasing and bearing noise started this morning",
            "asset_id": "PUMP-204", "site": "Demo Site", "production_impact": 3,
            "estimated_downtime_hours": 1, "safety_related": False,
        })
        assert response.status_code == 200
        incident_id = response.json()["incident_id"]
        review = client.post(f"/api/incidents/{incident_id}/review", json={
            "decision": "approved", "reviewer": "Test Reviewer", "comment": "Reviewed in test",
        })
        assert review.status_code == 200
        assert review.json()["review_status"] == "approved"


def test_duplicate_preserves_review_and_history(tmp_path, monkeypatch):
    monkeypatch.setenv("CRITICALOPS_DB_PATH", str(tmp_path / "duplicate.sqlite"))
    with TestClient(app) as client:
        ticket = {"incident_id": "FIXED-1", "description": "Pump bearing vibration"}
        assert client.post("/api/incidents/triage", json=ticket).status_code == 200
        assert client.post("/api/incidents/FIXED-1/review", json={"decision": "approved"}).status_code == 200
        assert client.post("/api/incidents/triage", json=ticket).status_code == 409
        assert client.get("/api/incidents/FIXED-1").json()["review_status"] == "approved"
        assert len(client.get("/api/incidents/FIXED-1/audit").json()) == 2
        assert client.get("/api/incidents/unknown").status_code == 404
        assert client.get("/api/incidents/unknown/audit").status_code == 404
