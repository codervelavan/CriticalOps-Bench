import json
import os
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

class ReviewConflict(ValueError):
    """The displayed review is stale or already finalised."""


ROOT = Path(__file__).resolve().parents[1]


def db_path() -> Path:
    raw = os.getenv("CRITICALOPS_DB_PATH", "data/workbench.sqlite")
    path = Path(raw)
    if not path.is_absolute():
        path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _connect():
    conn = sqlite3.connect(str(db_path()))
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with _connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS incidents (
                incident_id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                ticket_json TEXT NOT NULL,
                triage_json TEXT NOT NULL,
                review_status TEXT NOT NULL DEFAULT 'pending',
                reviewer TEXT,
                review_comment TEXT,
                reviewed_at TEXT
            )
        """)
        columns = {r[1] for r in conn.execute("PRAGMA table_info(incidents)")}
        if "version" not in columns:
            conn.execute("ALTER TABLE incidents ADD COLUMN version INTEGER NOT NULL DEFAULT 0")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS audit_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                incident_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                actor TEXT NOT NULL,
                details TEXT NOT NULL
            )
        """)


def save_incident(ticket: Dict[str, Any], triage: Dict[str, Any]) -> Dict[str, Any]:
    init_db()
    incident_id = triage["incident_id"]
    with _connect() as conn:
        conn.execute(
            "INSERT INTO incidents(incident_id,created_at,ticket_json,triage_json,review_status) VALUES(?,?,?,?,?)",
            (incident_id, triage["created_at"], json.dumps(ticket), json.dumps(triage), "pending"),
        )
        conn.execute(
            "INSERT INTO audit_events(incident_id,event_type,actor,details) VALUES(?,?,?,?)",
            (incident_id, "triaged", "system-demo", json.dumps({"model_mode": triage.get("model_mode"), "retrieval_mode": triage.get("retrieval_mode")})),
        )
    return {**triage, "version": 0}


def list_incidents(limit: int = 200) -> List[Dict[str, Any]]:
    init_db()
    with _connect() as conn:
        rows = conn.execute("SELECT * FROM incidents ORDER BY created_at DESC LIMIT ?", (max(1, min(limit, 1000)),)).fetchall()
    result = []
    for row in rows:
        triage = json.loads(row["triage_json"])
        triage["review_status"] = row["review_status"]
        triage["reviewer"] = row["reviewer"]
        triage["review_comment"] = row["review_comment"]
        triage["reviewed_at"] = row["reviewed_at"]
        triage["version"] = row["version"]
        triage["ticket"] = json.loads(row["ticket_json"])
        result.append(triage)
    return result


def review_incident(incident_id: str, decision: str, reviewer: str, comment: str,
                    expected_version: int = 0) -> Optional[Dict[str, Any]]:
    init_db()
    from datetime import datetime, timezone
    if decision not in {"approved", "rejected", "needs_more_information"}:
        raise ValueError("Unsupported review decision")
    reviewed_at = datetime.now(timezone.utc).isoformat()
    with _connect() as conn:
        conn.execute("BEGIN IMMEDIATE")
        row = conn.execute("SELECT * FROM incidents WHERE incident_id=?", (incident_id,)).fetchone()
        if row is None:
            return None
        if row["version"] != expected_version or row["review_status"] in {"approved", "rejected"}:
            raise ReviewConflict("Review changed or was finalised; reload the incident before reviewing")
        conn.execute(
            "UPDATE incidents SET review_status=?,reviewer=?,review_comment=?,reviewed_at=?,version=version+1 WHERE incident_id=? AND version=?",
            (decision, reviewer, comment, reviewed_at, incident_id, expected_version),
        )
        conn.execute(
            "INSERT INTO audit_events(incident_id,event_type,actor,details) VALUES(?,?,?,?)",
            (incident_id, "human_review", reviewer, json.dumps({"actor_type": "unverified_demo_label", "previous_status": row["review_status"], "decision": decision, "comment": comment, "previous_version": expected_version, "version": expected_version + 1})),
        )
        result = json.loads(row["triage_json"])
        result.update({"review_status": decision, "reviewer": reviewer, "review_comment": comment, "reviewed_at": reviewed_at, "version": expected_version + 1})
        return result


def metrics_summary() -> Dict[str, Any]:
    incidents = list_incidents(1000)
    total = len(incidents)
    if not total:
        return {"total_incidents": 0, "pending_reviews": 0, "critical_reviews": 0, "fallback_rate_pct": 0.0, "category_counts": {}, "review_counts": {}}
    pending = sum(1 for x in incidents if x.get("review_status") == "pending")
    critical = sum(1 for x in incidents if x.get("suggested_priority") == "critical_review")
    fallback = sum(1 for x in incidents if x.get("fallback_used"))
    cats, reviews = {}, {}
    for x in incidents:
        cats[x.get("category", "unknown")] = cats.get(x.get("category", "unknown"), 0) + 1
        reviews[x.get("review_status", "pending")] = reviews.get(x.get("review_status", "pending"), 0) + 1
    return {"total_incidents": total, "pending_reviews": pending, "critical_reviews": critical, "fallback_rate_pct": round(fallback / total * 100, 1), "category_counts": cats, "review_counts": reviews}


def get_incident(incident_id: str):
    init_db()
    with _connect() as conn:
        row = conn.execute("SELECT * FROM incidents WHERE incident_id=?", (incident_id,)).fetchone()
    if row is None:
        return None
    result = json.loads(row["triage_json"])
    result.update({key: row[key] for key in ("review_status", "reviewer", "review_comment", "reviewed_at", "version")})
    return result


def audit_history(incident_id: str):
    init_db()
    with _connect() as conn:
        rows = conn.execute("SELECT * FROM audit_events WHERE incident_id=? ORDER BY id", (incident_id,)).fetchall()
    return [dict(row) for row in rows]
