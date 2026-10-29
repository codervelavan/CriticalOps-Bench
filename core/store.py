import json
import os
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

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
            "INSERT OR REPLACE INTO incidents(incident_id,created_at,ticket_json,triage_json,review_status) VALUES(?,?,?,?,?)",
            (incident_id, triage["created_at"], json.dumps(ticket), json.dumps(triage), "pending"),
        )
        conn.execute(
            "INSERT INTO audit_events(incident_id,event_type,actor,details) VALUES(?,?,?,?)",
            (incident_id, "triaged", "system-demo", json.dumps({"model_mode": triage.get("model_mode"), "retrieval_mode": triage.get("retrieval_mode")})),
        )
    return triage


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
        triage["ticket"] = json.loads(row["ticket_json"])
        result.append(triage)
    return result


def review_incident(incident_id: str, decision: str, reviewer: str, comment: str) -> Optional[Dict[str, Any]]:
    init_db()
    from datetime import datetime, timezone
    reviewed_at = datetime.now(timezone.utc).isoformat()
    with _connect() as conn:
        row = conn.execute("SELECT triage_json FROM incidents WHERE incident_id=?", (incident_id,)).fetchone()
        if row is None:
            return None
        conn.execute(
            "UPDATE incidents SET review_status=?,reviewer=?,review_comment=?,reviewed_at=? WHERE incident_id=?",
            (decision, reviewer, comment, reviewed_at, incident_id),
        )
        conn.execute(
            "INSERT INTO audit_events(incident_id,event_type,actor,details) VALUES(?,?,?,?)",
            (incident_id, "human_review", reviewer, json.dumps({"decision": decision, "comment": comment})),
        )
        result = json.loads(row["triage_json"])
        result.update({"review_status": decision, "reviewer": reviewer, "review_comment": comment, "reviewed_at": reviewed_at})
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
