import json
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

import pytest
from fastapi.testclient import TestClient
from api import app
from core import store
from core.triage import triage_incident


@pytest.fixture
def incident(tmp_path, monkeypatch):
    monkeypatch.setenv("CRITICALOPS_DB_PATH", str(tmp_path / "reviews.sqlite"))
    ticket = {"incident_id": "REVIEW-1", "description": "Pump bearing vibration"}
    store.save_incident(ticket, triage_incident(ticket, use_model=False))
    return ticket["incident_id"]


def test_stale_review_does_not_change_history(incident):
    first = store.review_incident(incident, "needs_more_information", "Alice", "Need timestamp", 0)
    assert first["version"] == 1
    with pytest.raises(store.ReviewConflict):
        store.review_incident(incident, "approved", "Bob", "Stale", 0)
    assert store.get_incident(incident)["review_status"] == "needs_more_information"
    assert len(store.audit_history(incident)) == 2
    final = store.review_incident(incident, "approved", "Alice", "Timestamp supplied", 1)
    assert final["version"] == 2
    audit = json.loads(store.audit_history(incident)[-1]["details"])
    assert audit["previous_status"] == "needs_more_information"
    assert audit["actor_type"] == "unverified_demo_label"
    with pytest.raises(store.ReviewConflict):
        store.review_incident(incident, "rejected", "Bob", "Cannot overwrite final", 2)
    assert len(store.audit_history(incident)) == 3


def test_simultaneous_review_has_one_winner(incident):
    gate = Barrier(2)
    def attempt(actor):
        gate.wait()
        try:
            store.review_incident(incident, "needs_more_information", actor, "Concurrent", 0)
            return "saved"
        except store.ReviewConflict:
            return "conflict"
    with ThreadPoolExecutor(max_workers=2) as pool:
        outcomes = list(pool.map(attempt, ["Alice", "Bob"]))
    assert sorted(outcomes) == ["conflict", "saved"]
    assert store.get_incident(incident)["version"] == 1
    assert len(store.audit_history(incident)) == 2


def test_failed_audit_rolls_back_review(incident):
    with store._connect() as conn:
        conn.execute("CREATE TRIGGER fail_review_audit BEFORE INSERT ON audit_events WHEN NEW.event_type='human_review' BEGIN SELECT RAISE(ABORT, 'test failure'); END")
    with pytest.raises(sqlite3.IntegrityError):
        store.review_incident(incident, "approved", "Alice", "Must roll back", 0)
    assert store.get_incident(incident)["review_status"] == "pending"
    assert store.get_incident(incident)["version"] == 0
    assert len(store.audit_history(incident)) == 1


def test_legacy_database_migration_preserves_records(tmp_path, monkeypatch):
    path = tmp_path / "legacy.sqlite"
    monkeypatch.setenv("CRITICALOPS_DB_PATH", str(path))
    with sqlite3.connect(path) as conn:
        conn.execute("CREATE TABLE incidents (incident_id TEXT PRIMARY KEY, created_at TEXT NOT NULL, ticket_json TEXT NOT NULL, triage_json TEXT NOT NULL, review_status TEXT NOT NULL DEFAULT 'pending', reviewer TEXT, review_comment TEXT, reviewed_at TEXT)")
        conn.execute("INSERT INTO incidents VALUES ('OLD', '2026-01-01', '{}', '{}', 'approved', 'Legacy', NULL, NULL)")
    store.init_db()
    store.init_db()
    assert store.get_incident("OLD")["review_status"] == "approved"
    assert store.get_incident("OLD")["version"] == 0


def test_api_errors_and_response_contract(incident):
    with TestClient(app) as client:
        assert client.get(f"/api/incidents/{incident}").json()["version"] == 0
        assert client.post(f"/api/incidents/{incident}/review", json={"decision": "approved", "expected_version": 0}).status_code == 200
        assert client.post(f"/api/incidents/{incident}/review", json={"decision": "rejected", "expected_version": 0}).status_code == 409
        assert client.post(f"/api/incidents/{incident}/review", json={"decision": "invalid"}).status_code == 422
        assert client.post("/api/incidents/missing/review", json={"decision": "approved"}).status_code == 404
        assert client.post("/api/incidents/triage", json={"description": "short"}).status_code == 422
        assert len(client.get(f"/api/incidents/{incident}/audit").json()) == 2
